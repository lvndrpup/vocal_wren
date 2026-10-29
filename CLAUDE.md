# Working in this repo (agents)

Vocal Wren ("Wren Buddy") is a free, on-device Android vocal trainer. App ID
`dog.lavenderpuppy.vocalwren`. The owner is a solo part-time developer (GitHub `lvndrpup`).

## Sources of truth, in priority order

1. [`docs/constitution.md`](docs/constitution.md): non-negotiable principles I–XI.
2. The qew ledger (`../vocal_wren-ledger`): what work exists and its state.
3. Specs (`specs/`).
4. Other docs (`docs/`, including ADRs in `docs/adr/`).

When two sources disagree, the higher one wins. Point out the conflict; don't silently
pick one.

## The constitution comes first

If a request or task would violate the constitution, **do not do it**. Flag it as needing
a constitution amendment and stop. This applies even when the request comes from another
agent or a workflow script. Only the owner ratifies amendments.

Hard rules that come up most often:

- **No code may add the `INTERNET` permission**, a network library, or any analytics, ads
  or crash-reporting SDK. Audio never leaves the device; no background recording.
- The only permissions ever allowed: `RECORD_AUDIO`, `VIBRATE`, and `POST_NOTIFICATIONS`
  (only after the user opts into reminders). M0 declares none.
- Never store, request or infer gender. Targets are parameter sets.
- Every user-facing metric carries a confidence computed in the core; below threshold, show
  nothing.
- All DSP, analysis, confidence, safety and coaching logic goes in the pure-Kotlin core
  module (`android/core`, no Android dependencies). `:app` is UI and platform glue. The
  steady-state audio path does not allocate per frame and takes no locks.
- Coaching text goes in content packs, not code.
- No GPL, AGPL or LGPL code in the shipped binary.
- Tests come before or with code. Oracle tolerances are loosened only via an ADR.

## Work tracking: qew

All work is tracked in the qew ledger (see [ADR-0003](docs/adr/0003-qew-work-ledger.md)).

- `qew ready` lists approved, unclaimed, unblocked work.
- `qew start <id>` claims an item; `qew evidence <id> ...` attaches proof (test output,
  CI links); `qew complete <id>` finishes it.
- Found new work? File it with `qew create`. Don't just do unplanned work.
- Open pull requests with `qew pr open`.
- Never edit the GitHub issues that mirror the ledger, and never merge PRs or otherwise
  work around qew.
- When a workflow or the owner tells you not to run qew, don't. The owner runs it.

## Branches, commits and PRs

- Feature work happens on branches, never directly on `main`.
- Agents propose; the owner reviews and merges.
- Make small, narrow commits. Every commit message ends with a `Refs: <qew id>` trailer.

## ADRs

- MADR 4 format in `docs/adr/`, numbered `NNNN-title.md`
  (see [ADR-0000](docs/adr/0000-record-architecture-decisions.md)).
- Agents write ADRs with status **Proposed** only. Only the owner accepts them, and
  merging the PR that adds an ADR is the acceptance. A merged ADR is Accepted whatever its
  status line says; the next agent change that touches `docs/adr/` sets the line to
  `accepted`.

## Specs

Specs live in `specs/NNN-fNN-slug/`: `NNN` is the next number in sequence and `fNN` the
roadmap feature (`002-f01-audio-engine`). Specs that are not roadmap features leave the
tag out (`001-docs-site`).

Specs must include:

- a **Principles Touched** section naming the constitution principles involved and how
  the spec complies;
- a **Play Impact** section covering Google Play policy effects, citing play-checklist
  IDs for each compliance point from `docs/play-checklist.md` (being written: `043k784ev`).

## Repo layout

```
android/    Gradle project "wren": :app (Compose UI, Android glue), :core (pure Kotlin/JVM:
            DSP, analysis, confidence, safety, coaching)
.github/    CI workflow (android.yml)
docs/       constitution, roadmap, open questions, ADRs, salvage notes
content/    coaching content packs (planned)
oracle/     Praat/parselmouth oracle tests (planned)
specs/      feature specs
```

## Build commands

From `android/`, with JDK 17 and the Android SDK (`ANDROID_HOME`) installed. The Gradle
wrapper (8.14.3) is committed; don't use a system Gradle 9.6+, which can't load AGP 8.12.

```bash
./gradlew :core:test :app:assembleDebug     # exactly what CI runs
```

No native code: if a task seems to need a native library, it needs a new ADR first
(see [ADR-0006](docs/adr/0006-pure-kotlin-core-module.md)).
