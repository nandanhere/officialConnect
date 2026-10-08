# Privacy: what OfficialConnect does with your data

OfficialConnect is a student-built, unofficial viewer for the MSRIT student
portal. It is not affiliated with or endorsed by MSRIT. This document states
in plain language what leaves your device and what never does.

## What never leaves your device

- Your portal USN, password, date of birth, and everything you can see in
  the app (attendance, marks, fees, timetable, results). Scraping happens
  entirely on-device inside the app's browser session; scraped data is
  stored only in the app's local cache so it works offline.
- Your name or any contact details. The app has no account system and
  assigns no per-user identifier to analytics.

## What does leave your device (aggregate telemetry only)

If analytics collection is enabled, the app sends anonymous operational
events to the maintainer's Firebase project:

- Sync outcomes per section (e.g. attendance ok, 8s) with failure reasons
  when a section fails — no student data attached.
- Login flow outcomes (success / cancelled / timeout) without credentials.
- App version, platform, and distribution channel, used only to tell
  releases apart.
- Crash reports with the section the sync had reached — never with
  portal content.

Analytics event names and parameters are allowlisted in
`lib/Services/sync_diagnostics.dart`; anything not on the list is dropped
before sending. Google Analytics retains this data for at most 14 months.

## Builds that send nothing

Only production-marked release builds send telemetry — the `Release`
workflow and `scripts/android_release_check.sh --build-current` both set
the production marker. Developer and contributor builds collect nothing:
analytics collection is fail-closed and defaults to off.

## Your control

You can disable analytics and crash reporting at any time in the app's
settings. Disabling discards queued events; the app works fully offline
after your last sync regardless.

## Questions

Open a GitHub issue. If you are MSRIT staff reviewing this app: the
repository, this document, and the allowlist above are the complete
account of data handling — there is no server component and no database
of student records anywhere in this project.
