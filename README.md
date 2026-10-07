# Official Connect

[![CI](https://github.com/nandanhere/officialConnect/actions/workflows/ci.yml/badge.svg)](https://github.com/nandanhere/officialConnect/actions/workflows/ci.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

The unofficial student information system app for MSRIT students —
attendance, marks, timetable, fees, results, and exam seating from the
parent portal, in one fast on-device app.

## Getting started (contributors)

```sh
flutter pub get
cp lib/firebase_options.dart.example lib/firebase_options.dart
flutter analyze lib test
flutter test
flutter build apk --debug   # needs android/app/google-services.json, see below
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) before your first PR, and
[SECURITY.md](SECURITY.md) before reporting a vulnerability.

Releases are automatic: tagging `v<version>` (exactly the pubspec version)
builds signed artifacts and publishes a GitHub Release. Maintainers: see
[docs/RELEASE_SECRETS.md](docs/RELEASE_SECRETS.md) for the one-time secrets
setup. License: [GPL-3.0](LICENSE).

## Portal login integration notes

The official portal login form uses `username` plus three date selectors:

- `dd` uses values with a trailing space, such as `08 `.
- `mm` uses two-digit values, such as `12`.
- `yyyy` uses the four-digit year, such as `2000`.
- Changing `yyyy` invokes the portal `putdate()` JavaScript function, which generates the hidden password value.

The app-side WebView fills these controls and then continues through the portal's ordinary login and verification buttons. It must not fabricate or bypass any server-side CAPTCHA/token validation.

Login details are cached locally to suggest them on the next launch. Clearing the USN clears the saved login set. Future dates are rejected as stale/invalid cache values. The DOB picker must preserve the date selected by the user; opening the picker must not overwrite it with today's date.

### On-device scraper architecture

The app establishes the authenticated portal session in a WebView. During the ordinary successful path, the WebView stays mounted and active behind a native progress screen, so users see app-owned status messages rather than the portal UI. If the portal ever requires an interactive step, the error state offers an explicit **Open portal** fallback instead of silently failing.

The app scrapes directly inside the authenticated WebView. This preserves the portal's browser and network context, keeps credentials on the device, and stores only the parsed native-app JSON in the existing local cache. The scraper visits prerequisite authenticated pages before exam history and waits for page-specific content instead of fixed delays. The retired AWS Lambda scraper and proctor service are not part of the application architecture.

Measured on the API 35 Android emulator on 2026-09-08, the old flow took 50.1 seconds end-to-end. The optimized flow took 14.0 seconds for a repeat sync and 11.3 seconds with cookies cleared and the complete autofilled portal login. Internal instrumentation measured 2.5-3.9 seconds for scraping and 8.9-9.6 seconds from WebView creation through cache completion. These are diagnostic development measurements and will vary with portal and network latency.

### Examination results source

The **latest result** shortcuts are separate from the parent portal. They use the MSRIT examination results site (`exam.msrit.edu`) and must not be populated from cached parent-portal history.

The former server-side scraper contract is no longer valid: the old `/eresultseven/` route returns 404, the root page now represents the currently published regular cycle, and both the current regular page and the legacy supplementary page require a session-bound image security code. The app therefore keeps a hidden WebView for the examination-site session, fills the cached USN, displays only the site's security image in native UI, submits the user-entered code in that same session, parses the returned table, and renders native result cards. It caches a successful parsed result by USN and source; reopening is instant, while the refresh action deliberately requests a new live result.

Do not attempt to solve or bypass the examination site's security code. If upstream changes again, update the URLs, selectors, and HTML parser in `lib/Services/exam_result_scraper.dart` and keep the WebView/session boundary intact.

## Contributor Firebase setup

`android/app/google-services.json`, `ios/Runner/GoogleService-Info.plist`,
and `lib/firebase_options.dart` are intentionally untracked (see
`android/.gitignore`, `ios/.gitignore`, and `.gitignore`) — they carry keys
that must never be committed. For `firebase_options.dart`, copy
`lib/firebase_options.dart.example` and fill in your own test project (or
run `flutterfire configure`); placeholder values compile and run with
Firebase features inert. Debug builds need a `google-services.json` in
place: use a stub with your own test project, or ask a maintainer.
Release builds restore the real config from maintainer secrets (CI) or
before running `scripts/android_release_check.sh --build-current` (local);
never commit any of these files.

App Check ships in monitor mode (unenforced). Debug builds use the debug
provider and print a debug token to logcat on first run — register it in
Firebase Console → App Check → Apps → the debug app entry. Never commit or
ship debug tokens.
