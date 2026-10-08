# Update diagnostics

OfficialConnect records aggregate update health in Firebase Analytics. Events
must never contain student identifiers, dates of birth, verification values,
names, contact details, subjects, marks, URLs, cookies, page HTML, or raw error
messages.

## Events

`sync_section` records:

- section: profile, attendance, marks, results, fees, proctor, timetable,
  or seating
- outcome: ok, empty, partial, or error
- item_count, attempted_count, and failed_count
- duration_ms, duration_bucket, sync_mode, parser_version, and
  failure_reason (on failures)

`sync_finished` records the overall outcome, section count, duration, mode, and
parser version. Values are allow-listed and bounded before they reach the
analytics provider.

Users can disable this collection under **Settings > Help improve the app**.
The Android manifest explicitly removes advertising-ID permission.

## Firebase setup

The Android and iOS apps are registered in the existing `unofficialconnect`
Firebase project. To refresh or replace that configuration:

1. Sign in with Firebase CLI and select or create the OfficialConnect project.
2. Run `flutterfire configure` for Android and iOS.
3. Enable Google Analytics for that Firebase project.
4. Build release artifacts with the production markers
   (`OFFICIAL_CONNECT_DISTRIBUTION=production` and the pubspec
   `APP_VERSION`). The `Release` workflow passes both automatically; for a
   local manual build use `scripts/android_release_check.sh
   --build-current`, which does the same. Builds made without that marker
   are intentionally excluded from production Analytics and Crashlytics,
   even when compiled in release mode.
5. Verify events in Analytics DebugView using dummy data before release.
6. Complete the Play Data safety form and publish a privacy policy that covers
   update diagnostics and the local student-data cache.

The `distribution_channel=production` user property is attached to production
Analytics data. This makes release dashboards easier to audit without sending
student or device identifiers from application code.
