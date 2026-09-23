# Muse handoff: OfficialConnect continuation

## Objective

Continue OfficialConnect from the current checkout, using the kanban and state
files in this folder. Resolve the iOS sideload blocker if the local toolchain
now permits it; otherwise verify and document the exact blocker. Preserve the
already completed responsive navigation and Firebase work.

## Workspace

`/Users/nandanherekar/cd/projects/officialConnect`

Read these first:

- `plans_and_kanban/CURRENT_STATE.md`
- `plans_and_kanban/KANBAN.md`
- `plans_and_kanban/README.md`

## Required behavior

1. Inspect current git state, Flutter version, Xcode selection, and existing
   artifacts before making changes.
2. Preserve unrelated dirty changes and untracked files. Never use reset/clean
   or delete user work.
3. Keep the five-item phone navigation unchanged and keep the real tablet
   treatment width-aware.
4. If full Xcode is available, build an unsigned iOS artifact, inspect the
   embedded plist, and only then create a ZIP labelled `1.1.4` with build `12`,
   checksum, and accurate sideload instructions in Downloads.
5. If full Xcode is unavailable, do not fabricate, rename, or copy the stale
   `1.1.0+7` IPA. Update the kanban blocker with evidence.
6. Run proportionate validation and perform a final self-review. Report exact
   commands and results, including unavailable dependencies or tools.

## Out of scope

- No Apple signing, provisioning, Apple account changes, credentials, cloud
  publication, Play Store publication, deletion, commit, or push.
- No use of real student data.

## Completion report format

Return only a compact report containing: outcome, changed artifacts, validation
status, iOS package path/checksum or blocker, and residual risks.
