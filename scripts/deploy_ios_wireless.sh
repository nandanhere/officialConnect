#!/bin/sh
# Build OfficialConnect and install it on the paired iPhone — over Wi-Fi
# when possible, USB otherwise. Requires Flutter and full Xcode.
#
# Usage:
#   ./scripts/deploy_ios_wireless.sh [device-udid]
#
# First-time setup (once, with the phone plugged in):
#   1. Trust the Mac on the iPhone and enable Developer Mode
#      (Settings → Privacy & Security → Developer Mode).
#   2. Run this script once over USB; it pairs the phone for Wi-Fi use.
#   3. Afterwards the phone only needs to be on the same Wi-Fi network.
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
device_udid=${1:-00008140-001A48DE0A2A801C}
developer_dir=${DEVELOPER_DIR:-/Applications/Xcode.app/Contents/Developer}
export DEVELOPER_DIR="$developer_dir"

if [ ! -d "$developer_dir" ]; then
  echo "Full Xcode is required (not just Command Line Tools)." >&2
  exit 1
fi

cd "$project_dir"

echo "==> Checking device connection"
if ! xcrun devicectl device info details --device "$device_udid" >/dev/null 2>&1; then
  echo "==> Device not directly reachable; trying wireless pairing"
  if ! xcrun devicectl manage pair --device "$device_udid" --timeout 30; then
    echo "Could not reach the iPhone. Connect it with USB once, keep it on" >&2
    echo "the same Wi-Fi as this Mac, and make sure it is unlocked." >&2
    exit 1
  fi
fi

echo "==> Building release"
flutter build ios --release

echo "==> Installing on device"
xcrun devicectl device install app \
  --device "$device_udid" \
  build/ios/iphoneos/Runner.app

echo "==> Done. MSRIT Connect is up to date on the iPhone."
