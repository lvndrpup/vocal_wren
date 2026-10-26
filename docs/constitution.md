# Vocal Wren Constitution

**Version:** 2.0.0
**Ratified:** 2026-10-26 (v1.0.1); v2.0.0 ratified when the owner merges it
**Amended:** 2.0.0, principle IX: the shared core is pure Kotlin instead of Rust ([ADR-0006](adr/0006-pure-kotlin-core-module.md))
**Owner:** lvndrpup (project owner)

These principles are non-negotiable. Every spec, ADR, pull request and agent action must
comply. Anything that would break a principle needs an amendment first (see
[Amendments](#amendments)); it is never done "just this once".

Each principle has a short rationale and a **Checked by** line saying how compliance is
verified. Where a check is not automated yet, the line says so and names who checks it.

---

## I. On-device

Audio never leaves the phone. The app requests no `INTERNET` permission and ships no
analytics, advertising or crash-reporting SDKs.

**Rationale.** Voice recordings are intimate and identifying. The simplest privacy promise
that can be kept is "nothing is sent anywhere", and the simplest way to keep it is to make
sending impossible.

**Checked by.** Manifest review on every PR that touches `android/`; the only permissions
ever allowed are `RECORD_AUDIO`, `VIBRATE`, and `POST_NOTIFICATIONS` (only once the user opts
into reminders). Dependency review rejects analytics, ads and crash SDKs. No background
recording. A CI check of the merged manifest is planned.

## II. Measurement honesty

Every user-facing metric has a confidence value computed in the core. Below the
confidence threshold the app shows no number, no trend and no claim.

**Rationale.** A wrong number presented confidently does more harm than no number. People
change how they use their voice based on what the app tells them.

**Checked by.** Core types carry confidence alongside each value (for example
`Frame.f0_confidence`); unit tests cover the below-threshold path; UI review confirms nothing
is rendered without a passing confidence.

## III. Targets, not identities

The app never stores, requests or infers gender. Training targets are parameter sets
(pitch, resonance, weight); gendered presets are optional labels on those sets, chosen by
the user.

**Rationale.** People train their voices for many reasons. The app serves the target the
user picks and makes no assumption about who they are.

**Checked by.** Spec and data-model review; no field, prompt or classifier for gender
exists anywhere in the code or content packs.

## IV. Not medical care

Wren is a training aid, not a medical device, diagnosis or therapy. It does not claim to
treat or diagnose anything, and it points users to qualified professionals for pain, voice
loss or other concerns.

**Rationale.** Honesty about scope protects users and keeps the app outside medical-device
regulation.

**Checked by.** Content and store-listing review; an SLP review before v1.0 (milestone M6).

## V. Safety over progress

Safety cues pre-empt training cues. Sessions have caps, and the app prompts for rest.

**Rationale.** Vocal strain is a real risk of voice training. No progress goal justifies
injury.

**Checked by.** Safety logic lives in the core with tests proving safety cues take
priority over coaching cues; session caps and rest prompts are covered by spec F8.

## VI. Encouragement, not coercion

No guilt, no loss-aversion streaks, no dark patterns. Reminders are opt-in.

**Rationale.** Voice work is often emotionally loaded. Pressure tactics hurt people and
undermine practice that should be sustained by choice.

**Checked by.** Content-pack and UI review; reminders are off by default and
`POST_NOTIFICATIONS` is requested only after the user opts in.

## VII. Visual-first accessibility

The app works through visual feedback first (it must be usable without hearing the
playback), supports TalkBack, and meets WCAG 2.2 AA.

**Rationale.** Some users cannot or do not want to rely on listening back to themselves,
and accessibility is part of the product, not a later add-on.

**Checked by.** Accessibility checklist in each UI spec; TalkBack walkthrough before each
release; contrast and touch-target checks (spec F15).

## VIII. Content as data

Coaching text lives in versioned content packs, not in code.

**Rationale.** Coaching wording needs review (including by an SLP) and iteration without
rebuilding the app, and it must be versioned so a change can be traced and reverted.

**Checked by.** Code review rejects user-facing coaching strings hard-coded in
code; content packs carry a version (spec F16).

## IX. Shared core

All DSP, analysis, confidence, safety and coaching logic lives in one pure-Kotlin core
module (`android/core`) with no Android dependencies. The steady-state audio path does
not allocate per frame and takes no locks.

**Rationale.** One tested core keeps behaviour consistent, runs its tests on any JVM, and
can be shared with other platforms through Kotlin Multiplatform. One language keeps a
solo project maintainable. Allocation or locking on the audio thread causes glitches and
garbage-collection pauses.

**Checked by.** Code review (Android modules hold UI and platform glue only; the core
module's build file has no Android dependency); audio-path code is reviewed for
per-frame allocation and locking, with automated checks to be decided in M1 spikes.

## X. Test-first, oracle-verified

Tests are written before or with the code. DSP results are verified against an oracle:
Praat (via parselmouth) running in CI. Tolerances are loosened only through an ADR.

**Rationale.** Measurement honesty (II) is only as good as the evidence behind it. An
independent, established tool keeps the core honest.

**Checked by.** CI runs the test suite on every PR; once the oracle lands (M2) it runs on
every DSP PR; tolerance files change only alongside an ADR.

## XI. Decisions recorded

Significant decisions are recorded as MADR ADRs in [`docs/adr/`](adr/).

**Rationale.** A solo, part-time project loses context between sessions. Written decisions
let the owner and agents pick up where they left off and see why things are as they are.

**Checked by.** PR review: architecture, dependency, tolerance and policy changes cite an
ADR. Agents propose ADRs with status Proposed; only the owner accepts them.

---

## Licensing constraint

No GPL, AGPL or LGPL code is shipped in the app binary. The project's intended licence is
Apache-2.0. **Checked by:** dependency review on every PR that adds or upgrades a dependency; an
automated licence check in CI is planned.

## Amendments

1. Anyone (including an agent) may propose an amendment as a pull request that changes this
   file, with the reasoning in the PR description or an accompanying ADR.
2. Only the owner ratifies an amendment by merging it.
3. The constitution is versioned with semantic versioning:
   - **MAJOR**: a principle is removed or its meaning is weakened or reversed.
   - **MINOR**: a principle is added or materially strengthened.
   - **PATCH**: wording, clarification or typo fixes with no change in meaning.
4. Every amendment updates the version and the ratification date at the top of this file.
