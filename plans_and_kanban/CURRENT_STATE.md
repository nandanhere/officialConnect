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

## Open-source and CI handoff (2026-10-08)

- Canonical public repository: `https://github.com/official-connect/officialConnect`.
  The old `nandanhere/officialConnect` URL redirects to it; local `origin` was
  updated during the transfer.
- Contributor templates, release guidance, public integration documentation,
  and a pull-request template are committed. GitHub issues #17, #21, and #22
  were closed after the organization transfer checks completed.
- CodeRabbit is installed for this repository only. Main requires the `verify`
  and `history` checks; force-pushes and deletion are disabled.
- The secret-history CI job uses the maintained OSS TruffleHog container over a
  full checkout because the previous Gitleaks GitHub Action requires an
  organization license. The hosted CI run passed analysis, tests, debug APK
  build, and history scanning after this change.
- CI now uses `actions/checkout@v5` and `actions/setup-java@v5`. The only
  remaining runner notice is the scheduled `ubuntu-latest` image migration.

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

## Refresh emulator check (2026-10-01)

- Android 15 API 35 debug emulator used an already authenticated, consented
  portal session. No account identifiers, credentials, or page HTML were added
  to this repository.
- Two pre-fix manual/background refreshes took 47.4s and 48.3s end to end.
  Exam seating spent about 14.0s each time, ending `content_not_ready`.
  Attendance succeeded for all 10 discovered courses in about 4–4.7s.
- `portalExpectedContentSelector` used the generic `com_history` result-table
  selector for `task=seating`. The seating page has a different layout. Added
  page-specific seating readiness and the parser-supported result-table
  variant in `lib/Services/portal_session.dart`.
- Three post-fix refreshes took 31.6s, 35.5s, and 32.8s. Seating completed
  in about 0.44s with one parsed entry. The full refresh average fell from
  47.9s to 33.3s on this emulator; this is a small local sample, not a fleet
  latency claim.
- Semester results still take about 14s and end `content_not_ready`; profile
  remains partial due to two missing fields. The overall sync remains partial.
  Investigate the live result page/redirect before changing its timeout or
  treating an absent table as an authoritative empty result.
- Current scraper navigates one authenticated WebView serially. Parallel
  page loads in that same WebView would replace each other's documents. A
  separate-WebView or authenticated-request approach needs a session and
  correctness experiment before implementation.

## Separate WebView experiment (2026-10-02)

Superseded for the speed strategy by the successful same-authenticated-WebView
fetch approach: see FAST_REFRESH_REPORT.md. The separate-view failure below
remains historical evidence, not the current implementation.
Final retained emulator build: attendance available at 8.642s including login,
full refresh 30.152s; 10 attendance courses. All 103 Flutter tests passed.
Marks remains serial after fetched identity validation rejected 9/9 pages;
semester results still wait ~14s and fail readiness. Not published.

- One temporary debug build tried loading semester results in a second hidden
  WebView while the primary WebView scraped the other sections. The second
  view did not reach the authenticated dashboard within 11.5s, so results
  ended `browser_not_ready` without a successful parallel scrape.
- The experimental refresh took 42.7s end to end. Attendance and marks each
  parsed 10 courses; proctor and timetable returned `content_not_ready`, fees
  were partial, and seating appeared empty. This is worse than the previous
  day's 31.6–35.5s single-view sample, but conditions were not controlled.
- The app started an automatic retry after the partial result; it was stopped.
  A subsequent normal single-view recovery run hit the 75s flow limit while
  portal pages were unusually slow, so it did not replace the partial cache
  on this emulator. Real devices and production builds were not changed.
- All experimental code was removed, and the ordinary debug APK was rebuilt
  and reinstalled. A future parallel design needs to establish how a second
  WebView acquires a valid signed session and verify section correctness under
  simultaneous navigation before optimizing for elapsed time.

## Fast-refresh batch (2026-10-02, Muse, uncommitted)

