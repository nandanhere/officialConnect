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

Follow `docs/RELEASE_PROCESS.md` (release PR → tag → GitHub Release →
supervised Play submission). This file covers secrets setup only.
