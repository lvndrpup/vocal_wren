---
status: deprecated
date: 2026-10-26
decision-makers: owner (lvndrpup)
---

# Build native libraries with 16 KB page alignment

> Deprecated by [ADR-0006](0006-pure-kotlin-core-module.md) on 2026-10-26: the app ships no
> native libraries. If one is ever added, this decision returns through a new ADR.

## Context and Problem Statement

Android 15 and later devices may use 16 KB memory pages, and Google Play requires apps
targeting recent API levels to support them. Native libraries whose ELF LOAD segments are
aligned to only 4 KB fail to load on such devices. How do we make sure every `.so` we ship
is compatible?

## Decision Drivers

* Google Play 16 KB page-size requirement
* `targetSdk 36` (see [ADR-0002](0002-android-kotlin-compose-minsdk-30.md))
* Third-party native libraries (JNA's `libjnidispatch.so`) are built outside our control

## Considered Options

* Link our Rust library with a 16 KB max page size and check every `.so` in CI
* Rely on NDK defaults only
* Check manually before release

## Decision Outcome

Chosen option: "Link with a 16 KB max page size and check every `.so` in CI", because it
is cheap and catches regressions, including in libraries we don't build ourselves.

* `core/.cargo/config.toml` passes `-C link-arg=-Wl,-z,max-page-size=16384` for
  `aarch64-linux-android` and `x86_64-linux-android`.
* CI unpacks the debug APK and uses the NDK's `llvm-readelf` to require that every LOAD
  segment of every `.so` has `Align >= 0x4000`; the build fails otherwise.

### Consequences

* Good, because incompatible libraries are caught on every PR.
* Bad, because if JNA's prebuilt `libjnidispatch.so` is not 16 KB aligned we must find
  another JNA build or approach (OQ-J, answered by the first CI run).

## More Information

* Android Developers: "Support 16 KB page sizes"
* [Open questions](../open-questions.md), OQ-J
