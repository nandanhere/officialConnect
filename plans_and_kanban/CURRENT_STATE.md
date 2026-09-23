# OfficialConnect current state

Last carried forward: 2026-09-21

Source task: `Set up officialConnect locally`

Referenced task ID: `01a07b7d-c131-7152-bf1a-b33624fcf17e`

## Repository and app

- Canonical checkout: `/Users/nandanherekar/cd/projects/officialConnect`
- Flutter app version: `1.1.4+12`
- Firebase project: `unofficialconnect`
- Android and iOS identifier: `com.nandan.msritconnect`
- Local-only test account: `DUMMY`; never use real student data for emulator testing.

## Completed and evidenced

- Firebase configuration was generated for Android and iOS.
- Android debug APK was built successfully.
- Android target/compile SDK inspection reported SDK 36.
- Android manifest inspection reported no advertising-ID permission.
- Phone navigation retains the five destinations in `BottomNavigationBar`.
- Tablet-width layouts use a labelled `NavigationRail` from 600px upward.
- Tablet content is constrained to 900px and receives the post-navigation width
  through `MediaQuery` so existing screens size correctly.
- Adaptive navigation tests cover phone/tablet rendering, selection, and 200%
  text scaling; the focused suite passed.
- Focused analysis and `git diff --check` passed in the source task.
- A guarded Fastlane Play API workflow exists in `fastlane/Fastfile`,
  `scripts/play_publish.sh`, and `docs/PLAY_API_RELEASES.md`; it intentionally
  stops without release credentials and explicit confirmation.

## Current blocker

- The project version is `1.1.4+12`.
- The existing IPA and ZIP are stale: embedded version `1.1.0+7`, archive
  `outputs/OfficialConnect-iOS-Sideload-1.1.0.zip`.
- The current host uses `/Library/Developer/CommandLineTools`; `xcodebuild`
  therefore cannot build a current iOS IPA.
- No version-matched sideload ZIP was created in Downloads. Do not rename or
  repackage the stale artifact.

## Analytics baseline (live observations, 2026-09-21)

Window: GA/Firebase overview, last 28 days Aug 24–Sep 20, 2026; engagement
figures are 7d values. This supersedes no older evidence; it is a new dated
live snapshot. Full plan: `plans_and_kanban/ANALYTICS_RELIABILITY_PLAN.md`.

- 2.2K active users (7d) / 2.3K (30d); 63K events, 2K key events (7d).
- Engagement: 3m 02s per active user, 1m 11s per session, 1.5 engaged
  sessions per active user.
- Stability: ~97.5% crash-free users; no stack-level diagnosis available in
  the analytics view (needs Crashlytics console access).
- Screens: default report collapses into `MainActivity` (~6.3K views);
  custom `app_screen_view` ~24K events is the current source of truth.
- `sync_section` ~11K; `login_flow_started` and `feature_opened` ~3.4K each.
- Retention ~68.2% at week one (mature columns only; later columns immature).
- Key events effectively all Android; iOS ~zero (consistent with the stale
  `1.1.0+7` iOS artifact, not a measured product gap).
- Prior signal to verify, not a current number: ~5% of login starts earlier
  lacked a recorded completion event.

## Analytics instrumentation update (2026-09-21, in-repo)

Stage 1 of ANALYTICS_RELIABILITY_PLAN.md is implemented; no console,
release, or account changes made.

- `lib/Services/firebase_sync_diagnostics.dart`: `logScreenView` now sends
  the bounded Flutter route as both `screenName` and `screenClass` (was a
  constant `'OfficialConnect'`), so the default Screens report can separate
  routes instead of collapsing into one row (kanban A2).
- `lib/Services/sync_diagnostics.dart`: new `DiagnosticsRelease` attaches
  allowlisted `app_version` / `release_cohort` / `platform` to every custom
  event and `app_version` to Crashlytics context. Defaults to `1.1.4+12`;
  compile-time `APP_VERSION` override and test hooks included; untrusted
  values fall back instead of leaking (kanban A3).
- `lib/Services/firebase_crash_reporting.dart`: `app_version` added to
  Crashlytics custom keys so non-fatals segment by release (kanban A3).
- `test/firebase_operations_test.dart`: exact-match assertions updated for
  the new params; 5 new tests (release context, cohort derivation, no-leak,
  opt-out suppression, crash-context version). Suite: 31/31 pass.
  `dart analyze` on the four touched files: no issues.
- Still blocked on console access: A1 funnel verification (D2/D3 numbers),
  D1–D5 explorations (C1), crash triage (C2), `1.1.4` baseline marking (C3),
  and the 7d post-fix re-measure (A4).

## Feedback fixes (2026-09-23, in-repo)

Plan: `plans_and_kanban/REFRESH_TIMETABLE_PLAN.md`, cards F1–F6 in `KANBAN.md`.

- F6 attendance day-detail (reported with screenshot): day loop kept only
  `.first` per date. Fixed with `groupDaySlots`/`dayStatus`; agenda shows
  every slot, any-miss days color red. `attendance_day_slots_test` 3/3.
- F2 refresh resilience: `PortalScraper._readPage` caps each page at 40s →
  `failure_reason: 'timeout'`, later sections still run (cached fallback).
  Hung-page + Monday-fixture tests in `portal_scraper_resilience_test`.
- F4 syllabus: "UG First Year (2026 Scheme)" row (verified live msrit.edu
  PDF) added to all 19 BE departments; old rows kept. Higher-sem links
  need the IQAC index (unreachable) — follow-up.
- F5 clubs: GDSC-RIT → "GDG on Campus RIT" (Google's 2024 rename); dead
  `gdscrit.tech` replaced (linktree verified live). New-club suggestion
  still needs a name + link from the reporter.
- F1 Monday TT + F3 speed: pending live repro with the consented account
  (credentials in chat only, never in repo) and the D3 timing query.
- Suites run 2026-09-23: resilience + session + firebase_operations +
  day-slots — 43/43 pass. `dart analyze` clean on touched files.

## Working-tree caution

The checkout contains many pre-existing user changes and untracked files,
including app features, tests, Fastlane files, and generated tooling. Preserve
all unrelated work. Do not reset, clean, delete, commit, push, publish, or
change credentials unless separately authorized.
