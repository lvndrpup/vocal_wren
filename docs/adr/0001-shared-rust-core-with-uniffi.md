---
status: proposed
date: 2026-10-26
decision-makers: owner (lvndrpup)
---

# Shared Rust core exposed to Kotlin with UniFFI

## Context and Problem Statement

All DSP, analysis, confidence, safety and coaching logic must live in one shared core
(constitution principle IX) and be callable from the Android app. Which language and
binding approach do we use?

## Decision Drivers

* Principle IX: shared core, allocation-free and lock-free real-time audio callbacks
* Principle II: confidence computed in the core, next to each metric
* Principle X: the core must be testable on a desktop CI runner without Android
* No GPL/AGPL/LGPL in the shipped binary
* A solo developer: generated bindings beat hand-written JNI

## Considered Options

* Rust core with UniFFI-generated Kotlin bindings
* Rust core with hand-written JNI
* Kotlin-only (DSP on the JVM)
* C++ core with JNI

## Decision Outcome

Chosen option: "Rust core with UniFFI-generated Kotlin bindings", because Rust gives
memory safety and control over allocation on the audio thread, and UniFFI generates
the Kotlin side from proc-macro annotations with no hand-written JNI.

Shape (M0):

* Cargo workspace at `core/` with `vt-analysis` (pure Rust, no FFI: the `Frame` model and
  confidence types) and `vt-ffi` (the only crate Kotlin sees; library `vt_ffi`, built as
  `cdylib`, UniFFI 0.32 proc-macros).
* `vt-ffi` maps from `vt-analysis` types into its own `uniffi::Record` types, so FFI
  concerns never leak into the analysis crate.
* Kotlin bindings are generated at build time (`scripts/build-android.*`) into the
  `android/core-bridge` module and are not committed. App code uses them only through
  `dog.lavenderpuppy.vocalwren.corebridge.CoreBridge`.
* UniFFI's Kotlin bindings load the library through JNA, which is dual-licensed
  Apache-2.0 / LGPL-2.1; we use it under Apache-2.0.

### Consequences

* Good, because one tested core can serve future platforms.
* Good, because the core runs and is tested on any CI runner with plain `cargo test`.
* Bad, because UniFFI/JNA calls have overhead; high-rate data paths (live frames) may
  need batching. Throughput is a planned M1 spike.
* Bad, because JNA adds `libjnidispatch.so`, whose 16 KB page alignment must be checked
  (see [ADR-0005](0005-16kb-page-alignment.md), OQ-J).

### Confirmation

M0 exit: the hello-frame round trip (Kotlin -> Rust -> Kotlin) builds in CI and the app
shows `Core 0.1.0 · frame 1`.

## More Information

* UniFFI: <https://mozilla.github.io/uniffi-rs/>
* [Constitution](../constitution.md), principles II, IX, X
