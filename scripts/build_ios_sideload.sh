#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
# Resolve to an absolute path: the packaging step runs inside a temp dir.
output_dir=$(mkdir -p "${1:-"$project_dir/outputs"}" && CDPATH= cd -- "${1:-"$project_dir/outputs"}" && pwd)
developer_dir=${DEVELOPER_DIR:-/Applications/Xcode.app/Contents/Developer}

if [ ! -d "$developer_dir" ]; then
  echo "Xcode is required to build the iOS package." >&2
  exit 1
fi

mkdir -p "$output_dir"
cd "$project_dir"
DEVELOPER_DIR="$developer_dir" flutter pub get
DEVELOPER_DIR="$developer_dir" flutter build ios --release --no-codesign

package_dir=$(mktemp -d /tmp/officialconnect-ios.XXXXXX)
trap 'rm -rf "$package_dir"' EXIT INT TERM
mkdir -p "$package_dir/Payload"
cp -R "$project_dir/build/ios/iphoneos/Runner.app" "$package_dir/Payload/"

rm -f "$output_dir/OfficialConnect-unsigned.ipa"
(cd "$package_dir" && /usr/bin/ditto -c -k --sequesterRsrc --keepParent Payload \
  "$output_dir/OfficialConnect-unsigned.ipa")

echo "Created $output_dir/OfficialConnect-unsigned.ipa"
