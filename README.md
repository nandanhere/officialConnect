# Official Connect

[![CI](https://github.com/nandanhere/officialConnect/actions/workflows/ci.yml/badge.svg)](https://github.com/nandanhere/officialConnect/actions/workflows/ci.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

The unofficial student information system app for MSRIT students —
attendance, marks, timetable, fees, results, and exam seating from the
parent portal, in one fast on-device app. Student-built; not affiliated
with or endorsed by MSRIT.

## Features

- Attendance, CIE marks, timetable, fees, semester results, exam seating
- Latest regular/supplementary results from the examination site
- Cache-first offline access after your last sync
- On-device portal session — credentials never leave your phone
- Aggregate-only, opt-out diagnostics (no student data leaves the device)

## Get the app

- Android: when maintainers cut a release, signed APK/AAB artifacts land
  on the repository's GitHub Releases page (see
  [docs/RELEASE_PROCESS.md](docs/RELEASE_PROCESS.md)). A GitHub Release
  is not a store publication.
- iPhone: self-signed sideload — see
  [distribution/IOS_SIDELOAD.md](distribution/IOS_SIDELOAD.md).
- Or build from source below.

## Contribute

```sh
flutter pub get
cp lib/firebase_options.dart.example lib/firebase_options.dart
flutter analyze lib test
flutter test
flutter build apk --debug   # needs android/app/google-services.json, see CONTRIBUTING
```

You need Flutter stable (pinned `flutter-version` in
`.github/workflows/ci.yml`) and JDK 17. Read
[CONTRIBUTING.md](CONTRIBUTING.md) before your first PR,
[SECURITY.md](SECURITY.md) before reporting a vulnerability, and
[docs/PRIVACY.md](docs/PRIVACY.md) before touching portal data.

## Docs

| Doc | For |
|---|---|
| [CONTRIBUTING.md](CONTRIBUTING.md) | First build, PR rules, Firebase stubs |
| [docs/PRIVACY.md](docs/PRIVACY.md) | What leaves your device (aggregate telemetry only) |
| [docs/PORTAL_INTEGRATION.md](docs/PORTAL_INTEGRATION.md) | Portal login, scraper, exam-results notes |
| [docs/OFFLINE_BEHAVIOR.md](docs/OFFLINE_BEHAVIOR.md) | Cache-first behavior and limits |
| [docs/UPDATE_DIAGNOSTICS.md](docs/UPDATE_DIAGNOSTICS.md) | Analytics event contract |
| [docs/RELEASE_PROCESS.md](docs/RELEASE_PROCESS.md) | Maintainers: release PR → tag → GitHub Release → supervised store step |
| [distribution/ANDROID_RELEASE.md](distribution/ANDROID_RELEASE.md) | Maintainers: Android pre-release checks |
| [docs/PLAY_API_RELEASES.md](docs/PLAY_API_RELEASES.md) | Maintainers: guarded Play API upload |

Releases are tag-driven: tagging `v<version>` (exactly the pubspec
version) builds signed artifacts and publishes a GitHub Release.
Release tags and the Release workflow are maintainer-only.

License: [GPL-3.0](LICENSE).
