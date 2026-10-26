---
status: proposed
date: 2026-10-26
decision-makers: owner (lvndrpup)
---

# Pure-Kotlin core module instead of a Rust core

Supersedes [ADR-0001](0001-shared-rust-core-with-uniffi.md). Deprecates
[ADR-0005](0005-16kb-page-alignment.md). Requires constitution v2.0.0 (principle IX).

## Context and Problem Statement

ADR-0001 put all DSP, analysis, confidence, safety and coaching logic in a Rust core
reached from Kotlin through UniFFI and JNA. That means two languages, a generated binding
layer, an NDK cross-compile and native-library alignment checks, all for a solo part-time
project. On 2026-10-26 the owner asked to stay in Kotlin unless there is a critically
important reason for Rust. Is there one?

## Decision Drivers

* Maintainability for one part-time developer: one language, one build
* Principle IX: one shared, tested core; no per-frame allocation or locking on the audio path
* Principle X: the core must be testable on a desktop CI runner without Android
* Real-time needs: Wren *analyses* the voice (about 100 frames/s) and draws feedback; it
  does not play audio back with tight latency
* v3.0: iOS and web later

## Considered Options

* Pure-Kotlin core module (`android/core`, Kotlin/JVM, no Android dependencies)
* Keep the Rust core with UniFFI (ADR-0001)

## Decision Outcome

Chosen option: "Pure-Kotlin core module", because none of Rust's advantages is critical
for this app:

* **Real-time audio:** capture with `AudioRecord` on a dedicated thread into buffers
  allocated once. ART's concurrent garbage collector pauses for well under a millisecond,
  and the capture buffer absorbs that. Analysis, not low-latency playback, is the workload.
* **Speed:** the earlier Rust prototype used about 0.27 ms per 10 ms block. A JVM version a
  few times slower still leaves ample headroom.
* **Testing:** a plain Kotlin/JVM module runs JUnit on any CI runner, which is all the Praat
  oracle (principle X) needs.
* **Other platforms:** the core can move to Kotlin Multiplatform for iOS and web if v3.0
  happens.

Settings: Gradle modules `:app` (Android, Compose) and `:core` (Kotlin/JVM). The app has
no native libraries, so Rust, UniFFI, JNA, the NDK, `cargo-ndk` and the 16 KB
alignment check are removed.

### Consequences

* Good, because the whole project is one language and one Gradle build that IntelliJ opens
  directly.
* Good, because CI is one job and needs no NDK.
* Good, because with no native code the APK has no 16 KB page-alignment risk.
* Bad, because the audio path must be written carefully to avoid per-frame allocation;
  Kotlin does not enforce it the way Rust's type system can. Review and an M1 spike cover
  this.
* Bad, because if a native library is ever needed (for example Oboe), the NDK build and the
  alignment check come back, through a new ADR.

### Confirmation

`android/core/build.gradle.kts` applies only the Kotlin/JVM plugin; CI runs `:core:test`
on every PR.

## More Information

* [Constitution](../constitution.md), principle IX (v2.0.0)
