# Release Secrets (maintainers only)

The `release.yml` pipeline restores signing and Firebase config from these
seven repository secrets (Settings → Secrets and variables → Actions).
Set them once from the machine that holds the real files — values never
belong in chat, issues, or the repo:

| Secret | Value |
|---|---|
| `ANDROID_KEYSTORE_BASE64` | `base64 -i android/upload-keystore.jks` (single line) |
| `KEYSTORE_PASSWORD` | `storePassword` from `android/key.properties` |
| `KEY_PASSWORD` | `keyPassword` from `android/key.properties` |
| `KEY_ALIAS` | `keyAlias` from `android/key.properties` |
| `GOOGLE_SERVICES_JSON` | Contents of `android/app/google-services.json` |
| `GOOGLE_SERVICE_INFO_PLIST` | Contents of `ios/Runner/GoogleService-Info.plist` |
| `FIREBASE_OPTIONS_DART` | Contents of `lib/firebase_options.dart` |

With the GitHub CLI, from the repo root on that machine:

```sh
gh secret set ANDROID_KEYSTORE_BASE64 < <(base64 -i android/upload-keystore.jks | tr -d '\n')
gh secret set KEYSTORE_PASSWORD        # paste when prompted (same for KEY_PASSWORD, KEY_ALIAS)
gh secret set GOOGLE_SERVICES_JSON < android/app/google-services.json
gh secret set GOOGLE_SERVICE_INFO_PLIST < ios/Runner/GoogleService-Info.plist
gh secret set FIREBASE_OPTIONS_DART < lib/firebase_options.dart
```

## Releasing

1. Bump `version:` in `pubspec.yaml`, commit, push to `main`.
2. Tag exactly that version: `git tag v1.2.3+4 && git push origin v1.2.3+4`.
3. The pipeline verifies the tag matches pubspec, runs tests, builds the
   signed AAB + APK, and publishes a GitHub Release with both attached
   plus SHA-256 checksums.
4. To validate without publishing: Actions → Release → Run workflow
   (dry run — artifacts land on the workflow run, no Release is made).

Play uploads stay manual for now (see `docs/PLAY_API_RELEASES.md`).
