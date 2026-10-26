# Working in this repo (agents)

Vocal Wren ("Wren Buddy") is a free, on-device Android vocal trainer. App ID
`dog.lavenderpuppy.vocalwren`. The owner is a solo part-time developer (GitHub `lvndrpup`).

## Sources of truth, in priority order

1. [`docs/constitution.md`](docs/constitution.md): non-negotiable principles I–XI.
2. The qew ledger (`../vocal_wren-ledger`): what work exists and its state.
3. Specs (`specs/`, planned).
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
- Every user-facing metric carries a confidence computed in Rust; below threshold, show
  nothing.
- All DSP, analysis, confidence, safety and coaching logic goes in the Rust core. Kotlin is
  UI and platform glue. Real-time audio callbacks are allocation-free and lock-free.
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
- Agents write ADRs with status **Proposed** only. Only the owner accepts them.

## Specs

Specs (planned under `specs/`) must include:

- a **Principles Touched** section naming the constitution principles involved and how
  the spec complies;
- a **Play Impact** section covering Google Play policy effects, citing play-checklist
  IDs for each compliance point.

## Repo layout

```
core/       Rust workspace: vt-analysis (pure analysis), vt-ffi (UniFFI, the only crate Kotlin sees)
android/    Gradle project: :app (Compose UI), :core-bridge (generated bindings + CoreBridge)
scripts/    build-android.sh / build-android.ps1
.github/    CI workflows (rust.yml, android.yml)
docs/       constitution, roadmap, open questions, ADRs
content/    coaching content packs (planned)
oracle/     Praat/parselmouth oracle tests (planned)
specs/      feature specs (planned)
```

## Build commands

Rust checks, as CI runs them. Run them inside `core/`: rustup picks the toolchain pinned
in `core/rust-toolchain.toml` from the current directory, not from `--manifest-path`.

```bash
cd core
cargo fmt --all --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace
cargo deny --all-features check        # needs cargo-deny installed
cd ..
```

Android, from the repo root:

```bash
# Native libs + Kotlin bindings (needs cargo-ndk and ANDROID_NDK_HOME)
bash scripts/build-android.sh          # or: pwsh scripts/build-android.ps1 on Windows

# App (CI uses Gradle 8.14.3; run `gradle wrapper --gradle-version 8.14.3` once in
# android/ to get ./gradlew locally; the wrapper files are gitignored)
gradle -p android :app:assembleDebug
```

The build script cross-compiles `vt-ffi` with `cargo ndk` into
`android/core-bridge/src/main/jniLibs/` and generates Kotlin bindings into
`android/core-bridge/src/main/java/uniffi/vt_ffi/`. Both are generated and gitignored;
never commit them.
