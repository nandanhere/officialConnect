# OfficialConnect analytics and reliability plan

Date: 2026-09-21. Baseline window (live GA/Firebase overview): last 28 days
Aug 24–Sep 20, 2026; headline engagement figures quoted for last 7 days
unless noted.

Status: planning only. No app code, Firebase/GA settings, Crashlytics
permissions, releases, or account changes were made to produce this plan.

## 1. Baseline (live observations, not older evidence)

- Project: `unofficialconnect`. App: `official_connect`, latest Android
  release `1.1.4` marked successful.
- Scale: 2.2K active users (7d), 2.3K (30d); 63K events and 2K key events
  (7d).
- Engagement (visible): 3m 02s average per active user, 1m 11s per session,
  1.5 engaged sessions per active user.
- Stability: ~97.5% crash-free users in the Firebase stability overview.
  Stack-level diagnosis is not available in the analytics view; it requires
  Crashlytics console access.
- Screens: default screen reporting collapses into `MainActivity` (~6.3K
  views); custom `app_screen_view` carries ~24K events. The custom stream is
  currently the trustworthy screen signal.
- Funnels: `sync_section` ~11K events; `login_flow_started` and
  `feature_opened` ~3.4K each.
- Retention (visible cohort chart): ~68.2% at week one for the mature portion;
  later columns are immature and must not be read as regressions.
- Platform split: Android accounts for essentially all key events; iOS is
  effectively zero — consistent with the known iOS blocker (stale `1.1.0+7`
  artifact, no current release), not necessarily a product signal.
- Prior signal (unverified against current data): earlier live event analysis
  found ~5% of login starts without a recorded completion event. Treat as a
  hypothesis to verify, not a current measurement.

## 2. Problem statement

1. Screen reporting is split and misleading by default: native auto screen
   reporting (`MainActivity`) shadows the real Flutter screen breakdown, so
   anyone reading the default Screens report gets the wrong picture.
2. Login/sync health is event-rich but funnel-poor: starts, sections, and
   features are counted, but completion/drop-off by outcome, stage, and
   release cohort is not routinely checked.
3. Crash signal stops at the headline: 97.5% crash-free users is known, but
   the top crashing stacks, affected versions, and device clustering are
   unknown without Crashlytics console work.
4. Retention and version signals are easy to misread: immature cohort columns
   and the Android/iOS imbalance invite wrong conclusions.
5. Local-build contamination is a standing risk: any misconfigured analytics
   opt-in from a dev build pollutes production funnels.

## 3. Hypotheses (ranked, falsifiable)

- H1 — Screen collapse cause: native automatic screen reporting is still on,
  and `FirebaseSyncDiagnostics` reports every screen with a constant
  `screenClass: 'OfficialConnect'` (see
  `lib/Services/firebase_sync_diagnostics.dart`), so the default report cannot
  separate Flutter routes. Falsify by: per-screen `screenClass` (or disabling
  auto reporting) makes the default Screens report match `app_screen_view`
  proportions.
- H2 — Login gap is real but small: ~5% of `login_flow_started` lack a paired
  `login_flow_finished` (by `flow_id`) within a timeout window, concentrated
  in specific `failure_stage`/`failure_reason` values (session_expired,
  timeout, network_error). Falsify by: flow_id-paired funnel over the current
  28d window shows gap < 1% or evenly spread with no clustering.
- H3 — Sync partials cluster by section: `sync_section` outcomes other than
  success/complete concentrate in 1–2 sections (candidates: results, seating)
  and correlate with `parse_error`/`content_not_ready`. Falsify by: per-section
  outcome table shows uniform success.
- H4 — Crashes cluster by version/device: the 2.5% non-crash-free share is
  dominated by older builds or a small device set, not `1.1.4`. Falsify by:
  Crashlytics version/device breakdown shows `1.1.4` dominant.
- H5 — iOS zero is distribution, not instrumentation: iOS key events are zero
  because there is no current iOS release in the field (blocker in
  `CURRENT_STATE.md`), not because iOS logging is broken. Falsify by: a
  current-version iOS session emits events that never arrive.

## 4. In-repo vs account-access work

In-repo (Muse/another engineer can do without console access):

- Screen reporting fix, event-schema tightening, funnel query scripts over
  exported data, unit/widget tests for the diagnostics layer, docs.
- Files of interest: `lib/Services/sync_diagnostics.dart`,
  `lib/Services/firebase_sync_diagnostics.dart`,
  `lib/Services/firebase_crash_reporting.dart`, `lib/Services/app_distribution.dart`.

Requires Firebase/GA/Crashlytics account access (cannot be done in-repo):

- Reading Crashlytics stacks, affected versions, device models.
- Building/saving GA explorations, dashboards, audiences, release cohorts.
- Changing GA data-retention, key-event definitions, or Crashlytics alert
  velocity thresholds.
- Marking releases or comparing version cohorts in the console.

Rule: in-repo work must never embed secrets, tokens, or personal data; device
model and version are aggregate-only dimensions (see schema).

## 5. Measurement schema (proposed, additive)

Conventions: all new params optional; never log user IDs, emails, USNs, or
raw portal content. Durations in ms clamped as today. `flow_id` stays a
short random hex per attempt, joined across start/finish/attention.

Common params on every custom event (add where missing):

- `app_version`: e.g. `1.1.4+12` (currently not attached to custom events).
- `release_cohort`: e.g. `1.1.4`, derived from `app_version`; used for
  version segmentation without console release-marking.
- `platform`: `android` / `ios` (do not rely on console auto-dimension in
  exported-data queries).
