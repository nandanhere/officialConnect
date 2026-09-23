# Play API release workflow

This repository can publish a verified Android App Bundle through the Google
Play Developer API. It removes the repeated browser upload step while keeping
the important safeguards: a release is built and checked locally, the intended
track is explicit, and an upload requires an unmistakable confirmation value.

## Sequence for every release

1. Review the code and run the app tests.
2. Build and verify the release artifact:

   ```sh
   scripts/android_release_check.sh --build-current
   ```

3. Check the current Play Console release and vitals. Do not create a competing
   Console edit while an API release is being prepared.
4. Upload the verified AAB with the command below. Internal testing is the
   recommended first destination; production requires an explicit fraction.
5. Confirm the release and its rollout state in Play Console after the API
   returns successfully. Keep the prior production artifact available for a
   recovery release.

## One-time owner setup

This needs to be done once in Google Cloud and Play Console by the account
owner. Do not put the downloaded JSON key in this repository.

1. Link the Play Console developer account to a Google Cloud project.
2. Enable the **Google Play Android Developer API** in that Cloud project.
3. Create a dedicated service account named for releases, download its JSON
   key to a private local path such as `secrets/play-release.json`, and keep
   that path ignored by Git.
4. In Play Console, invite that service account with the least permissions
   needed to manage releases for `com.nandan.msritconnect`. It should not get
   financial, user-data, or broad account-administration permissions.
5. Install the local release dependency once:

   ```sh
   BUNDLE_PATH=vendor/bundle bundle install
   ```

## Upload commands

Use an absolute path for the credential file. The wrapper refuses to do
anything unless `PLAY_PUBLISH_CONFIRM=YES` is set. With no argument it
uploads `build/app/outputs/bundle/release/app-release.aab`, the artifact
produced by `scripts/android_release_check.sh --build-current`; pass an
explicit AAB path only for a bundle you already verified with
`scripts/android_release_check.sh --check-artifact <path>`. Never rebuild
between verification and upload: upload the exact file that was checked.

```sh
export PLAY_SERVICE_ACCOUNT_JSON="$PWD/secrets/play-release.json"
export PLAY_TRACK=internal
export PLAY_PUBLISH_CONFIRM=YES
scripts/play_publish.sh
```

For a staged production release, set a fraction deliberately:

```sh
export PLAY_TRACK=production
export PLAY_ROLLOUT=0.10
export PLAY_PUBLISH_CONFIRM=YES
scripts/play_publish.sh
```

`PLAY_ROLLOUT` accepts an explicit decimal fraction from `0.01` through
`1.0` (for example `0.10`); values such as `0.5xyz`, `50%`, or an empty
string are rejected, never rounded or defaulted. A `1.0` rollout completes
the release; smaller fractions stay in progress. The script does not infer
the track or fraction, and it does not upload store listing text,
screenshots, or metadata. Those remain deliberate Console changes.

Local dependencies install to `vendor/bundle` (ignored by Git) via
`BUNDLE_PATH=vendor/bundle bundle install`, matching the wrapper default.
`Gemfile.lock` stays tracked for repeatable installs. Guard paths can be
exercised without publishing via `scripts/play_publish_guard_test.sh`.

## Rollback and safety

Stop a problematic rollout from the Play Console immediately, then use the
existing verified recovery-bundle procedure in `distribution/ANDROID_RELEASE.md`
if a replacement build is needed. Before any production upload, verify the
current upload-key and signing status in Play Console; older local notes may
not represent the current account state.

The Play Developer API uses transactional *edits*: an upload is not visible to
users until the API commits the edit. Avoid changing the same release in Play
Console while the command is running, because a Console change can invalidate
the API edit.
