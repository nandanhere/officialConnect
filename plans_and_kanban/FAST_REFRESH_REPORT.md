# Authenticated background fetch and early attendance (2026-10-02)

User authorized implementing the same authenticated WebView as a background
fetch coordinator, prioritizing speed. No release, upload or publication was
performed. Muse could not start (402 billing verification); Codex implemented
and tested locally. Existing unrelated changes were preserved.

## Implemented

- Reuse the authenticated WebView's cookies for GET fetches of portal-emitted
  course URLs, preserving the exact href rather than appending a signature.
- Independently compare the first fetched course with ordinary navigation on
  each sync: full parsed counts, identity and date lists must match.
- After a successful probe, fetch at most two pages concurrently. Accept only
  expected course identity plus section structure and no login/password form.
  Ambiguous/rejected pages use serialized navigation after fetches settle.
- Fetches have a 3-second AbortController budget plus 1-second bridge guard.
- Persist and notify attendance immediately on refresh of an existing cache,
  before marks and slower optional sections. Preserve other cached sections;
  mark them pending, keep sync retryable, including after app restart. Initial
  uncached login still waits for the complete model.
- Avoid looking up a disposed widget's context after the 75-second flow limit;
  stop scheduling course reads once the flow is inactive.
- Resolve semester-result links by task=getResult, not the first com_history
  link (which may instead be seating).
- Do not claim all information is up to date while sections are pending or
  failed. No changes to login verification or CAPTCHA.

## Live emulator evidence

API35 arm64 AVD officialConnectApi35, using the app's existing saved-login flow.
No credentials were extracted, logged or written. Aggregate timings only.

- Final retained build (marks fast path removed): first attendance fetch
  matched navigation; remaining 9/9 fetches accepted. All 10 attendance
  courses persisted 2.403 seconds after scraping began, 8.642 seconds after
  refresh began including sign-in. Full refresh finished in 30.152 seconds;
  10 attendance, 10 marks and 10 fees entries, results still unavailable.
  No deactivated-context failure appeared in the aggregate test logs.

- Attendance-only fetch build: 10 attendance courses and 10 marks courses;
  attendance persisted 3.235 seconds after scraping began (8.190 seconds after
  refresh began). Full refresh including sign-in: 29.140 seconds.
- Subsequent combined probe runs: attendance persisted at 3.727 / 3.640 seconds
  after scrape began (9.016 / 8.400 seconds including sign-in). Full refresh:
  31.938 / 31.879 seconds. Attendance accepted 9/9 subsequent fetched pages in
  the instrumented run, in addition to the first navigation-verified page.
- Marks' first page matched normal navigation but subsequent identity checks
  accepted 0/9 pages in that run. All 10 courses remained available via normal
  fallback. Do not describe these runs as successful parallel marks scraping.
- Semester results still wait approximately 14 seconds then return no ready
  result table. Overall sync remains partial; this change does not resolve the
  portal's semester-results problem.
- Prior single-view sample was 31.6 / 35.5 / 32.8 seconds (33.3 average).
  Different-day uncontrolled observations are not a rigorous speed benchmark.
  The main verified gain is time-to-visible-attendance, not guaranteed total
  latency. No data from other accounts or production devices was tested.

## Validation and follow-up

Full Flutter suite: 103 tests passed. Focused tests cover first-page login
rejection, wrong-course rejection, max-two concurrency, navigation after
fetches settle, early delivery, cancellation, cache preservation and pending
restart behavior. Android debug APK built; targeted analyzer passed.

The whitespace-normalized marks-label retry also accepted 0/9 pages; full
refresh was 35.603 seconds with slower sign-in. The marks fast path was removed
from the retained implementation because the extra attempts added latency.
Marks and optional sections remain serialized. Only attendance uses parallel
fetch. Remaining: establish a trustworthy dashboard-to-marks identity mapping;
investigate result readiness/redirect independently. Do not loosen identity
checks merely to increase accepted-page counts. Build warnings about the
future Kotlin migration remain unrelated and unchanged.
