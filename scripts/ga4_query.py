#!/usr/bin/env python3
"""Query OfficialConnect GA4 analytics without a browser.

Replaces the manual GA4 Realtime/exploration checks with the GA4 Data API:
- `section-timing`: per-section mean of duration_ms for sync_section
  events with sync_mode=refresh (the Task 2 exploration; median/max need
  the GA4 UI — the Data API client only aggregates TOTAL/COUNT).
- `event-check`: look for an event name (e.g. refresh_finished) in the
  last-30-min Realtime window (the Task 3/4 check).

Auth: uses Application Default Credentials — set GOOGLE_APPLICATION_CREDENTIALS
to a service-account JSON key that has Viewer on the GA4 property. The key
must NEVER live in the repo. Property id via --property or GA4_PROPERTY_ID.

Requires: pip install google-analytics-data
"""

import argparse
import os
import sys

PROPERTY_ENV = "GA4_PROPERTY_ID"


def _client():
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
    except ImportError:
        sys.exit("Missing dependency: pip install google-analytics-data")
    try:
        return BetaAnalyticsDataClient()
    except Exception as exc:  # noqa: BLE001 - surface auth errors plainly
        sys.exit(f"Could not create GA4 client (check credentials): {exc}")


def _property(args) -> str:
    prop = args.property or os.environ.get(PROPERTY_ENV, "")
    if not prop:
        sys.exit(f"Set --property or {PROPERTY_ENV} to the GA4 numeric property id.")
    return f"properties/{prop}"


def cmd_section_timing(args) -> int:
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Filter,
        FilterExpression,
        FilterExpressionList,
        Metric,
        MetricAggregation,
        RunReportRequest,
    )

    client = _client()
    request = RunReportRequest(
        property=_property(args),
        dimensions=[Dimension(name="customEvent:section")],
        metrics=[
            Metric(name="customEvent:duration_ms"),
            Metric(name="eventCount"),
        ],
        # TOTAL only (this API version lacks AVERAGE/MEDIAN); the
        # per-section mean is derived locally as total_ms / events.
        metric_aggregations=[MetricAggregation.TOTAL],
        dimension_filter=FilterExpression(
            and_group=FilterExpressionList(
                expressions=[
                    FilterExpression(
                        filter=Filter(
                            field_name="eventName",
                            string_filter={"value": "sync_section"},
                        )
                    ),
                    FilterExpression(
                        filter=Filter(
                            field_name="customEvent:sync_mode",
                            string_filter={"value": "refresh"},
                        )
                    ),
                ]
            )
        ),
        date_ranges=[DateRange(start_date=args.days_ago, end_date="today")],
    )
    try:
        response = client.run_report(request)
    except Exception as exc:  # noqa: BLE001
        sys.exit(f"Report request failed: {exc}")
    if not response.rows:
        print("No sync_section/refresh rows in range (definitions accrue from Sep 23, 2026).")
        return 0
    print(f"{'section':<24}{'avg_ms':>10}{'events':>8}{'total_ms':>10}")
    for row in response.rows:
        section = row.dimension_values[0].value
        # With TOTAL+COUNT aggregations each section yields one summary row
        # (RESERVED_*) plus its detail row; the detail row carries values.
        values = [v.value for v in row.metric_values]
        total = float(values[0]) if values[0] else 0.0
        count = int(float(values[1])) if len(values) > 1 and values[1] else 0
        avg = total / count if count else 0.0
        print(f"{section:<24}{avg:>10.1f}{count:>8}{total:>10.0f}")
    return 0


# 28-day per-section mean durations (ms), measured 2026-09-25. A daily
# mean above 2x baseline is flagged; retune after major portal changes.
SECTION_BASELINES_MS = {
    "results": 30800,
    "fees": 10000,
    "marks": 9500,
    "attendance": 7900,
    "proctor": 1900,
    "profile": 0,  # uninstrumented upstream; excluded from checks
}

_SYNC_OK = {"ok", "complete", "success", "partial", "empty"}
_SYNC_BAD = {"error", "timeout", "session_expired", "network_error"}


def _run(client, prop, dimensions, metrics, date, extra_filter=None):
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Metric,
        RunReportRequest,
    )

    req = RunReportRequest(
        property=prop,
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        date_ranges=[DateRange(start_date=date, end_date=date)],
    )
    if extra_filter is not None:
        req.dimension_filter = extra_filter
    try:
        return client.run_report(req), None
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def _event_filter(event_names):
    from google.analytics.data_v1beta.types import Filter, FilterExpression

    return FilterExpression(
        filter=Filter(
            field_name="eventName",
            in_list_filter={"values": list(event_names)},
        )
    )


