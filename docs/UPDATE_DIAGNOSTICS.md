# Update diagnostics

OfficialConnect records aggregate update health in Firebase Analytics. Events
must never contain student identifiers, dates of birth, verification values,
names, contact details, subjects, marks, URLs, cookies, page HTML, or raw error
messages.

## Events

`sync_section` records:

- section: profile, attendance, marks, results, fees, or proctor
- outcome: ok, empty, partial, or error
- item_count, attempted_count, and failed_count
- duration_ms, sync_mode, and parser_version

`sync_finished` records the overall outcome, section count, duration, mode, and
parser version. Values are allow-listed and bounded before they reach the
analytics provider.

Users can disable this collection under **Settings > Help improve updates**.
The Android manifest explicitly removes advertising-ID permission.

## Firebase setup

The Android and iOS apps are registered in the existing `unofficialconnect`
Firebase project. To refresh or replace that configuration:

1. Sign in with Firebase CLI and select or create the OfficialConnect project.
2. Run `flutterfire configure` for Android and iOS.
3. Enable Google Analytics for that Firebase project.
4. Build the app normally; no Firebase build flag is required.
5. Verify events in Analytics DebugView using dummy data before release.
6. Complete the Play Data safety form and publish a privacy policy that covers
   update diagnostics and the local student-data cache.
