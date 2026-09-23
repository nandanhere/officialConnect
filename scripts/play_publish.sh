#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
readonly DEFAULT_AAB="$PROJECT_DIR/build/app/outputs/bundle/release/app-release.aab"

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

usage() {
  cat <<'EOF'
Usage:
  PLAY_PUBLISH_CONFIRM=YES PLAY_SERVICE_ACCOUNT_JSON=/abs/path/key.json \
    PLAY_TRACK=internal scripts/play_publish.sh [PATH_TO_VERIFIED_AAB]

Uploads a verified AAB through the Google Play Developer API. Safe by
default: refuses to run unless PLAY_PUBLISH_CONFIRM=YES, PLAY_TRACK is one
of internal, alpha, beta, production, and the AAB file exists. Production
also requires PLAY_ROLLOUT as an explicit decimal fraction from 0.01 to
1.0 (for example 0.10). The AAB defaults to
build/app/outputs/bundle/release/app-release.aab, the artifact produced by
scripts/android_release_check.sh --build-current.

Options:
  -h, --help    Show this help and exit.
EOF
}

[[ "${1:-}" == "-h" || "${1:-}" == "--help" ]] && { usage; exit 0; }
[[ $# -le 1 ]] || { usage >&2; die "expected at most one AAB path argument (got $#)."; }

[[ "${PLAY_PUBLISH_CONFIRM:-}" == "YES" ]] || \
  die 'Set PLAY_PUBLISH_CONFIRM=YES only after verifying the release.'
[[ -n "${PLAY_SERVICE_ACCOUNT_JSON:-}" ]] || \
  die 'Set PLAY_SERVICE_ACCOUNT_JSON to a local service-account JSON file.'
[[ -f "${PLAY_SERVICE_ACCOUNT_JSON:-}" ]] || \
  die 'PLAY_SERVICE_ACCOUNT_JSON does not point to a file.'
[[ -r "${PLAY_SERVICE_ACCOUNT_JSON:-}" ]] || \
  die 'PLAY_SERVICE_ACCOUNT_JSON is not readable.'
[[ -n "${PLAY_TRACK:-}" ]] || die 'Set PLAY_TRACK (internal, alpha, beta, or production).'
case "${PLAY_TRACK:-}" in
  internal|alpha|beta|production) ;;
  *) die "PLAY_TRACK must be one of: internal, alpha, beta, production (got: $PLAY_TRACK)." ;;
esac

if [[ "${PLAY_TRACK:-}" == "production" ]]; then
  rollout="${PLAY_ROLLOUT:-}"
  [[ -n "$rollout" ]] || die 'Production requires PLAY_ROLLOUT as an explicit decimal fraction from 0.01 to 1.0 (for example 0.10).'
  [[ "$rollout" =~ ^(0\.[0-9]+|1\.0*)$ ]] || \
    die "PLAY_ROLLOUT must be an explicit decimal fraction from 0.01 to 1.0 (got: $rollout)."
  [[ "$rollout" =~ ^0\.0+$ ]] && \
    die "PLAY_ROLLOUT must be an explicit decimal fraction from 0.01 to 1.0 (got: $rollout)."
  awk -v rollout="$rollout" 'BEGIN { exit !(rollout >= 0.01 && rollout <= 1.0) }' || \
    die "PLAY_ROLLOUT must be an explicit decimal fraction from 0.01 to 1.0 (got: $rollout)."
fi

aab_path="${1:-$DEFAULT_AAB}"
[[ -f "$aab_path" ]] || die "AAB not found: $aab_path"

cd "$PROJECT_DIR"
exec env BUNDLE_PATH="${BUNDLE_PATH:-vendor/bundle}" \
  bundle exec fastlane android publish "aab:$aab_path"
