# OfficialConnect kanban

## Done

- [x] Configure Firebase for the existing `unofficialconnect` project.
- [x] Validate Android debug build and SDK/permission configuration.
- [x] Preserve phone navigation.
- [x] Add a genuine adaptive tablet navigation treatment.
- [x] Test phone/tablet navigation, selection, and 200% text scaling.
- [x] Add guarded Play API release workflow without publishing.

## Blocked

- [ ] Build and package the current iOS sideload ZIP.
  - Blocker: full Xcode is not installed/selected; only Command Line Tools are
    active.
  - Exit condition: build a fresh unsigned IPA, inspect its embedded
    `CFBundleShortVersionString` and `CFBundleVersion` as `1.1.4` and `12`,
    generate a SHA-256 checksum and instructions, then place the truthful ZIP
    in `/Users/nandanherekar/Downloads`.

## Next

- [ ] Reinspect the checkout and current toolchain before doing more work.
- [ ] If full Xcode becomes available, rebuild and verify the iOS IPA; otherwise
  leave the blocker documented and do not create a misleading package.
- [ ] If requested, run the broader current Flutter validation suite and report
  unavailable tools or failures exactly.
- [ ] If requested, complete one-time Google Play service-account setup and only
  publish after explicit release authorization and confirmation.

## Analytics and reliability (see ANALYTICS_RELIABILITY_PLAN.md)

In-repo cards (no console access needed):

- [ ] A1 (P1): Verify login/sync funnels on current data. Flow-id-pair
  `login_flow_started` → `login_flow_finished`/`login_flow_attention`;
  per-section `sync_section` outcome table. Done when the ~5% unpaired-start
  prior signal is confirmed or refuted with numbers, or lack of data access
  is recorded as the blocker. No dependencies.
  - 2026-09-21: still blocked — no Firebase/GA export or console access in
    this session, so no numbers recorded. Query spec stands in
    ANALYTICS_RELIABILITY_PLAN.md §6 (D2/D3).
- [x] A2 (P1): Fix screen-report collapse. Give each screen a distinct
  `screenClass` in `FirebaseSyncDiagnostics` (or disable native auto screen
  reporting if the `MainActivity` row persists).
  - 2026-09-21: in-repo fix landed — `logScreenView` now uses the bounded
    route as both `screenName` and `screenClass`
    (`lib/Services/firebase_sync_diagnostics.dart`). 7d agreement check
    (within 5%) still needs console access; tracked under C1/D1.
- [x] A3 (P2): Add `app_version` / `release_cohort` / `platform` params to
  custom events and an `app_version` Crashlytics custom key; keep allowlists
  and clamping in `SyncDiagnostics`.
  - 2026-09-21: landed via `DiagnosticsRelease` in
    `lib/Services/sync_diagnostics.dart` (allowlisted, `APP_VERSION`
    override, test hooks) + `app_version` Crashlytics key in
    `lib/Services/firebase_crash_reporting.dart`. `firebase_operations_test`
    31/31 pass, including opt-out suppression and no-leak checks.
- [ ] A4 (P2): Re-measure one full 7d window after A2+A3 and update the
  retention/maturity baseline. Done when week-one mature figure and its date
  range are recorded in CURRENT_STATE.md. Depends on A2, A3.
  - 2026-09-21: clock starts now that A2+A3 shipped; needs console access
    (C1) plus a full 7d post-fix window.

Console-gated cards (require Firebase/GA/Crashlytics account access):

- [ ] C1 (P1): Build D1–D5 explorations (screen truth, login funnel, sync
  health, crash triage, retention). Done when each has a saved definition and
  the 28d numbers are pasted as aggregates (no personal data). Blocked until
  console access is granted; A1 specifies the queries.
- [ ] C2 (P1): Crash triage on `1.1.4` (top 3 issues by affected users with
  version/device scope). Done when one follow-up card per issue exists, or
  the exact missing Crashlytics permission is recorded. No code dependency.
- [ ] C3 (P3): Mark `1.1.4` as the release baseline for cohort comparison.
  Done when per-cohort login/sync/crash-free views exist. Depends on A3, C1.
- [ ] C4 (P3, after iOS unblocks): Verify iOS event flow on a current build
  and only then read platform splits as product signals. Depends on the iOS
  sideload blocker above and C1.

## Feedback fixes (see REFRESH_TIMETABLE_PLAN.md)

