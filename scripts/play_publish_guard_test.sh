#!/usr/bin/env bash
# Non-publishing guard-path tests for scripts/play_publish.sh and the
# release_status/rollout logic in fastlane/Fastfile.
#
# Nothing here contacts Google Play: every case either exits in the
# wrapper's pre-upload guards or, for the one valid invocation, reaches a
# stub `bundle` on PATH that records the call and exits 99.
set -u

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
readonly PUBLISH="$SCRIPT_DIR/play_publish.sh"

pass=0
fail=0

check() { # name expected_exit expected_pattern... -- env... -- args...
  local name="$1" expected="$2" pattern="$3"
  shift 3
  local env_assignments=("PATH=$STUB_BIN:$PATH") args=() in_args=0 token
  for token in "$@"; do
    if [[ "$token" == "--" ]]; then
      in_args=1
    elif (( in_args == 0 )); then
      env_assignments+=("$token")
    else
      args+=("$token")
    fi
  done
  local output status
  output="$(env "${env_assignments[@]}" bash "$PUBLISH" "${args[@]}" 2>&1)"
  status=$?
  if (( status == expected )) && grep -qF "$pattern" <<<"$output"; then
    pass=$((pass + 1))
    printf 'PASS: %s\n' "$name"
  else
    fail=$((fail + 1))
    printf 'FAIL: %s (exit %s, want %s)\n%s\n' "$name" "$status" "$expected" "$output"
  fi
}

STUB_BIN="$(mktemp -d "${TMPDIR:-/tmp}/play-guard-stub.XXXXXX")"
trap 'rm -rf "$STUB_BIN" "$FIXTURES"' EXIT
cat >"$STUB_BIN/bundle" <<'EOF'
#!/usr/bin/env bash
echo "STUB-BUNDLE-REACHED: $*"
exit 99
EOF
chmod +x "$STUB_BIN/bundle"

FIXTURES="$(mktemp -d "${TMPDIR:-/tmp}/play-guard-fix.XXXXXX")"
touch "$FIXTURES/cred.json" "$FIXTURES/app.aab"

check "missing confirm refuses" 1 "PLAY_PUBLISH_CONFIRM" \
  "PLAY_SERVICE_ACCOUNT_JSON=$FIXTURES/cred.json" "PLAY_TRACK=internal" -- "$FIXTURES/app.aab"
check "missing credential refuses" 1 "PLAY_SERVICE_ACCOUNT_JSON" \
  "PLAY_PUBLISH_CONFIRM=YES" "PLAY_TRACK=internal" -- "$FIXTURES/app.aab"
check "bogus track refuses before upload" 1 "PLAY_TRACK must be one of" \
  "PLAY_PUBLISH_CONFIRM=YES" "PLAY_SERVICE_ACCOUNT_JSON=$FIXTURES/cred.json" "PLAY_TRACK=bogus" -- "$FIXTURES/app.aab"
check "production without rollout refuses" 1 "PLAY_ROLLOUT" \
  "PLAY_PUBLISH_CONFIRM=YES" "PLAY_SERVICE_ACCOUNT_JSON=$FIXTURES/cred.json" "PLAY_TRACK=production" -- "$FIXTURES/app.aab"
for bad in 0.5xyz 0.10foo abc 50% 0 0.001 2 0.00 " 0.5" ""; do
  check "production rollout '$bad' refuses" 1 "PLAY_ROLLOUT" \
    "PLAY_PUBLISH_CONFIRM=YES" "PLAY_SERVICE_ACCOUNT_JSON=$FIXTURES/cred.json" "PLAY_TRACK=production" "PLAY_ROLLOUT=$bad" -- "$FIXTURES/app.aab"
done
check "missing AAB refuses" 1 "AAB not found" \
  "PLAY_PUBLISH_CONFIRM=YES" "PLAY_SERVICE_ACCOUNT_JSON=$FIXTURES/cred.json" "PLAY_TRACK=internal" -- "$FIXTURES/nope.aab"
check "help exits zero" 0 "Usage" \
  -- "--help"
check "valid internal reaches bundler only" 99 "STUB-BUNDLE-REACHED" \
  "PLAY_PUBLISH_CONFIRM=YES" "PLAY_SERVICE_ACCOUNT_JSON=$FIXTURES/cred.json" "PLAY_TRACK=internal" -- "$FIXTURES/app.aab"
check "valid production fraction reaches bundler only" 99 "STUB-BUNDLE-REACHED" \
  "PLAY_PUBLISH_CONFIRM=YES" "PLAY_SERVICE_ACCOUNT_JSON=$FIXTURES/cred.json" "PLAY_TRACK=production" "PLAY_ROLLOUT=0.10" -- "$FIXTURES/app.aab"

# Fastfile rollout logic mirror: strict shape, no silent to_f coercion.
ruby -e '
valid = ->(r) { r && r.match?(/\A(?:0\.[0-9]+|1\.0+)\z/) && !r.match?(/\A0\.0+\z/) && r.to_f.between?(0.01, 1.0) }
good = %w[0.01 0.10 0.5 1.0 1.00]
bad = ["0.5xyz", "0.10foo", "abc", "50%", "0", "2", "0.00", " 0.5", "", "1", nil]
ok = good.all? { |r| valid.(r) } && bad.none? { |r| valid.(r) }
puts(ok ? "PASS: Fastfile rollout predicate" : "FAIL: Fastfile rollout predicate")
exit(ok ? 0 : 1)
' && pass=$((pass + 1)) || fail=$((fail + 1))

printf '\n%s passed, %s failed\n' "$pass" "$fail"
(( fail == 0 ))
