# Vocal Wren

Vocal Wren ("Wren Buddy") is a free Android vocal trainer for pitch, resonance and vocal
weight, with plain-language coaching. It is a general-purpose trainer: you choose a
target, and a target is just a set of parameters. Gendered presets exist as optional
shortcuts; the app never asks for or infers your gender.

## Privacy promise

Everything happens on your phone. Audio never leaves the device: the app has no internet
permission, no analytics, no ads and no crash reporting. It never records in the
background.

Wren is a training aid, not medical care. See the [constitution](docs/constitution.md)
for the full set of principles.

## Status

**M0 Foundations.** The goal is a hello-frame round trip (Kotlin → Rust → Kotlin) that
builds in CI; the app shows `Core 0.1.0 · frame 1`. See the [roadmap](docs/roadmap.md).

## Layout

```
core/       Rust core (Cargo workspace): vt-analysis, vt-ffi (UniFFI bindings)
android/    Android app (Kotlin, Jetpack Compose): :app, :core-bridge
scripts/    Build scripts for the native libraries and Kotlin bindings
.github/    CI workflows
docs/       Constitution, roadmap, open questions, ADRs
```

## Building

Needs: Rust (version pinned in `core/rust-toolchain.toml`), `cargo-ndk`, an Android NDK
(`ANDROID_NDK_HOME`), JDK 17, the Android SDK and Gradle.

```powershell
# 1. Build the Rust core for Android and generate Kotlin bindings (Windows)
.\scripts\build-android.ps1
#    or on Linux/macOS: bash scripts/build-android.sh

# 2. Once only: create the Gradle wrapper (the wrapper JAR is not committed)
cd android
gradle wrapper
cd ..

# 3. Build the app
gradle -p android :app:assembleDebug   # or android/gradlew :app:assembleDebug
```

Generated files (`android/core-bridge/src/main/jniLibs/` and
`android/core-bridge/src/main/java/uniffi/`) are gitignored.

## Contributing and work tracking

Work is tracked with [qew](https://github.com/foundlings/qew); the ledger lives in the
sibling [`vocal_wren-ledger`](https://github.com/lvndrpup/vocal_wren-ledger) repository
(`../vocal_wren-ledger`). Run `qew ready` to see available work. Agents: read
[CLAUDE.md](CLAUDE.md). Decisions are recorded in [docs/adr](docs/adr/).

## Licence

Intended licence: Apache-2.0. The `LICENSE` file is still to be added.
