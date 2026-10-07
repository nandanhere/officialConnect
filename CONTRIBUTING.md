# Contributing to OfficialConnect

Thanks for helping out. The short version:

1. Fork, branch from `main`, open a PR. CI must be green; CodeRabbit will
   review alongside humans.
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

See `README.md` ("Contributor Firebase setup") for the full story on config
files, and `docs/PRIVACY.md` before touching anything that handles portal
data — probes and tests use aggregate shapes only, never personal content.