- [x] F1 (P1): Timetable Monday + home-card states. Repro with consented
  account, anonymized fixture, parser fix + regression test.
  - 2026-09-23: Monday-table parsing locked in with
    `test/fixtures/timetable_monday_variant.html` + regression test
    (day/date asserted). Live repro with consented account still pending;
    no credentials in repo.
  - 2026-09-23 VERIFIED LIVE (emulator, Sep-20 debug build, consented ZX
    account; creds via adb only, never in repo): fresh sync → timetable ok
    (82 entries, MONDAY 48 — biggest day), Monday tab renders 7 classes,
    home Today card updates correctly. NO parser bug. User symptoms =
    stale cache (older builds predate the feature) + stalled syncs (the
    F2 problem). Measured on fast net: attendance 5.3s, marks 6.0s,
    seating 12.6s FAILED content_not_ready, results 13.3s FAILED
    content_not_ready — content waits dominate; on college wifi these
    balloon past the 90s budget. Seating/results waits are F3 candidates.
- [x] F2 (P1): Refresh resilience — per-section timeout that records
  `sync_section{timeout}` and continues with cached data.
  - 2026-09-23: landed — `PortalScraper._readPage` caps every page read at
    40s (bridge calls have no timeout of their own) and maps the stall to
    `failure_reason: 'timeout'`; later sections still run. Hung-page test
    included. 40s covers worst-legitimate ~27s; retune from analytics p90.
- [ ] F3 (P2): Refresh speed from measured numbers (waits/session reuse).
  Depends on F2 and the D3 timing query.
  - 2026-09-23 (Codex console pass, `/tmp/codex-analytics.md`): standard GA
    reports can't slice custom params — durations/splits unavailable; need
    a free-form exploration (median/avg/max; GA4 has no p90). `sync_finished`
    flowing (2495 events/28d) but `refresh_finished` absent from listed
    events — investigate naming/thresholding. Retention 68.2% reconfirmed;
    crash-free 99.4% (Aug 26–Sep 22).
  - 2026-09-23 round 2: root cause found — the GA4 property has ZERO custom
    definitions registered, so section/sync_mode/outcome/duration_ms are
    unqueryable. Fix is console-side registration (reporting-only, no code);
    applies to future data only, so per-section history is unrecoverable.
    `refresh_finished` still unverified (no realtime check performed).
  - 2026-09-23 Task 1 DONE: all 7 dimensions + duration_ms metric
    registered and verified in-console. Data accrues from Sep 23 onward
    only. Task 2 queued: build the D3 exploration + realtime
    `refresh_finished` check.
  - Result 2: exploration shows no data — checked window predates accrual;
    aggregates incomplete. Re-read earliest Sep 30. `refresh_finished`
    still unverified (no test device). Task 3 queued for the realtime
    check.
  - 2026-09-23: loop PARKED (mailbox STOPPED, watcher cron deleted) — no
    device available. Resume triggers: (1) a test-device refresh session
    for Task 3; (2) Sep 30+ for the per-section exploration re-read.
  - 2026-09-23: loop RE-ARMED (mailbox RUNNING, watcher 98b52c1a) — live
    refresh being arranged for Task 3's realtime check.
  - 2026-09-23: 1.1.5 scope set — frequent users first (expedited rollout:
    internal → 50% → 100% with short holds; changes are additive with
    Remote Config kill-switches), higher-sem syllabus refresh REQUIRED via
    Task 5 (ET/ISE/CSE priority). Loop RUNNING, watcher d530ebbc.
  - Result 5 (partial): IQAC host resets in all browsers — zero verified
    links. One UNVERIFIED candidate: ETE 3-4sem 2023-24 (indexed content
    matches, load unconfirmed — NOT for use yet). Lead: msrit.edu CSE
    dept page exposes a 2026-27 PDF. Task 6 queued (msrit.edu dept pages
    only, skip IQAC).
  - Result 6 DONE: 5 links content-verified (CSE 3-4/5-6, ISE 2nd/3rd/4th
    yr 2026-27) + 4 load-verified (ET 3-4/5-6/7-8 sept-2026, CSE 7-8
    2026-27) — all 9 swapped into dummy_data 2026-09-23 (my load-check:
    HTTP 200 PDFs). Task 7 queued: remaining branches.
  - Result 7 DONE: 18 links content-verified (Civil/ME/EEE/EIE/Chemical/
    CyberSec × 3, all 2026-27) — swapped into dummy_data 2026-09-23.
    Still stale: Biotech, IEM, Medical Electronics, AI&ML, AI&DS,
    Architecture (dept pages expose only Google-Drive links). Task 8
    queued: check Drive link public-loadability.
  - 2026-09-23: all 18 also load-verified by me (HTTP 200 PDFs); analyze
    clean, full suite 84/84 green. Syllabus coverage now: 1st-yr 2026
    book + current schemes for CSE/ISE/ET/Civil/ME/EEE/EIE/Chemical/
    CyberSec (9 depts).
  - Result 8 DONE: 19 Drive PDFs public-loadable, Academic Year 2025-26.
    Applied 18 (Biotech/IEM/MedElectronics/AIML/AI&DS/Arch); EXCLUDED AIML
    VII&VIII link (cover says V&VI — mislabeled by MSRIT, stays stale).
    Syllabus now current for 15/16 branches. Loop parked (Sep 30 re-read
    pending).
  - 2026-09-23: all applied (incl. a mid-edit URL repair — path-only
    matches corrupted 13 rows, fixed and re-verified); analyze clean,
    full suite 84/84 green.
  - Result 3 (partial): Realtime shows sync_section (30) + sync_finished (5)
    flowing; `refresh_finished` absent — but no refresh occurred during the
    watch, so not a verified negative. A human refresh just completed;
    Task 4 queued for the immediate re-check.
  - Result 4 VERIFIED NEGATIVE: after a real refresh, `refresh_finished`
    absent from full Realtime list on two checks. App-side investigation
    opened (recordRefreshOutcome path).
  - Resolution 2026-09-23: NOT an app bug. `refresh_finished` fires only
    on the background-refresh path (`openPortalRefresh` covers all its
    branches); full-login syncs emit `login_flow_*` + `sync_*` but never
    `refresh_finished` — and Result 4's Realtime (5 login_flow_finished +
    5 sync_finished) is consistent with full logins. Dashboard rule:
    refresh health = `sync_finished{sync_mode=refresh}` (both paths set
    the flag); `refresh_finished` = background-refresh UX only. No code
    change. Loop parked again; per-section re-read due Sep 30+.
