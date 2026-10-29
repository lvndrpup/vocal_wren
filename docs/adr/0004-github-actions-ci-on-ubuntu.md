---
status: accepted
date: 2026-10-26
decision-makers: owner (lvndrpup)
---

# GitHub Actions CI on Ubuntu runners

## Context and Problem Statement

The owner develops on Windows and needs every change checked on a clean machine.
Principle X requires tests (and later the Praat oracle) to run on every change. Where does
CI run?

## Decision Drivers

* Principle X: test-first, oracle-verified in CI
* Free for a public repository
* Android SDK preinstalled on the runner
* Python available for parselmouth (the oracle, M2)

## Considered Options

* GitHub Actions on `ubuntu-latest`
* GitHub Actions on Windows or macOS runners
* Self-hosted or third-party CI

## Decision Outcome

Chosen option: "GitHub Actions on `ubuntu-latest`", because the code is already on GitHub,
Linux runners are the fastest and cheapest, and they ship with the Android SDK.

Workflows (triggers: push to `main`, pull requests, manual dispatch):

* `android.yml`: JDK 17 (Temurin), then `gradle :core:test :app:assembleDebug`, uploading
  the debug APK. (The Rust and NDK jobs went away with
  [ADR-0006](0006-pure-kotlin-core-module.md).)
* No Gradle wrapper JAR is committed; CI sets up Gradle with an explicit version.

### Consequences

* Good, because every PR gets the checks the owner can't run locally.
* Bad, because Windows-specific build problems are not caught in CI.

## More Information

* Emulator tests in CI are undecided: OQ-I in [open questions](../open-questions.md).