def cmd_daily_health(args) -> int:
    """One lightweight daily quality gate over yesterday's events (~3 calls)."""
    client = _client()
    prop = _property(args)
    day = args.date
    verdicts = []  # (level, message); level in OK/WARN/FAIL

    def outcome_breakdown(event):
        resp, err = _run(
            client, prop,
            ["customEvent:outcome"], ["eventCount"], day,
            _event_filter([event]),
        )
        if err:
            return None, err
        return {r.dimension_values[0].value: int(r.metric_values[0].value)
                for r in resp.rows}, None

    # 1. Sync outcome mix.
    sync, err = outcome_breakdown("sync_finished")
    if err:
        verdicts.append(("FAIL", f"sync_finished unreadable: {err}"))
    elif not sync:
        verdicts.append(("WARN", "sync_finished: no events yesterday"))
    else:
        total = sum(sync.values())
        bad = sum(v for k, v in sync.items() if k in _SYNC_BAD)
        rate = bad / total if total else 0.0
        detail = ", ".join(f"{k}={v}" for k, v in sorted(sync.items()))
        if rate >= 0.15:
            verdicts.append(("FAIL", f"sync error rate {rate:.0%} ({detail})"))
        elif rate >= 0.05:
            verdicts.append(("WARN", f"sync error rate {rate:.0%} ({detail})"))
        else:
            verdicts.append(("OK", f"sync error rate {rate:.0%} ({detail})"))

    # 2. Top failure reasons across sync + operational failures.
    from google.analytics.data_v1beta.types import (
        Dimension as _Dim, Metric as _Met, DateRange as _DR,
        RunReportRequest as _RR,
    )
    try:
        resp = client.run_report(_RR(
            property=prop,
            dimensions=[_Dim(name="customEvent:failure_reason")],
            metrics=[_Met(name="eventCount")],
            date_ranges=[_DR(start_date=day, end_date=day)],
            dimension_filter=_event_filter(
                ["sync_section", "sync_finished", "operation_failure"]),
        ))
        reasons = sorted(
            ((r.dimension_values[0].value or "(none)",
              int(r.metric_values[0].value)) for r in resp.rows),
            key=lambda kv: -kv[1],
        )[:3]
        if reasons:
            verdicts.append(("OK", "top failure reasons: " + ", ".join(
                f"{k}={v}" for k, v in reasons)))
    except Exception as exc:  # noqa: BLE001
        verdicts.append(("WARN", f"failure reasons unreadable: {exc}"))

    # 3. Section durations vs baseline (yesterday's mean per section).
    resp, err = _run(
        client, prop,
        ["customEvent:section"],
        ["customEvent:duration_ms", "eventCount"], day,
        _event_filter(["sync_section"]),
    )
    if err:
        verdicts.append(("FAIL", f"section timing unreadable: {err}"))
    else:
        for r in resp.rows:
            section = r.dimension_values[0].value
            base = SECTION_BASELINES_MS.get(section)
            if not base:
                continue
            total = float(r.metric_values[0].value or 0)
            count = int(float(r.metric_values[1].value or 0))
            mean = total / count if count else 0.0
            if mean > 2 * base:
                verdicts.append((
                    "WARN",
                    f"{section} mean {mean:.0f}ms > 2x baseline {base}ms"))
        verdicts.append(("OK", "section durations within 2x baseline"))

    # 4. Login completion.
    login, err = outcome_breakdown("login_flow_finished")
    if err:
        verdicts.append(("FAIL", f"login outcomes unreadable: {err}"))
    elif login:
        total = sum(login.values())
        good = sum(v for k, v in login.items() if k in _SYNC_OK)
        rate = good / total if total else 0.0
        detail = ", ".join(f"{k}={v}" for k, v in sorted(login.items()))
        if rate < 0.90:
            verdicts.append(("WARN", f"login success {rate:.0%} ({detail})"))
        else:
            verdicts.append(("OK", f"login success {rate:.0%} ({detail})"))

    # 5. Version adoption among syncing users (info only; unenriched
    # events such as raw screen views carry no app_version).
    resp, err = _run(
        client, prop, ["customEvent:app_version"], ["eventCount"], day,
        _event_filter(["sync_finished"]))
    if not err and resp.rows:
        mix = {r.dimension_values[0].value: int(r.metric_values[0].value)
               for r in resp.rows}
        total = sum(mix.values()) or 1
        top = sorted(mix.items(), key=lambda kv: -kv[1])[:3]
        if len(mix) == 1 and next(iter(mix)) == "":
            # app_version only ships from 1.1.5 onward; a fully blank mix
            # means the base is still on older clients.
            verdicts.append(("OK", "version mix: pre-1.1.5 clients (no data)"))
        else:
            verdicts.append(("OK", "version mix: " + ", ".join(
                f"{k or '(unset)'}={v / total:.0%}" for k, v in top)))

    levels = [level for level, _ in verdicts]
    for level, message in verdicts:
        print(f"[{level}] {message}")
    if "FAIL" in levels:
        return 2
    if "WARN" in levels:
        return 1
    return 0


def cmd_event_check(args) -> int:
    from google.analytics.data_v1beta.types import (
        Dimension,
        Filter,
        FilterExpression,
        Metric,
        RunRealtimeReportRequest,
    )

    client = _client()
    request = RunRealtimeReportRequest(
        property=_property(args),
        dimensions=[Dimension(name="eventName")],
        metrics=[Metric(name="eventCount")],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name="eventName",
                string_filter={"value": args.name},
            )
        ),
    )
    try:
        response = client.run_realtime_report(request)
    except Exception as exc:  # noqa: BLE001
        sys.exit(f"Realtime request failed: {exc}")
    total = sum(int(r.metric_values[0].value) for r in response.rows)
    if total:
        print(f"FOUND: {args.name} x{total} in the Realtime window.")
        return 0
    print(f"ABSENT: {args.name} not in the Realtime window (verified negative).")
    return 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--property", default="", help="GA4 numeric property id")
    sub = parser.add_subparsers(dest="cmd", required=True)

    timing = sub.add_parser("section-timing", help="per-section refresh durations")
    timing.add_argument("--days-ago", default="28daysAgo")
    timing.set_defaults(func=cmd_section_timing)

    check = sub.add_parser("event-check", help="Realtime presence of one event")
    check.add_argument("--name", default="refresh_finished")
    check.set_defaults(func=cmd_event_check)

    health = sub.add_parser("daily-health", help="lightweight daily quality gate")
    health.add_argument("--date", default="yesterday")
    health.set_defaults(func=cmd_daily_health)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