- [x] F4 (P2): Current syllabus URLs per branch (data-only).
  - 2026-09-23: added a verified-live "UG First Year (2026 Scheme)" row
    (`msrit.edu/pdf/First_year_syllabus_2026-RIT.pdf`, HTTP 200) to all 19
    BE departments; old rows kept. Higher-sem refresh still needs the IQAC
    index (unreachable from here) — follow-up with batch-aware links.
- [x] F5 (P3): Replace GDSC club card (data-only).
  - 2026-09-23: renamed to "GDG on Campus RIT" (Google's 2024 rename of
    GDSC); dead `gdscrit.tech` links replaced (linktree is live, discord
    invite kept). Logo asset unchanged.
  - 2026-09-23 (Codex browser pass): no RIT-specific GDG-chapter or ADG
    links page verifiable; nearest candidate is IEEE RIT via the official
    events hub `https://events.msrit.edu/` (live, but an events listing,
    not a club links page). A brand-new club card still needs the
    reporter's pick + link + logo.
- [x] F6 (P1): Attendance day-detail dropped the second slot. Day loop kept
  only `.first` per date (and present hid absent). 2026-09-23: fixed with
  `groupDaySlots`/`dayStatus` in
  `attendance_details_calender_version.dart` — agenda shows one appointment
  per slot, a day with any miss colors red. `test/attendance_day_slots_test`
  3/3 pass.

## 1.1.5 release (cutting 2026-09-23, version 1.1.5+13)

Rollout gates (expedited, frequent-users-first): internal testing →
production 50% (short hold, watch crash-free + refresh_finished/timeout
rate) → 100%. Kill-switches: `automatic_refresh_enabled`,
`portal_sync_enabled`. Fold in Result 8 Drive links first if it lands
before publish.
Blocked items stay out: replacement club, F3 tuning (Sep 30+ data).

## 1.1.5 release readiness (2026-09-23)

Analytics in build confirmed: A2 screen-class fix + A3 version/cohort/
platform params ship in 1.1.5; `APP_VERSION` is now stamped from pubspec
by `scripts/android_release_check.sh` (was hardcoded `1.1.4+12`), so
`release_cohort` survives the version bump. Full suite: 84/84 pass
(includes 5 A3 tests, Monday + hung-page scraper tests, 3 day-slot
tests). Note: one widget_test needed a phone-width surface after the
uncommitted adaptive-nav work (rail replaces bottom bar ≥600px) —
test-only fix, flag if restyling. Blocked items stay out: replacement
club, higher-sem syllabus (Task 5 running), F3 tuning (Sep 30+ data).

## Rules

- Prefer Muse for substantial implementation, investigation, testing, and
  recovery work.
- Keep phone behavior intact while validating tablet behavior separately.
- Test navigation transitions and accessibility scaling, not only initial render.
- Treat Firebase/Play/iOS account actions, publication, deletion, and signing as
  externally consequential and out of scope unless explicitly authorized.
