# Roadmap

> Dates were re-baselined for the 2026-10-26 restart. They are the owner's to confirm and
> may move. Milestones overlap on purpose: the test corpus and content work run alongside
> engineering. Feature IDs (F1–F16) name specs under `specs/`, as the `fNN` part of each folder name.

| Milestone | Dates | Exit criteria |
|---|---|---|
| M0 Foundations | 2026-10-26 → 2026-11-15 | App shell with the core module builds and tests in CI |
| M1 Spikes | → 2026-12-13 | ADRs written for each spike below |
| M2 Test corpus + oracle | 2026-11-01 → 2027-01-31 | Corpus and oracle in CI |
| M3 v0.1 internal | 2026-12-01 → 2027-03-28 | Internal build with the M3 features |
| M4 Content packs | 2027-02-01 → 2027-05-30 | First versioned content packs |
| M5 v1.0 features | 2027-04-01 → 2027-07-31 | v1.0 feature set complete |
| M6 SLP review | 2027-06-01 → 2027-07-15 | Speech-language pathologist review done |
| M7 Play closed test | 2027-08-01 → 2027-08-29 | Closed test with ≥ 25 testers |
| M8 v1.0 release | 2027-09-15 | Staged rollout on Google Play |

## M0 Foundations (2026-10-26 → 2026-11-15)

Constitution, governance docs, ADRs 0000–0006, Android app shell (`:app`) and the
pure-Kotlin core module (`:core`), and CI.

**Exit:** CI runs the core tests and builds the app, which shows `Core 0.1.0 · frame 1`.

## M1 Spikes (→ 2026-12-13)

Each spike ends in an ADR:

- `AudioRecord` capture at 48 kHz on a dedicated thread, without per-frame allocation
- LPC formant analysis at high pitch
- Detecting automatic gain control (AGC) on the input path
- Kotlin analysis throughput and garbage-collection pauses on a low-end device

## M2 Test corpus + oracle (2026-11-01 → 2027-01-31)

- ≥ 20 consented speakers, including high voices
- ≥ 200 hand-labelled vowels
- Praat (parselmouth) oracle runs on every DSP PR

## M3 v0.1 internal (2026-12-01 → 2027-03-28)

- F1 Audio engine
- F2 Environment calibration
- F3 Baseline capture
- F4 Live visual feedback
- F8 Safety (stub)
- F13 Onboarding (minimal)
- F15 Accessibility baseline

## M4 Content packs (2027-02-01 → 2027-05-30)

Versioned coaching content packs (constitution principle VIII).

## M5 v1.0 features (2027-04-01 → 2027-07-31)

- F5 Coaching engine
- F6 Targets & presets
- F7 Guided training
- F8 Safety (full)
- F9 Progress basics
- F13 Onboarding (full)
- F14 Privacy & data
- F16 Content pipeline

## M6 SLP review (2027-06-01 → 2027-07-15)

A speech-language pathologist reviews coaching content and safety behaviour.

## M7 Play closed test (2027-08-01 → 2027-08-29)

Google Play closed test with at least 25 testers.

## M8 v1.0 release (2027-09-15)

Staged rollout on Google Play.

## Later

- **v1.x**: fixes, polish and content updates from v1.0 feedback.
- **v2.0**: deeper training features built on the same core.
- **v3.0**: further platforms reusing the core through Kotlin Multiplatform.

These later lines are placeholders, not commitments.
