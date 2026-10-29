---
status: accepted
date: 2026-10-26
decision-makers: owner (lvndrpup)
---

# Android app in Kotlin and Jetpack Compose, minSdk 30

## Context and Problem Statement

The first platform is Android. Which UI stack and which minimum API level do we target?

## Decision Drivers

* Principle VII: TalkBack support and WCAG 2.2 AA
* Principle IX: the app holds UI and platform glue only; logic lives in the pure-Kotlin core module
* A solo developer: a modern, well-documented toolkit
* Google Play target API level requirements

## Considered Options

* Kotlin + Jetpack Compose (Material 3)
* Kotlin + Android Views (XML layouts)
* A cross-platform UI framework (Flutter, React Native)

## Decision Outcome

Chosen option: "Kotlin + Jetpack Compose (Material 3)", because it is Google's current
recommended toolkit, has built-in semantics for accessibility, and keeps the app layer
thin over the core module.

Settings: Gradle Kotlin DSL with a version catalog; modules `:app` and `:core`
([ADR-0006](0006-pure-kotlin-core-module.md));
`minSdk 30`, `compileSdk 36`, `targetSdk 36`; JVM toolchain 17.

**minSdk 30 rationale: TODO (owner).** Why API 30 (Android 11) rather than a lower
minimum is not yet written down. See OQ-R in [open questions](../open-questions.md).

### Consequences

* Good, because Compose semantics make TalkBack support straightforward.
* Good, because a recent minSdk reduces compatibility work.
* Bad, because minSdk 30 excludes devices on Android 10 and older.

## More Information

* [Constitution](../constitution.md), principles VII and IX
* [Open questions](../open-questions.md), OQ-R
