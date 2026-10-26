#!/usr/bin/env bash
# Build the Rust core for Android and generate its Kotlin bindings.
# Run from the repo root:  bash scripts/build-android.sh
#
# Outputs (both generated and gitignored):
#   android/core-bridge/src/main/jniLibs/<abi>/libvt_ffi.so
#   android/core-bridge/src/main/java/uniffi/vt_ffi/vt_ffi.kt
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
jni_libs="$root/android/core-bridge/src/main/jniLibs"
kotlin_out="$root/android/core-bridge/src/main/java"

if ! command -v cargo >/dev/null 2>&1; then
  echo "error: cargo not found. Install Rust via https://rustup.rs" >&2
  exit 1
fi
if ! command -v cargo-ndk >/dev/null 2>&1; then
  echo "error: cargo-ndk not found. Install it with: cargo install cargo-ndk --locked" >&2
  exit 1
fi
if [[ -z "${ANDROID_NDK_HOME:-}" ]]; then
  echo "warning: ANDROID_NDK_HOME is not set; cargo-ndk will try to find an NDK itself" >&2
fi

# Run inside core/ so core/rust-toolchain.toml and core/.cargo/config.toml apply.
cd "$root/core"

cargo ndk -t arm64-v8a -t x86_64 -o "$jni_libs" build -p vt-ffi --release

# Generate bindings from the unstripped cargo output (the jniLibs copy may be
# stripped, which would drop the uniffi metadata).
target_dir="${CARGO_TARGET_DIR:-$root/core/target}"
lib="$target_dir/aarch64-linux-android/release/libvt_ffi.so"
if [[ ! -f "$lib" ]]; then
  echo "error: expected built library at $lib" >&2
  exit 1
fi

cargo run -p vt-ffi --features cli --bin uniffi-bindgen -- \
  generate --library "$lib" --language kotlin --out-dir "$kotlin_out" --no-format

echo "Built $jni_libs and $kotlin_out/uniffi/vt_ffi/vt_ffi.kt"
