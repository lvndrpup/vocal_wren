---
status: proposed
date: 2026-10-26
decision-makers: owner (lvndrpup)
---

# GitHub Actions CI on Ubuntu runners

## Context and Problem Statement

The owner develops on Windows without a guaranteed local Rust or Android toolchain.
Principle X requires tests (and later the Praat oracle) to run on every change. Where does
CI run?

## Decision Drivers

* Principle X: test-first, oracle-verified in CI
* Free for a public repository
* Android SDK and NDK preinstalled on the runner
* Python available for parselmouth (the oracle, M2)

## Considered Options

* GitHub Actions on `ubuntu-latest`
* GitHub Actions on Windows or macOS runners
* Self-hosted or third-party CI

## Decision Outcome

Chosen option: "GitHub Actions on `ubuntu-latest`", because the code is already on GitHub,
Linux runners are the fastest and cheapest, and they ship with the Android SDK and NDK.

Workflows (triggers: push to `main`, pull requests, manual dispatch):

* `rust.yml`: `cargo fmt --check`, `cargo clippy -D warnings`, `cargo test`, `cargo-deny`
  (licence allow-list; no GPL/AGPL/LGPL).
* `android.yml`: JDK 17 (Temurin), Rust Android targets, `cargo-ndk`, the runner's NDK
  (`ANDROID_NDK_LATEST_HOME`), `scripts/build-android.sh`, `gradle assembleDebug`, then a
  16 KB page-alignment check of every `.so` in the APK (see
  [ADR-0005](0005-16kb-page-alignment.md)).
* No Gradle wrapper JAR is committed; CI sets up Gradle with an explicit version.

### Consequences

* Good, because every PR gets the checks the owner can't run locally.
* Bad, because the Windows build script (`scripts/build-android.ps1`) is not exercised
  in CI.
* Bad, because using the runner's latest NDK means the NDK version can change under us.

## More Information

* Emulator tests in CI are undecided: OQ-I in [open questions](../open-questions.md).
