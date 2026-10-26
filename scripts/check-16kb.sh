#!/usr/bin/env bash
# Verify every native library in an APK is 16 KB page aligned:
# each LOAD segment of each .so must have Align >= 0x4000.
#
# Usage: scripts/check-16kb.sh <path/to/app.apk>
# Needs ANDROID_NDK_HOME (for llvm-readelf) or READELF pointing at a readelf.
#
# JNA's libjnidispatch.so is checked like everything else (open question OQ-J):
# if it fails, it is reported by name and the check fails. Do not filter it out.
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <apk>" >&2
  exit 2
fi
apk="$1"
if [[ ! -f "$apk" ]]; then
  echo "error: APK not found: $apk" >&2
  exit 2
fi

readelf="${READELF:-${ANDROID_NDK_HOME:-}/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-readelf}"
if [[ ! -x "$readelf" ]]; then
  echo "error: llvm-readelf not found at '$readelf' (set ANDROID_NDK_HOME or READELF)" >&2
  exit 2
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
unzip -q -o "$apk" -d "$tmp"

mapfile -t libs < <(find "$tmp/lib" -name '*.so' -type f 2>/dev/null | sort)
if [[ ${#libs[@]} -eq 0 ]]; then
  echo "FAIL: no .so files found in $apk (expected at least libvt_ffi.so)" >&2
  exit 1
fi

failed=0
for lib in "${libs[@]}"; do
  name="${lib#"$tmp"/}"
  aligns="$("$readelf" -lW "$lib" | awk '$1 == "LOAD" { print $NF }')"
  if [[ -z "$aligns" ]]; then
    echo "FAIL  $name  (no LOAD segments found)"
    failed=1
    continue
  fi
  bad=""
  for a in $aligns; do
    if (( a < 0x4000 )); then
      bad+=" $a"
    fi
  done
  if [[ -n "$bad" ]]; then
    note=""
    [[ "$name" == *libjnidispatch.so ]] && note="  [JNA, see OQ-J]"
    echo "FAIL  $name  LOAD align(s) below 0x4000:$bad$note"
    failed=1
  else
    echo "OK    $name  align $(echo $aligns)"
  fi
done

if (( failed )); then
  echo "16 KB page-size check FAILED" >&2
  exit 1
fi
echo "16 KB page-size check passed for ${#libs[@]} libraries"
