# Android release readiness

The Android app targets and compiles against API 36, uses Java 17, AGP 9.1,
Gradle 9.3.1, Kotlin 2.4, and the Flutter-pinned NDK. API 35 theme resources
explicitly participate in Android's enforced edge-to-edge behavior. Insets
inside Flutter screens remain the responsibility of `SafeArea`, scrolling
layouts, and other Flutter-side layout code.

JNI libraries use modern, uncompressed packaging. The release checker verifies
that packaged ELF `LOAD` segments support 16 KB pages and, for APKs, asks
`zipalign` to verify 16 KB native-library alignment.

## Pre-release check

From the repository root:

```sh
scripts/android_release_check.sh --check
scripts/android_release_check.sh --build-current
```

The second command builds both the signed release AAB and universal APK, then
checks their native libraries. It requires the ignored local signing files
`android/key.properties` and `android/upload-keystore.jks` for a
distributable build. Never commit either file.

Before uploading, also confirm that:

- the upload-key reset is active in Play Console;
- the candidate version code is greater than every uploaded artifact;
- Play Console's pre-launch report has no new blocker;
- edge-to-edge layouts have been exercised on API 35 or newer;
- rollout monitoring and the staged-rollout stop criteria are ready.

## Emergency recovery bundle

> Stale: the pinned baseline commit `e0715ba` is absent from this history,
> and the version codes below predate the current release line. The owner
> must designate a fresh verified baseline (script `BASELINE_COMMIT`) and a
> minimum recovery version code above anything already uploaded before
> relying on this procedure.

The procedure builds old source as a new, higher version without touching
the current checkout:

```sh
mkdir -p outputs/recovery
scripts/android_release_check.sh --build-recovery \
  "$PWD/outputs/recovery/officialconnect-recovery-<version>.aab" <version-code>
```

The script verifies the commit, creates a temporary detached Git worktree,
keeps the baseline application source, and overlays the current verified
Android build harness inside that disposable worktree. This is necessary
because the baseline's old Gradle setup is no longer accepted by current
Flutter. The temporary build also raises several pinned plugin versions
whose old Android implementations reference embedding APIs removed from
current Flutter; the caller's dependency files are untouched.
It then copies local Android build/signing configuration, builds with the
supplied version code for 64-bit Android devices, verifies 16 KB ELF alignment,
copies out the AAB, and
removes the worktree. It does not switch branches, change tracked files, create
a tag, or push anything.

Always pass an explicit version code higher than every artifact already
uploaded to Play. Inspect the resulting AAB and upload it only after
deciding to invoke recovery; building it does not alter a Play rollout.
