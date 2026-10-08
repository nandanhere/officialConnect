# Contributing to OfficialConnect

Thanks for helping out. The short version:

1. Fork, branch from `main`, open a PR. CI must be green; automated
   review may comment alongside humans.
2. Match the existing code style (`flutter analyze lib test` is the gate —
   zero issues).
3. Behavior changes need a regression test in `test/` that fails before the
   fix and passes after. Don't weaken existing tests to fit a change.
4. Never commit secrets: API keys, keystores, `key.properties`,
   `google-services.json`, `GoogleService-Info.plist`, tokens. If you slip,
   say so immediately so the secret can be rotated — don't just delete it
   in a follow-up commit.

## First build

You need Flutter stable (see `flutter-version` in `.github/workflows/ci.yml`
for the pinned version) and JDK 17 for Android builds.

```sh
flutter pub get
cp lib/firebase_options.dart.example lib/firebase_options.dart
# Android debug builds also need android/app/google-services.json in place:
# point it at your own Firebase test project (any valid structure builds;
# Firebase features stay inert without real keys).
flutter analyze lib test
flutter test
flutter build apk --debug
```

See `docs/PRIVACY.md` before touching anything that handles portal
data — probes and tests use aggregate shapes only, never personal content.

## Firebase config files (untracked, never commit)

`android/app/google-services.json`, `ios/Runner/GoogleService-Info.plist`,
and `lib/firebase_options.dart` carry keys and are intentionally untracked.
For `firebase_options.dart`, copy the `.example` file and fill in your own
test project (or run `flutterfire configure`); placeholder values compile
and run with Firebase features inert. Android debug builds need a
`google-services.json` in place — use a stub for your own test project.
Release builds restore the real config from maintainer secrets; never
commit any of these files.

App Check ships in monitor mode (unenforced). Debug builds use the debug
provider and print a debug token to logcat on first run — register it in
Firebase Console → App Check → Apps → the debug app entry. Never commit
or share debug tokens.