- `sync_mode`: already present on login/sync events; extend to
  `feature_state_shown` where relevant.

Per area:

- Screen views: `app_screen_view{screen, app_version, platform}`;
  `screen_time{screen, duration_ms, app_version}`. Fix: pass distinct
  `screenClass` per screen (or the screen name itself) in
  `analytics.logScreenView`, and disable native auto screen reporting if the
  duplicate `MainActivity` row persists.
- Login: `login_flow_started{sync_mode, flow_id, platform, app_version}` →
  exactly one of `login_flow_finished{outcome, sync_mode, flow_id,
  duration_ms}` or `login_flow_attention{reason, stage, sync_mode,
  duration_ms}`. Acceptance: ≥ 99% of starts pair within 15 min in the
  verification window, or the unpaired remainder is explained by reason/stage.
- Sync: `sync_section{section, outcome, item_count, attempted_count,
  failed_count, duration_ms, sync_mode, parser_version, failure_reason?,
  app_version}` + `sync_finished{outcome, section_count, duration_ms,
  sync_mode, parser_version, failure_stage?, failure_reason?, app_version}`.
- Exceptions/ops: `operation_failure{operation, stage, reason, sync_mode,
  app_version}` mirrored to Crashlytics non-fatal via
  `recordOperationalIssue` (already wired); add `app_version` to the
  Crashlytics custom keys so non-fatals segment by release.
- Device/release: consume console-provided `device model`, `OS version`,
  `app version` dimensions in Crashlytics/GA — never log device identifiers
  or build fingerprints as event params.

## 6. Dashboards and funnel checks (account-access, specified so an engineer
## with access can build them in one pass)

- D1 — Screen truth: exploration comparing default Screens vs
  `app_screen_view{screen}` counts over 28d; done when both agree within 5%
  after the H1 fix, or the default report is formally deprecated in favor of
  the custom event.
- D2 — Login funnel: `login_flow_started` → `login_flow_finished` by
  `outcome`, segmented by `sync_mode`, `failure_stage`, `failure_reason`,
  `release_cohort`; includes unpaired-start rate by `flow_id` (the H2 check).
- D3 — Sync health: `sync_section` outcome rate per `section`, plus
  `sync_finished` outcome distribution; segmented by `sync_mode` and
  `release_cohort` (the H3 check).
- D4 — Crash triage: top Crashlytics issues by users affected with version
  and device-model breakdown; velocity alerts noted (the H4 check).
- D5 — Retention read correctly: cohort table annotated with mature vs
  immature columns; week-one ~68.2% re-baselined after each release.

## 7. Crash diagnosis procedure (account access required)

1. Open Crashlytics for `unofficialconnect`, filter to version `1.1.4`,
   last 28d.
2. Record top 3 issues by affected users: title, fatal vs non-fatal,
   first-seen version, device-model cluster.
3. Cross-reference each against `operation_failure` reason/stage and
   `sync_section` failure_reason for the same window.
4. File one kanban card per issue with stack signature and version/device
   scope; do not paste stack frames containing personal data into planning
   docs.

## 8. Retention interpretation guardrails

- Only read mature columns; later columns in the visible chart are immature.
- Always segment by `release_cohort` before concluding a retention change.
- The iOS-zero split is a distribution artifact until a current iOS build
  ships; do not compare platform retention until then.

## 9. Release/version segmentation

- Until console release-marking is available, `release_cohort` (in-repo param)
  is the segmentation key.
- With console access: mark `1.1.4` as the baseline release, then compare
  login completion, sync success, and crash-free users per cohort on every
  subsequent release.

## 10. Acceptance criteria (plan-level)

- Screen reporting: one documented source of truth; default vs custom counts
  agree within 5% or the deprecated one is named.
- Login funnel: paired-start rate measured on current 28d data; H2 confirmed
  or refuted with numbers and stage/reason breakdown.
- Sync: per-section outcome table published; any section with < 95% success
  has a follow-up card.
- Crash: top-3 stacks identified with version/device scope, or access blocker
  recorded with the exact missing permission.
- Retention: mature week-one figure re-recorded with its date range; no claim
  made from immature columns.
- Privacy: no secrets, tokens, user IDs, or personal data in events,
  dashboards, or planning docs.

## 11. Staged execution order

- Stage 0 — Verify without changes (no access needed beyond read-only
  console): run the D2/D3 funnel checks on current data; confirm or refute
  H2/H3; record numbers in `CURRENT_STATE.md`.
- Stage 1 — In-repo instrumentation (no console writes): H1 screen fix +
  `app_version`/`release_cohort`/`platform` params + Crashlytics
  `app_version` key; unit tests on `SyncDiagnostics` allowlists/clamping;
  guard local-build contamination (existing `setEnabled(false)` path).
  - Implemented 2026-09-21 (see `CURRENT_STATE.md`); console-side
    verification (D1 7d agreement, D2/D3 funnels) still pending Stage 2.
- Stage 2 — Console work (access required): build D1–D5; run crash triage
  procedure; mark `1.1.4` baseline.
- Stage 3 — Follow-through: file per-issue cards from findings; re-measure
  one full 7d window post-fix; update retention baseline.
- Stage 4 — iOS: after the sideload blocker clears and a current iOS build
  ships, test H5 and only then read platform splits as product signals.

## 12. Risks and non-goals

- Contamination from local builds sending production events; mitigated by the
  existing opt-in gate — keep it.
- Over-logging: schema is additive and bounded; no free-text or portal
  content params.
- Non-goals: changing Firebase/GA settings, Crashlytics permissions,
  releases, or credentials in this plan; those need explicit authorization.
