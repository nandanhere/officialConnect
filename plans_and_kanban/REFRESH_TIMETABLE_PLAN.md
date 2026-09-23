# Refresh, timetable, and explore-content fix plan

Date: 2026-09-23. Source: user feedback (slow ~2 min refresh, sometimes
stuck updating; timetable broken — home card stale, Monday missing;
explore syllabus links stale 2021-22; GDSC defunct).

Status: planning only. No app code, releases, or account changes made.
ZX consented to testing with their portal account. Their credentials live
in chat only — never commit them, never log them, never paste them into
fixtures or docs. Any saved HTML fixture must be anonymized (no USN, names,
marks, session tokens).

## 1. What the code already tells us

- Refresh scrapes sections **sequentially** in one hidden WebView
  (`lib/Services/portal_scraper.dart`): dashboard → attendance → marks →
  proctor → fees → timetable → seating → results. Every section awaits
  `_navigateAndRead` with content-ready waits. On slow college wifi each
  page load stretches, so ~2 min refreshes and 90s+ stalls are expected,
  not anomalous.
- `openPortalRefresh` (`lib/Screens/login_screen/portal_refresh.dart`)
  has a **90s overall timeout** reporting `refresh_finished{timeout}`.
  There is **no per-section timeout**: one hung page blocks everything
  behind it ("stuck updating", and sections after the stall never run —
  which can also present as "timetable not updating").
- Timing telemetry **already exists**: `sync_section{duration_ms}` per
  section, `sync_finished{duration_ms}`, `refresh_finished{outcome}`.
  After Stage 1 these carry `app_version`/`release_cohort`/`platform`,
  so the analytics console can answer "where does refresh time go"
  with zero new code (D3 query below).
- Timetable parser (`_parseTimetable`) only accepts tables whose text
  contains `DAY dd-mm-yyyy` + a `TIME` column + a `COURSE CODE` column.
  A Monday table with a different header, or a portal week-window that
  omits Monday, yields zero Monday entries. The home card
  (`today_timetable_card.dart`) then shows a fallback line, which reads
  as "broken / not updating". No weekday-mapping bug is visible in
  `timetableFor` (ISO date equality) — this needs live data, not guessing.
- Explore content is static data: syllabus PDF links
  (`DummyData.syllabusLinks`, many 2021-22) and club cards
  (`dummy_data.dart`, incl. `GDSC-RIT`) in `lib/Providers/dummy_data.dart`.

## 2. Step 1 — Measure with existing analytics (no code, console access)

D3-refresh query (GA exploration or export), 28d, `release_cohort=1.1.4`:

- `sync_section` p50/p90 `duration_ms` per `section`, `sync_mode=refresh`.
- `sync_finished` outcome distribution + p90 `duration_ms`.
- `refresh_finished` outcome counts (success / partial / timeout / error).
- Correlate: do timeouts cluster on slow `duration_ms` sections, and does
  `timetable` show elevated `parse_error` / `content_not_ready` / `empty`?

Decision rule: if one section dominates p90, fix that section's waits;
if all sections are uniformly slow, the win is parallelism/timeouts, not
parser tweaks. If `refresh_finished=timeout` is common, the 90s budget is
structurally too small for sequential scraping on slow networks.

## 3. Step 2 — Repro with the consented ZX account (device/emulator)

1. Fresh login → record wall-clock per progress label ("Syncing …").
2. Refresh on slow-network simulation; note which label it stalls on.
3. Timetable screen: check whether Monday's table exists in the portal,
   what its header looks like, and what the parser kept vs skipped.
4. Save **anonymized** fixtures: Monday timetable table (if present),
   any table the parser skips. No personal data.
5. Confirm home-card behavior for: section error, section empty, refresh
   timeout mid-sequence (does the card explain, or look broken?).

## 4. Fixes (in order)

- F1 (P1) — Timetable Monday: extend `_parseTimetable`/fixtures for the
  observed Monday header (or empty-week handling), add regression tests
  in `portal_scraper_resilience_test.dart`; fix home-card copy for
  error/empty/timeout states so "no data" never looks "broken".
- F2 (P1) — Refresh resilience: per-section timeout (record
  `sync_section{timeout}` + continue with cached data) so one slow page
  can't starve later sections; keep the 90s overall budget or retune it
  from Step 1 numbers. Progress label per section already exists —
  keep it truthful while sections skip.
- F3 (P2) — Refresh speed: only after Step 1 numbers. Candidates:
  skip disabled sections earlier (already done per-section), shorten
  content waits for known-fast pages, reuse session harder. Not
  parallel WebViews (portal session is single-browser-context).
- F4 (P2) — Syllabus links: replace stale 2021-22 PDFs with current
  MSRIT syllabus URLs per branch. Needs URL research on the college
  site; data-only change in `dummy_data.dart`. Confirm which batch the
  reporter means (likely current 1st-year scheme).
- F5 (P3) — Clubs: verify GDSC/GDG-on-Campus status at RIT, then replace
  with the suggested active club (ask reporter for the name + link +
  logo). Data-only change in `dummy_data.dart` (+ image asset if needed).

## 5. Acceptance

- Refresh: p90 `sync_finished duration_ms` down or timeout rate down on
  the next 7d window, same cohort comparison; no new `unknown` outcomes.
- Timetable: Monday entries parse from a saved anonymized fixture;
  home card shows a truthful state for error/empty/timeout.
- Explore: syllabus links open current-scheme PDFs; no GDSC card.
- Privacy: no credentials, USN, or personal data in code, fixtures,
  analytics params, or planning docs.