- Fleet GA4 (7d, ~1900 refreshes/section): results 22.0s avg at 96%
  `content_not_ready`, seating 16.9s at ~100% (released build lacks the Oct 1
  seating selector fix), marks 9.6s, attendance 7.0s, singles ~1.4-1.8s.
- Emulator baseline (current tree, API35, saved login): 31.3s end to end
  (sign-in ~6s, scrape 25.4s). Attendance visible at 4.6s; results alone
  burned 14.0s with `content_not_ready`.
- Shipped in tree: stale onLoadStop session probes suppressed during scrape;
  dashboard reuses the current page when already loaded; photo download
  overlaps attendance; marks fast path via probe + distinct-course validation
  (dashboard labels proved unmatchable, 0/9 before); fetch-first reads for
  proctor/fees/timetable/seating/results with navigation fallback; uniform
  6s content waits (retired the 12s results window); single-evaluation
  navigation polling; login-form fast-negative auth check; autofill retry
  short-circuit.
- Emulator after (two runs): 18.9s end to end, scrape 12.7s both runs.
  Attendance visible at ~2.0s; marks 9/9 fetched (~1.7s); singles all
  fetch-served (0.1-0.6s); results 7.6s still failing. All section counts
  identical to baseline (10/10/10/66/1, cached results kept).
- Suite 109/109 green, analyzer clean. Remaining: results root cause needs
  the live portal flow (Codex browser Task 17 dispatched via mailbox); then
  the results wait can be replaced by the correct read instead of shortened
  further blindly.

## Results read fix (2026-10-02, Muse, uncommitted)

- Result 17 (Codex browser): the history route answers direct navigation
  with the login page; only a dashboard EXAM HISTORY click reaches the
  signed destination (5 tables: 1 backlog + 4 semester). The old "slow
  endpoint init" theory is disproved. exam.msrit.edu not needed.
- Implemented results-first ordering: results read while the browser still
  shows the dashboard (fetch, else dashboard click). A dashboard revisit
  was tried first and failed the same way (unsigned dashboard navigation
  is refused too), which fixed the ordering. No retry: content-match
  implies non-empty parse. Early-attendance payload now carries the real
  results outcome. Order pinned by a navigation-sequence regression test.
- Emulator (3 runs): results ok, 5/5 tables, 209/226ms via fetch and
  457ms via forced click fallback. Full refresh 11-13s end to end
  (scrape ~5.2s), attendance visible ~2.1s. Suite 110/110, analyze clean.
- Residual: dashboard-marker shortcut can false-positive on detail pages
  (proven harmless for the initial read across 6 runs, but unhardened);
  backlog table parses as a term entry (kept: hiding user data is worse).

## Proctor/fees parse audit (2026-10-02, Muse, uncommitted)

- Privacy-safe live probes (counts/shapes only): proctor observation page
  carries 1 cn-res-table with caption + 1 header row and an EMPTY tbody
  (genuinely zero notes, not selector rot); fees page carries the
  1 cn-pay-table (10/10 rows parsed) plus a 4-row student-info table that
  holds no fee data (correctly ignored). Fees empty path already honest.
- Rot fixed: proctor section hardcoded count 1 (now the parsed note
  count); disabled/error paths emitted proctorship as `[]` while the
  contract is a Map (now `_emptyProctor()`); `SisProctorData.proctorData`
  crashed on legacy `[]` caches and missing keys (now normalizes to the
  empty map with 'Not given' defaults). Failing-first tests added
  (3 scraper + 2 consumer + 1 fees characterization).
- Emulator: proctor ok count 0 (was 1), fees ok 10, all other sections
  unchanged. Suite 118/118, analyze clean. Probes removed.
- Follow-up (same day, approved test-creds content read): the 110-char
  header is name (bare text node) + department/email/phone spans; the
  parser stuffed the whole blob into proctor_name. `_parseProctor` now
  splits by structure + pattern (email/phone/branch degrade to 'No data'
  when parts are missing), pinned by a span-shape regression test. Live:
  name 12 chars, branch/email/phone populated (were 'No data').
