# Build the Rust core for Android and generate its Kotlin bindings.
# Run from the repo root:  pwsh scripts/build-android.ps1
# PowerShell equivalent of scripts/build-android.sh (for the Windows dev machine).
#
# Outputs (both generated and gitignored):
#   android/core-bridge/src/main/jniLibs/<abi>/libvt_ffi.so
#   android/core-bridge/src/main/java/uniffi/vt_ffi/vt_ffi.kt
$ErrorActionPreference = 'Stop'

$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$jniLibs = Join-Path $root 'android/core-bridge/src/main/jniLibs'
$kotlinOut = Join-Path $root 'android/core-bridge/src/main/java'

if (-not (Get-Command cargo -ErrorAction SilentlyContinue)) {
    throw 'cargo not found. Install Rust via https://rustup.rs'
}
if (-not (Get-Command cargo-ndk -ErrorAction SilentlyContinue)) {
    throw 'cargo-ndk not found. Install it with: cargo install cargo-ndk --locked'
}
if (-not $env:ANDROID_NDK_HOME) {
    Write-Warning 'ANDROID_NDK_HOME is not set; cargo-ndk will try to find an NDK itself'
}

# Run inside core/ so core/rust-toolchain.toml and core/.cargo/config.toml apply.
Push-Location (Join-Path $root 'core')
try {
    cargo ndk -t arm64-v8a -t x86_64 -o $jniLibs build -p vt-ffi --release
    if ($LASTEXITCODE -ne 0) { throw "cargo ndk failed (exit $LASTEXITCODE)" }

    # Generate bindings from the unstripped cargo output (the jniLibs copy may be
    # stripped, which would drop the uniffi metadata).
    $targetDir = if ($env:CARGO_TARGET_DIR) { $env:CARGO_TARGET_DIR } else { Join-Path $root 'core/target' }
    $lib = Join-Path $targetDir 'aarch64-linux-android/release/libvt_ffi.so'
    if (-not (Test-Path $lib)) { throw "expected built library at $lib" }

    cargo run -p vt-ffi --features cli --bin uniffi-bindgen -- `
        generate --library $lib --language kotlin --out-dir $kotlinOut --no-format
    if ($LASTEXITCODE -ne 0) { throw "uniffi-bindgen failed (exit $LASTEXITCODE)" }
}
finally {
    Pop-Location
}

Write-Host "Built $jniLibs and $kotlinOut/uniffi/vt_ffi/vt_ffi.kt"