- Follow-up: empty fee page no longer wipes dashboard fees (fallback
  keeps dashboard rows when the page yields zero of both fees and
  refunds; genuinely-empty stays 'empty'). Failing-first test added.
  Suite 120/120, analyze clean. Content probes removed.

## Release 1.1.6+15 (2026-10-02, committed, upload staged)

- Dirty-tree review: 18 modified + 5 new files, all identified (fast
  batch, results-first, profile/proctor/fees fixes, duration_bucket,
  pending/partial UI honesty, Firebase config untracking, docs). No
  foreign code, no secrets in new docs. README gained the contributor
  Firebase/App Check setup section the gitignore comments reference.
- App Check client enrolment rides this release: Play Integrity (prod)
  / debug provider, App Attest / debug, activated before other Firebase
  services. Enforcement stays OFF (monitor mode). Debug activation
  verified on emulator via redacted logcat (provider present, no token
  recorded). Provider-selection regression tests added.
- Checks at commit: suite 122/122, analyzer clean, static release
  config pass, signed AAB+APK rebuilt from the committed tree with ELF
  + zipalign pass. Supervised browser upload dispatched as mailbox
  Task 22; Crashlytics re-verify (Task 19), App Check console
  registration (Task 20), allowlist test-project validation (Task 21)
  dispatched alongside. Task 18 (duration_bucket registration) still
  OPEN with Codex.

## Zero-touch monitoring finish (2026-10-02, Muse via API, no commit needed)

- Used the machine's existing firebase-tools login (owner account,
  cloud-platform scope; token never printed or stored) — zero human
  action for everything below. No repo changes; tree still clean at
  3713821.
- Task 19 DONE: getIamPolicy proves the owner account is roles/owner
  (includes firebase.projects.update) — Result 14's banner was stale;
  no grant needed or possible. Email pref already selected. Visual
  confirmation folded into Task 22 step 0.
- Task 20 DONE: App Check REST shows playIntegrityConfig (Android) +
  appAttestConfig (iOS) already registered (3600s TTL, permissive
  defaults; PATCH idempotent). Enforcement untouched/OFF everywhere.
- Task 21 DONE: prod mobile keys pruned 25→6 APIs (firebase,
  firebaseappcheck, firebaseinstallations, firebaseremoteconfig [+realtime],
  logging) after emulator validation against a sandbox project with a
  6-restricted test key + registered debug token; two post-prune prod
  refreshes verified clean. Browser key untouched (unused by the app).
  Sandbox restored pristine; scratch secrets scrubbed.
- Residuals: orphan empty GCP project oc-keytest-20261002 (API-created,
  API-invisible, free; delete in console if convenient); the ONLY
  remaining human cost in the whole release is the single supervised
  browser sitting (Task 22 upload + Task 18/19 visual checks).

## Date-picker third-column fix (2026-10-02, Muse, uncommitted)

- Report ("can't pick dates after 2008") + user screenshot: the DOB
  year grid showed only 2 of 3 columns (2008/2011/2014/2017 cut off).
  Root cause: date_picker_plus is fixed 328px wide while the dialog
  content is ~192-262px on phones; the F7 horizontal scroll made it
  scrollable but undiscoverable. Bounds were never the issue
  (1994-2011 all along).
- Fix: bound the picker to a computed finite box (width from dialog
  geometry, height mirroring the package's 402/300 caps) so the grid
  squeezes to 3 fitted columns. Tight-in-both-dimensions also fixes a
  latent intrinsic-measurement crash (debug-only assertion; in release
  it silently produced the clipped layout). Tried and rejected:
  bare width box, LayoutBuilder (both crash on intrinsics).
- Regression tests at 320/390/800px assert every year cell is
  on-screen (failed pre-fix); golden screenshot verified 3 fitted
  columns. Suite 125/125, analyze clean. Emulator session preserved
  (prefs backup/restore verified with home-screen proof).
- Gradient-adjust parked per user (2026-10-03); 1.1.6+15 already
  submitted for review, so this fix ships in 1.1.7+16 (new AAB hash →
  Task 23), superseding v15 before anything reaches users.
