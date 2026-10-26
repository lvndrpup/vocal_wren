# Salvage audit: `voice-trainer` (Resonance Scope) → Vocal Wren

| | |
|---|---|
| Source | github.com/lvndrpup/voice-trainer, `main` @ `77fc562` (2026-08-28), 58 commits, 107 tracked files |
| Unmerged branches diffed | `origin/chore/wizard-review-light-default` @ `2c3ce82`; `origin/feat/calibration-raw-frame-persistence` @ `1903eb8` |
| Method | I read every tracked file on `main`. I hash-checked the 22 Spec Kit files against `.specify/integrations/*.manifest.json`: all are unmodified upstream v1.0.1, so I skimmed them rather than auditing them line by line. I read `package-lock.json` for licences only. I did not run anything (no `npm install`, no tests). |
| Audit date | 2026-10-26 |

## TL;DR

- **voice-trainer *is* Resonance Scope**, the repository behind that working name. It is not an ancestor. The repo reached v0.3 of 7 planned versions, built over 10 days (2026-08-18 → 08-28).
- **What can be reused, by type:**
  - Two small DSP estimators: NSDF pitch and LPC F1/F2. Both have known, measured weaknesses.
  - A well-reasoned calibration protocol with a headless step engine.
  - Design notes for strain detection and risk tiers.
  - Accessibility lessons.
  - Strong process and agent tooling: docs-auditor, dsp-numerics-auditor, review personas, and a test-plan merge gate.
- **Gaps:**
  - Nothing is checked against an external oracle, and nothing has been tested on a real voice.
  - No estimator returns a confidence value.
  - There is no exercise or coaching content.
  - There is no resonance, brightness or vocal-weight metric. The only resonance data is F1/F2, captured during calibration.
- **Biggest conflicts with the Vocal Wren constitution** (detail in §4):
  - "For vocal feminization" framing runs throughout (III).
  - User-facing strings are hardcoded in source (VIII).
  - Estimators return a value or nothing, with no confidence (II).
  - Testing is synthetic only (X).
  - "Describes, never grades" rules out the encouragement Vocal Wren wants (VI).
  - The repo deliberately softened its strain caution (V).
- **Unmerged branches:**
  - `wizard-review-light-default` holds one useful tooling commit, `5945c4f`.
  - `calibration-raw-frame-persistence` adds nothing: its trees diff empty against the #56 and #59 squash commits. Delete it.
- **Licence:** there is no licence file, and one human author wrote everything, so you can relicense freely. There is no GPL or AGPL code, and every npm dependency is dev-only.

---

## 1. What voice-trainer is

### Identity

Every naming point says "Resonance Scope":

- README, CLAUDE.md, and the constitution title.
- `package.json` name `resonance-scope`.
- IndexedDB database `resonance-scope`.
- Export file name `resonance-scope-sessions-<ts>.json`.
- GitHub Project board "Resonance Scope".

`voice-trainer` is only the repo slug. "Resonance Scope" is explicitly a working name. A neutral user-facing name was still open, because "some users are in living situations where an explicit name is a problem" (`docs/decisions.md` §Open). The same constraint applies to Vocal Wren.

How your prior findings line up with this repo:

| Prior finding | Found here? | Detail |
|---|---|---|
| "MPM k=0.9 fixed octave errors" | Yes | Matches `bfd30d9`. Here 0.9 is an **absolute** threshold (see D1). |
| "F1 unreliable above F0≈280 Hz" | Yes | Matches `9f11f3f`: F1 errors of 12–25 %+ at F0 220–350 Hz. |
| "LPC order 10" | No | Not in this repo or its history. Order was a fixed 12, then `round(fs'/1000)+4`, which is 16 at 48 kHz. |

Order 10 matches Praat's Burg default: 5 formants gives order 10 [from memory]. If another Resonance Scope build produced that finding, it isn't in this repo. [uncertain]

### Architecture and data flow

Stack: Vite + TypeScript, no UI framework, Canvas 2D, 100 % client-side. Module boundaries are enforced by `no-restricted-imports` in `eslint.config.mjs`.

| Module | Role | LOC |
|---|---|---|
| `src/audio` | the only code that touches Web Audio | 276 |
| `src/dsp` | pure functions: log-bins, pitch, formants, medians | 594 |
| `src/calibration` | headless calibration step engine and validity checks | 392 |
| `src/render` | Canvas spectrogram | 80 |
| `src/store` | IndexedDB for sessions and calibrations | 408 |
| `main.ts`, `wizard.ts`, `tick-features.ts`, `dom.ts`, `describe-capture-error.ts` | composition and DOM wiring | 769 |

Tests: 60 unit tests (`node --test`) and 11 Playwright e2e tests. Docs run to about 3,000 lines; custom agent tooling to about 770.

```
getUserMedia(echoCancellation/noiseSuppression/autoGainControl {exact:false}, mono)
  → AnalyserNode(fftSize 2048, smoothingTimeConstant 0.8, min/max dB −100/−30)
  ├─ main.ts tick() on requestAnimationFrame (~60 Hz)
  │    getSpectrum → computeLogFrequencyBins(300 rows) → SpectrogramRenderer.pushColumn
  │    getSpectrum → peakDb = max bin (dBFS)                → readout
  │    getWaveform (2048 samples) → detectPitch             → readout ("—" if null)
  │    every 100 ms → FeatureFrame{timestamp, f0Hz|null, peakDb} → IndexedDB "frames"
  └─ wizard.ts (its own MicrophoneCapture; setInterval 100 ms within each step)
       steps 0/1/2/4/5 → {levelDb, f0Hz};  corner-i/a/u → {levelDb, estimateFormants}
       → CalibrationEngine.submitStep → validity check → buildDraft
       → IndexedDB "calibrations" + raw readings in "calibrationFrames"
```

### Maturity: what works vs. stubs

About 18 of the 56 first-parent commits on `main` changed product code. 9 commits only added ledger rows; the rest were process, tooling or docs.

| Area | State |
|---|---|
| Mic capture with AGC/AEC/NS off | Works on Chromium, including a fake-mic e2e test. iOS and Android browsers untested. No device picker; unplugging the mic is unhandled. |
| Log-frequency spectrogram | Works. |
| Live F0 readout | Works on synthetic sines. Never validated on real voice. |
| Formants (F1/F2) | Run only inside the calibration wizard at 10 Hz. No live formant or resonance display. Synthetic validation only. |
| Session logging | Works: `{f0Hz, peakDb}` at 10 Hz. |
| Export / delete-all | **Sessions only.** Calibration data can be neither exported nor deleted from the UI. `CalibrationStore.deleteAll()` exists but is never called. |
| Calibration wizard | Works end to end and saves a `Calibration` plus its raw frames. Nothing ever reads either back: `getLatestCalibration` and `getCalibrationFrames` have no callers. |
| v0.4: targets, post-session report, adherence streak | Not started. |
| v0.5: strain interface, self-report, off-day flag | Design docs only. |
| v1.0: onboarding, progressive disclosure, risk tiers, SLP review | Design docs only. |
| Coaching / exercise content | None. Open question: "needs a real SLP source." |
| Resonance, brightness, weight / spectral tilt | None. |
| Confidence values | None. Every estimator returns a value or `null`. |
| Oracle / golden-file DSP tests | Planned, deferred three times, never built. |

### Unmerged branches

**`origin/chore/wizard-review-light-default`** (`5945c4f` plus the merge `2c3ce82`; PR #81):

- `/wizard-review` defaults to one correctness reviewer. The four-persona fan-out, reaction round and Scrum Master run only with `deep`.
- Reverses the earlier rule that the Scrum Master "always runs last". `/wizard-act` is updated so a missing Scrum Master comment no longer counts as "never reviewed".
- Rationale is in the commit and in `decisions.md`: the cost was the fan-out of 5–6 cold agent runs, not the roughly 2,000 words of persona text.
- Also commits `.specify/feature.json` by mistake. That file is per-checkout state that `.specify/.gitignore` ignores.
- **Worth taking (agent tooling), minus `feature.json`.**

**`origin/feat/calibration-raw-frame-persistence`** (`88d6777`, `ad788b9`, `debcff7`, `d990099`, `1903eb8`, branched from `dd2fc83`):

- This is the pre-squash history of PRs #56 and #59.
- `git diff cf46ebd debcff7` and `git diff 7a5a1db 1903eb8` are both empty.
- Its diff against `main` only shows that it's behind: it lacks the accessibility fixes, the `MIN_DRAWN_LEVEL` floor and the realistic test windows.
- Only its commit messages have value, as the record of the mutual-exclusion race and the e2e helper hang (§3).
- **Nothing to salvage. Delete the branch.**

---

## 2. Salvage inventory

**Reuse modes:** port algorithm to Rust, port to Kotlin UI, adopt content-text as content pack, adopt spec-or-doc, adopt test fixture-or-test case, adopt agent tooling, reference only.

**Effort:** S = hours, M = 1–3 days, L = a week or more (including tests and docs).

**Verification:** "[likely]" means the source repo itself never checked the claim.

### 2.1 DSP & analysis

| ID | Source | What it is | Reuse mode | VW target | Effort | Notes |
|---|---|---|---|---|---|---|
| D1 | `src/dsp/index.ts` `detectPitch`; `docs/pitch-detection.md`; `bfd30d9` | NSDF / McLeod-style F0 on one 2048-sample window | port algorithm to Rust | F1 · vt-dsp | S | `NSDF(τ) = 2Σx[i]x[i+τ] / Σ(x[i]²+x[i+τ]²)` over the overlap. Lags searched `floor(fs/1000)` … `min(N−1, ceil(fs/50))`, i.e. 50–1000 Hz. Takes the **first** local max with NSDF ≥ 0.9; parabolic refine `τ + 0.5(y₋−y₊)/(y₋−2y₀+y₊)`. Returns `null` for silence, no qualifying peak, or a too-short window. See port notes. |
| D2 | `estimateFormants` and helpers in `src/dsp/index.ts`; `docs/formant-extraction.md`; `7dba395`, `9f11f3f` | LPC F1/F2 | port algorithm to Rust as a **baseline** to compare against the oracle; replace the peak-picking | F1 · vt-dsp | M | Constants in the port notes. Known failure modes: F1 error of 12–25 %+ at F0 220–350 Hz; formants closer than ~150–300 Hz merge and return `null` (typical for /u/). No F3 and no bandwidths, so no confidence. |
| D3 | `computeLogFrequencyBins`; `eb4b8a5` | remaps linear FFT bins onto a log2 frequency axis for display | port algorithm to Rust (or Kotlin) | F4 | S | `f_i = 2^(log2 fmin + i/(n−1)·(log2 fNyq − log2 fmin))`, interpolating linearly between the 2 nearest bins. fmin 20 Hz; there is no fmax. Issue #2 asked for 60 Hz–8 kHz; never reconciled. Near the top, one row spans many FFT bins but only 2 are sampled, so narrow peaks can vanish. Take the max or power-mean per row instead. |
| D4 | `medianOfFinite`, `estimateHabitualF0Hz` | robust aggregation that drops null, NaN and ±∞ | port algorithm to Rust | F3 · vt-analysis | S | Habitual F0 = median of the voiced frames from "count to five". Keep as is. |
| D5 | `estimateComfortableF0Range` | comfortable F0 range from the greeting and hum-slide steps | port algorithm to Rust **with a change** | F3, F6, F8 | S | Floor = min of the hum F0s; ceiling = max(max hum, max greeting). The repo marks this formula [likely] in decisions.md §Open. Raw min/max means one octave-error frame sets the range. Use percentiles (e.g. P5/P95) and a minimum voiced-frame count. |
| D6 | `src/tick-features.ts` `peakDb` | "level" = loudest dB bin of the AnalyserNode spectrum, smoothed at 0.8 | reference only | F1 level | — | Not a usable level measure: it depends on the window and the smoothing, and is −∞ in silence. Vocal Wren should use per-hop RMS dBFS plus a clipping count. Every dB threshold in the repo (C3) is in this unit and doesn't transfer. |
| D7 | `docs/strain.md`, Approaches 3–4 | notes on vocal weight, spectral tilt and perturbation measures | reference only | vt-analysis (weight), F8 | — | Nothing implemented. Three findings worth keeping, each described below the table. |
| D8 | — | resonance/brightness metric, smoothing, voicing, confidence | reference only | F1, F4, F5 | — | All absent. No spectral centroid or brightness measure, no F0 smoothing or hysteresis. Voicing is only "NSDF ≥ 0.9". The only confidence is the strain *design* (K2). Build these new. |

**D7 detail:**

- **Spectral tilt.** H1-H2, H1-A1 and H1-A3 track phonation type: lower H1-H2 means pressed, higher means breathy. The repo cites voicescience.org; Hanson 1997 and Hillenbrand et al. 1994 are cited but were never opened. These measures need formant correction and are confounded by mic response, vowel, F0 and distance.
- **CPPS points the wrong way for strain.** Pressed phonation is highly periodic, so CPPS can rise under strain.
- **Jitter and shimmer** on a laptop mic "mostly measure the room."
- The repo's recommendation: log these measures, but don't feed them back to the user until they are validated.

**Port notes D1 (pitch).**

Keep:
- Normalising each lag by its own overlap energy, and taking the first acceptable peak. Both fixed real bugs (`bfd30d9`).
- Parabolic refinement.
- Treating 50–1000 Hz as search bounds, not targets.

Change:
1. **Cost.** Compute the autocorrelation with an FFT. The direct form costs up to ~1.4 M inner-loop iterations per call (all 913 lags at 48 kHz). Every unvoiced frame pays the full cost, at 100 frames/s on a phone.
2. **Threshold.** 0.9 here is an **absolute** threshold that is also the only voicing gate. Canonical MPM applies k relative to the highest key maximum and gates voicing separately. Expect dropouts on breathy, soft or noisy real voices [likely].
3. **Confidence.** Return the clarity value (NSDF at the chosen peak) as the F0 confidence. The code currently computes and discards it.
4. **Level gate.** Add a level/SNR gate. NSDF ignores amplitude, so any quiet periodic background in 50–1000 Hz is reported as a pitch: mains-hum harmonics, a fan, a TV [likely, by construction, untested].
5. **Edge case.** A peak at exactly `minLag` is never detected, because the search needs a rise before the fall.

**Port notes D2 (formants)**, exact constants from the source:

```
target rate   = 2 * maxFormantHz              (default 5000 → 10 kHz)
decim factor  = max(1, floor(fs / target))     48k→4 (12 000 Hz), 44.1k→4 (11 025), 16k→1
anti-alias    = 65-tap Hamming windowed-sinc, cutoff 0.9 * (fs'/2), DC-normalised
pre-emphasis  = y[n] = x[n] − 0.97 x[n−1]
window        = Hamming 0.54 − 0.46 cos(2πn/(N−1))
order p       = round(fs'/1000) + 4            16 @48k, 15 @44.1k, 20 @16k  (originally a fixed 12)
LPC           = autocorrelation r[0..p] → Levinson–Durbin; null if r0 ≤ 0 or prediction error ≤ 0
envelope      = 20·log10(1/|A(e^jω)|) on a 5 Hz grid over [150, min(5000, fs'/2 − 1)] Hz
peaks         = local maxima, parabolic refine; drop prominence < 3 dB; merge peaks < 150 Hz apart
result        = first two survivors = (F1, F2); otherwise null
```

Recommendations for Vocal Wren:

1. **Root-solve the LPC polynomial.** That yields F1–F3 plus bandwidths, which feed confidence. The repo rejected root-solving only to avoid adding a dependency (#67, never done).
2. **Retest the LPC order (spike).**
   - The repo's own data shows a higher order hurts at high F0. Going from 16 to 20 took `/i/` at 280 Hz from 2.3 % to 71.6 % F2 error, and `/a/` at 350 Hz from 4.3 % to 51.2 % F1 error.
   - That trend fits your order-10 finding. Test 10 vs 16 in M1.
   - Pitch-synchronous windowing was tried and doesn't help. It moved errors by under 1 point, and `/u/` at 220 Hz got worse (F1 6.2 % → 10.4 %).
3. **Guard against label shift.** "First two survivors" means a missed F1 silently reports F2 as F1, with no warning.
4. **Formant ceiling.** Don't take it from Praat's sex-based 5000 / 5500 Hz convention. Use a fixed value or one derived from the user's calibration (principle III).
5. **Real-time constraints (principle IX).**
   - The decimator filters at the full rate and then throws away 3 of 4 samples; use a polyphase filter.
   - Every stage allocates memory. Levinson–Durbin allocates a fresh array on each recursion step. Preallocate instead.

### 2.2 Capture, calibration, persistence

| ID | Source | What it is | Reuse mode | VW target | Effort | Notes |
|---|---|---|---|---|---|---|
| C1 | `docs/adr/0002-agc-off-raw-constraints.md`; `src/audio/index.ts`; `213e82d` | raw-capture decision, read-back of applied settings, typed errors, capture state machine | adopt spec-or-doc (supersede it with a VW ADR); port to Kotlin (error and state model) | F1, F2 | S | Detail and Android notes below the table. |
| C2 | `docs/calibration.md`; `STEP_PROMPTS` in `src/calibration/index.ts` | 6-step calibration protocol, ~90 s (8 engine steps) | adopt spec-or-doc + adopt content-text as content pack | F2 (step 0), F3 (steps 1–5), F13 | M | Steps and design rationale below the table. |
| C3 | `CalibrationEngine` and `computeStepValidity` in `src/calibration/index.ts`; ADR 0004; `f686930`, `1849d65` | headless calibration state machine with validity checks | port algorithm to Rust | F3 · vt-analysis | M | Engine behaviour and thresholds below the table. |
| C4 | `docs/calibration-store.md`; `src/store/calibration.ts`; `7a5a1db` | calibration record, plus raw per-step frames kept for recompute | adopt spec-or-doc (schema) | F3, F14 | S | `Calibration{schemaVersion, id, timestamp, deviceId?, noiseFloorDb?, levelReferenceDb?, habitualF0Hz?, comfortableF0Range?, cornerVowels{i,a,u}?, validity}` and `CalibrationStepFrame{calibrationId, stepId, levelDb, f0Hz?, formants?}`. Keep the rule "store raw features so calibrations can be recomputed when the estimators change". Nothing ever read them back. Add an estimator version, per-metric confidence, and F3. |
| C5 | `docs/calibration.md`, Re-calibration and Validity handling sections | re-calibration triggers; "degrade, do not block" | adopt spec-or-doc | F2, F3, F6 | S | Triggers: device change, 30+ days, the user reporting a vocal change, or habitual F0 drifting. A partly invalid calibration blocks tier B/C targets but keeps the instrument; the report says what went wrong and offers to redo that step. Re-calibrating under the same protocol doubles as a progress artefact (F9). |
| C6 | ADR 0003; `docs/session-store.md`; `src/store/index.ts`, `idb.ts` | session/frame persistence model | adopt spec-or-doc (Room/SQLite design) | F9, F14 | S | Keep: sessions and frames in separate tables (O(1) append); `schemaVersion` on every record; the caller throttles logging (10 Hz); a storage failure degrades gracefully (the instrument keeps running and tells the user "not saving"). Fix these gaps: −∞ serialises to JSON `null`; an abrupt exit leaves `endedAt` null; no quota handling; no migrations. |

**C1 detail:**

- Requests AEC, NS and AGC off with `{exact:false}`, mono. It **fails hard** (`OverconstrainedError`) rather than degrade.
- Errors: permission-denied, not-found, hardware-busy, constraints-unsupported, context-suspended, state-misuse.
- States: uninitialized → permission-requested → active / denied / error / suspended → stopped.
- ADR 0002 itself notes some Android stacks can't fully disable AEC [likely].
- **Android analogue:** Oboe `InputPreset::Unprocessed`, falling back to `VoiceRecognition`. Assert that no AGC/NS/AEC effects are attached, and record the applied configuration.
- F2 wants *detect it and lower the session's trust* instead of failing hard. That needs a new ADR.

**C2 steps:**

| Step | Prompt task | Duration | Produces |
|---|---|---|---|
| 0 | stay quiet | 3 s | noise floor |
| 1 | "ahh" | 5 s | steadiness, level reference |
| 2 | count to five | 5 s | habitual F0 |
| corner /i/ /a/ /u/ | one vowel each | 2 s each | formant anchors |
| 4 | "hiii" greeting | 2 s | top of comfortable range |
| 5 | hum slide | 8 s | comfortable range |

That is 29 s of capture in total.

Design rationale to keep:

- The greeting register replaces a max-pitch task.
- "Stop wherever it stops feeling easy" is deliberate safety wording.
- Testing maximum range is opt-in, only after several sessions and a warning, and never during onboarding.
- Never auto-play recordings.
- One-tap redo for each step.
- "Don't say 'calibrating'; say what it's for."

**C3 detail:**

- API: `beginStep`, `submitStep`, `redoStep`, `isComplete`, `getStepReadings`, `buildDraft`.
- One step can be in progress at a time, in any order. Each vowel can be redone on its own.
- Aggregates readings by median. `valid` is true only if every check passes, but consumers read the individual checks.
- Port with a Rust enum per step family. That rules out the wrong-shape bug class fixed in `1849d65`.

Validity thresholds, all [likely] and set without real-device data:

| Constant | Value | Where used |
|---|---|---|
| `NOISE_FLOOR_MAX_DB` | −50 | step 0; median peak-bin dB, the D6 unit |
| `MIN_VOICED_RATIO` | 0.5 | step 2 and each vowel |
| `MAX_F0_STDEV_HZ` | 40 | step 1; population standard deviation |

Re-express the F0 standard deviation in semitones. 40 Hz is 40 % at 100 Hz but 13 % at 300 Hz. Steps 4 and 5 have no check, and the "level far from session-1 reference" check was never implemented.

### 2.3 Visualisation & accessibility

| ID | Source | What it is | Reuse mode | VW target | Effort | Notes |
|---|---|---|---|---|---|---|
| U1 | `src/render/index.ts`; `docs/spectrogram.md`; `eb4b8a5`, `5d895af` | scrolling log-frequency spectrogram | port to Kotlin UI (concept) | F4 | S | One column per frame, low frequencies at the bottom. Grayscale, linear dB→brightness over [−100, −30] dB. `MIN_DRAWN_LEVEL = 24/255` keeps drawn silence distinguishable from never-drawn canvas. In Compose, use a ring-buffer bitmap (write one column, draw two slices) instead of redrawing the whole canvas onto itself each frame. |
| U2 | `docs/spectrogram.md` (issue #65); `be3c6b4`; `specs/001-noise-floor-brightness/research.md` | perceptual check of a brightness map: sRGB EOTF → CIE L* | adopt spec-or-doc (method) | F4, F15 | S | Linear-dB grayscale came out roughly perceptually uniform: mean ΔL* per 5 dB step was 7.66 in the quiet half vs 6.63 in the loud half. Floor trade-off: 8/255 gives L* 2.19 and collapses 2.2 dB; 24/255 (what shipped) gives L* 8.25 and collapses 6.6 dB. Neither was checked on a real display. Reuse the method to validate any Vocal Wren colour map (L* must be monotonic). |
| U3 | `src/main.ts` (`READOUT_ANNOUNCE_INTERVAL_MS`), `index.html`; `fd95f50` | throttled screen-reader announcements | port to Kotlin UI | F15 | S | Visual readouts refresh freely with no live region. One hidden polite region announces "Peak −20.3 dB, F0 180.2 Hz" every 1000 ms. A polite region updated at 10 Hz had flooded the announcement queue. TalkBack equivalent: `liveRegion = Polite` on a single throttled summary node. |
| U4 | `src/dom.ts` `focusIfIdle`; `wizard.ts` `claimFocusIfNotElsewhere` and `showProgress`; `c8218e7`, `b1a20c3` | focus and announcement hygiene | port to Kotlin UI (principles) | F15, F13 | S | Rules listed below the table. |
| U5 | `src/wizard.ts`; `docs/calibration-wizard.md` | guided-step UX | port to Kotlin UI | F3, F13 | S | Progress as text: "Step N of 8". Never auto-advance; show Next/Redo after each result. Cancel discards everything, so nothing partial is saved. The completion message lists by number the steps that need a redo, with no score. |
| U6 | `docs/index.md`, Layer model | L0 capture → L1 features → L2 calibration → L3 targets → L4 feedback → L5 history; the instrument display hangs off L1 | adopt spec-or-doc (as an ADR) | architecture, F4–F6, F9 | S | Gate: no targets or feedback until a calibration exists. Maps onto vt-dsp → vt-analysis → F3 → F6 → vt-coach → F9. |

**U4 rules:**

- Restore focus only if nothing else holds it.
- Never take focus from something outside the wizard panel.
- After a status update, wait 150 ms before moving focus (`FOCUS_ANNOUNCEMENT_DELAY_MS`, [speculative]).
- Clear text, then set it, so a redo re-announces the same text.
- Make every timer check whether the wizard was aborted.
- Always announce cancel and completion.
- Re-tune the timings against TalkBack.

### 2.4 Safety, coaching, content

| ID | Source | What it is | Reuse mode | VW target | Effort | Notes |
|---|---|---|---|---|---|---|
| K1 | `docs/strain.md`, Approaches | five strain-detection approaches, each with a verdict | adopt spec-or-doc | F8 (stub in M3, full in M5) | M | Approaches listed below the table. Reword the clinical terms (IV). |
| K2 | `docs/strain.md`, Interface | `StrainSignal{id, score 0..1, confidence 0..1, rationale}`; `StrainEstimator{id, requires, estimate(window) → signal or null}`; the resolver takes the confidence-weighted max | port algorithm to Rust | F8 · vt-safety | S | Self-report registers at confidence 1.0. An unvalidated proxy ships at 0.2 and can only nudge; it is promoted once it correlates with the self-report labels. Same shape as VW II (metric plus confidence). `rationale` must become a content-pack key (VIII). |
| K3 | `docs/strain.md`, Exercise risk tiers | A/B/C gating, set per exercise | adopt spec-or-doc | F7, F8 | S | Tiers listed below the table. VW V needs hard caps and cues that pre-empt training (§4). |
| K4 | `docs/decisions.md`, Decided — product | coaching cadence: sparse, non-scoring live cues; substantive feedback after the session | adopt spec-or-doc (as ADR rationale) | F5, F4 | S | Cites Winstein & Schmidt 1990 (the guidance hypothesis); Van Stan et al. 2017, JSLHR 60(4) (summary feedback → better retention on a voice task); Van Stan et al. 2017, AJSLP 26(1) (voice evidence still thin). This is in tension with F4's live feedback, so decide it in an ADR. |
| K5 | `docs/decisions.md`, Decided — product | progressive disclosure; off-day flag | adopt spec-or-doc | F13, F9, F6 | S | Session 1: instrument plus one guided calibration, no targets. Sessions 1–5: the user's own trends only ("still learning your voice"). From session 5: targets derived from calibration. A one-tap off-day flag (sick / tired / post-op) excludes the session from trends and suppresses targets. Don't persist the *reason*: it is health data (IV, F14). |
| K6 | `STEP_PROMPTS`, `computeStepValidity`, `buildCompletionMessage` (`wizard.ts`), `describeCaptureError` | every user-facing string (about 30) | adopt content-text as content pack | F16 · vt-content, F2/F3 | S | 8 prompts (C2), 10 validity messages, completion and cancel text, and 6 capture-error messages. Example: "It's noisy in here — find a quieter spot and redo this step." One fix needed: step 2 tells the user to "try speaking a little louder", but the repo's own tier table puts loudness work in tier C. Use "move a little closer to the mic" instead. **No exercise or coaching content exists.** |
| K7 | CLAUDE.md non-negotiables; constitution IV | rules on streaks and scores | reference only | F9 | — | Forbidden: performance streaks, leaderboards, personal-best pitch, scores or verdicts, and calling a trend "progress". Allowed: adherence streaks, shown post-session only, that survive off-days. Reconcile with VI (§4). |

**K1 approaches:**

1. **Self-report**, Borg CR10-*style* effort rating. Ship first; it is the label set the others are validated against.
2. **Range-relative geometry**: F0 against the calibrated ceiling, cumulative phonation time, F0 drift within a session. Ship second.
3. **Spectral tilt**: H1-H2, H1-A1, H1-A3. A stretch goal.
4. **Perturbation measures**: jitter, shimmer, HNR, CPPS. "Mostly a trap."
5. **Per-user logistic regression** on 2 and 3, trained on 1's labels. The eventual payoff.

**K3 tiers:**

| Tier | Risk | Examples | Coaching behaviour |
|---|---|---|---|
| A | low | SOVT, straw phonation, humming, mid-range glides | full coaching and live cues |
| B | moderate | resonance work, connected speech in the target range | coaching on, self-report required at session end, soft time cap |
| C | high | sustained work near the ceiling, loudness work, anything above the comfortable range | instrument only: no targets, no cues, timer visible |

### 2.5 Presets / target ranges

| ID | Source | What it is | Reuse mode | VW target | Effort | Notes |
|---|---|---|---|---|---|---|
| P1 | constitution III; CLAUDE.md; `docs/formant-extraction.md`; `src/dsp/index.test.ts` | target policy | reference only | F6 | — | Detail below the table. |

**P1 detail:**

- **No presets in code.** There are no presets or target ranges anywhere in the code; they are forbidden ("every target derives from the user's own calibration").
- **Gendered framing in prose.** It appears only in docs: F0 220–350 Hz is called "plausible feminization-training targets" (`formant-extraction.md`, `decisions.md`). ⚠ III.
- **Test fixtures.** The formant fixtures (270/2290, 730/1090, 300/870) are Peterson & Barney's adult-*male* averages [from memory], labelled only "adult". They are fine as fixtures, but test coverage stops at this lowest-formant set.
- **Idea worth taking for F6.** Express presets as offsets from the user's own calibration: semitones above habitual F0, or a % shift from their own corner vowels. That makes them non-gendered by construction.

### 2.6 Specs, constitution, ADRs, docs

| ID | Source | What it is | Reuse mode | VW target | Effort | Notes |
|---|---|---|---|---|---|---|
| S1 | `.specify/memory/constitution.md` v1.0.0 | 8 principles, Quality Gates, Governance | adopt spec-or-doc (Governance and Quality Gates); reference only (the principles) | M0 | S | Governance rules to keep are listed below the table. Quality Gates: tests, honest verification (say what couldn't be verified), and named failure modes. |
| S2 | `docs/adr/0001`–`0005` | five ADRs in a light MADR format | adopt spec-or-doc (rewrite as Vocal Wren ADRs) | M0, XI | S | 0001 client-only, so privacy is structural; 0002 raw capture; 0003 sessions/frames split; 0004 headless calibration module; 0005 Spec Kit adoption (with measured costs and the fenced-off commands). |
| S3 | `docs/documentation-standards.md`; CLAUDE.md, Documentation section | documentation rules | adopt spec-or-doc | M0, XI | S | Diátaxis, one mode per page. Mermaid for anything structural. ADRs are immutable: supersede them and update the old one's Status. External links only if actually opened; otherwise tag the claim [likely] or [speculative]. Relative links only. The ADR template (Status, Context, Decision, Consequences, Alternatives) is lighter than full MADR. |
| S4 | `docs/decisions.md` | running log in four sections (Decided / Corrected / Open / Deferred), plus "Known biases in this plan" | adopt spec-or-doc (the pattern) | M0 | S | Its content is mined into §3. The "Known biases" section applies to Vocal Wren as written: voice science designed with an LLM "is what wrong-but-confident looks like", so get an SLP review before v1.0. |
| S5 | `docs/spec-driven-development.md`; CLAUDE.md, Spec-driven development section | Spec Kit operating rules | adopt spec-or-doc | M0 | S | Rules listed below the table. |
| S6 | `specs/001-noise-floor-brightness/` | retrospective worked example of the Spec Kit loop | reference only | M0 | — | Its Constitution Check actually argued a principle (III) and forced a docs task (VII). It also splits verification honestly into automated checks and a manual check on a real display. |
| S7 | `.specify/templates/*`, `.specify/scripts/bash/*`, `.claude/skills/speckit-*` | stock Spec Kit v1.0.1 | **don't copy; reinstall the current Spec Kit** | M0 | S | All 22 files are hash-identical to the install manifest, and no `templates/overrides/` were used. |
| S8 | `.github/PULL_REQUEST_TEMPLATE.md` | PR test-plan template | adopt spec-or-doc | M0 | S | Every test-plan item gives exact steps, where to look and the expected result. Anything that can't be verified stays unchecked, with the reason. Pairs with A8. |
| S9 | `.gitattributes` | `* text=auto eol=lf` | adopt agent tooling (repo hygiene) | M0 | S | Matters on this Windows workstation for any `.sh` hook that gets ported. |

**S1 Governance rules to keep:**

- The constitution is standalone, not a pointer to CLAUDE.md.
- The constitution owns rules checkable against a plan; CLAUDE.md owns process.
- A conflict between the two is a bug in one of them.
- Amending the constitution needs an ADR and a semver bump.
- A violation of a NON-NEGOTIABLE principle is rejected outright, never "justified" in the Complexity Tracking table.

**S5 rules:**

- `/speckit-specify` consumes the issue rather than re-deriving it.
- Skip the loop for spikes.
- `/speckit-analyze` is not code review: it is read-only over spec, plan and tasks.
- The speckit skills ship with `disable-model-invocation: false`, so keeping them user-invoked is a rule, not a technical control.
- A `specify init` upgrade rewrites `.claude/settings.json` (ASCII escapes); revert that diff.
- **`/speckit-tasks` treats tests as optional unless asked for**, so Vocal Wren's principle X must require them. Spec 001 did this through its Quality Gates.
- The fence on `/speckit-taskstoissues` was about the GitHub board, so it is moot under qew.

### 2.7 Tests & fixtures

| ID | Source | What it is | Reuse mode | VW target | Effort | Notes |
|---|---|---|---|---|---|---|
| T1 | helpers in `src/dsp/index.test.ts` | synthetic signal generators | adopt test fixture (port to Rust test-support / vt-synth) | M2, F1 | S | Generators listed below the table. |
| T2 | `src/dsp/index.test.ts` (31 cases) | DSP acceptance cases | adopt test case | F1, M2 | S | **Pitch:** sines at 110/220/440 Hz recovered within 1 Hz (48 kHz, 2048 samples); silence, noise and an 8-sample window → null; invalid options throw. **Formants** (F0 150 Hz): the three vowels within ±40 Hz F1 / ±60 Hz F2 at 44.1 and 48 kHz; (500, 1500) at 16 kHz within ±45 / ±70 Hz; silence, NaN/∞, white noise and a 440 Hz sine → null; a too-short window throws. These tolerances say nothing about high-F0 behaviour. |
| T3 | `docs/formant-extraction.md`, Known limitations | error matrix: F0 150/220/280/350 Hz × /i a u/, at 48 kHz | adopt test case (as a regression table) | M1, M2 | S | Turn it into an accuracy table tracked in CI against Praat, rather than prose. |
| T4 | `src/calibration/index.test.ts` (26 cases) | calibration engine cases: state, validity, aggregation | adopt test case | F3 | S | Includes regression tests: wrong-shape readings throw; `formants: undefined` is treated as unvoiced; a redo replaces readings rather than accumulating them; "no level reading" is reported differently from "noisy". |
| T5 | `e2e/*.spec.ts`, `e2e/helpers/*` (11 cases) | end-to-end scenarios | adopt test case (as Android instrumented / Compose tests) | F3, F14, F15 | M | Scenarios listed below the table. The Playwright code itself isn't reusable. |

**T1 generators:**

- `sineWave`.
- `synthesizeVowel(f0, f1, f2, fs, dur)`: a naive sawtooth `2(φ−floor(φ+0.5))` through two cascaded 2-pole resonators. Coefficients: `r = e^(−πB/fs)`, `a1 = 2r·cos θ`, `a2 = −r²`, `b0 = 1−a1−a2`. Bandwidth B is 80 Hz for F1 and 100 Hz for F2.
- LCG noise `s = (s·1103515245 + 12345) & 0x7fffffff`, seed 42. JS doubles overflow 2^53, so this isn't a true LCG and a Rust port won't be bit-identical. That doesn't matter for its purpose.
- `realisticCaptureWindow`: a centred 2048-sample slice of a 0.5 s signal, which lets the filters settle.
- **Extend with:** F3, F0 from 150 to 400 Hz, higher formant sets, jitter, shimmer and breath noise. Compare against Praat.

**T5 scenarios:**

- Session start → frames → stop sets `endedAt`.
- The export matches the database.
- Delete-all empties everything. In Vocal Wren this must include calibration data.
- Cancelling the confirm dialog leaves data intact.
- Focus is restored after each action.
- A full wizard run saves 1 record and 100–400 frames (29 s at 10 Hz), with f0 vs formants split by step family.
- Cancelling saves nothing.
- Mutual exclusion engages on the tap itself, before the permission prompt resolves.
- Tests read the database directly, bypassing the store under test.

### 2.8 Agent tooling

| ID | Source | What it is | Reuse mode | VW target | Effort | Notes |
|---|---|---|---|---|---|---|
| A1 | `CLAUDE.md`, "How I work" and "Docs vs. specs" | working rules | adopt agent tooling | M0 | S | Show the diff first; push back bluntly; "done" requires naming edge cases, failure modes and what you'd test; tag [likely] / [speculative] and say "I don't know"; flag god modules. Ground truth is the code and the reference docs; roadmap, decisions and specs describe intent. Drop the board and WIP rules (qew replaces them). |
| A2 | `.claude/agents/dsp-numerics-auditor.md` | checks estimators against analytic ground truth | adopt agent tooling (re-ground for Rust) | M1, M2, X | S | Pure tones, harmonic series, silence and pathological input; states its tolerance before judging; scratch scripts only in /tmp. Re-target it at `cargo test` plus the Praat/parselmouth oracle. It caught real overclaims three times (`7dba395`, `9f11f3f`, `be3c6b4`). |
| A3 | `.claude/agents/docs-auditor.md` | audits the whole docs tree | adopt agent tooling | M0, XI | S | Checks for Diátaxis mixing, ADRs edited after acceptance (via `git log --follow`), dead relative links and wikilinks, and Mermaid diagrams that no longer match the code. It found 5 real drifts in `4bec825`. |
| A4 | `.claude/agents/debugger.md` | reproduce → isolate → report; never fixes | adopt agent tooling | M0 | S | Includes the discipline of always running `git bisect reset`. |
| A5 | `.claude/agents/reviewer.md` | reviews a diff against acceptance criteria and the non-negotiables | adopt agent tooling (rewrite the checklist for VW I–XI) | M0 | S | "Always state which edge cases the code does NOT handle." |
| A6 | `.claude/agents/accessibility-tester.md` | read-only accessibility audit (Read/Grep/Glob only) | adopt agent tooling (re-ground for Compose) | F15 | S | Re-target to Compose semantics, TalkBack, WCAG 2.2 AA contrast and target size, and throttled live regions. |
| A7 | `.claude/agents/wizard-{correctness,security,simplicity,performance,scrummaster}.md`, `.claude/skills/wizard-review`, `wizard-act`; **unmerged `5945c4f`** | persona-based PR review posted to GitHub, plus a plan-mode follow-up | adopt agent tooling (take the `5945c4f` versions) | M0 | M | Details below the table. |
| A8 | `.claude/hooks/check-test-plan.sh` + `.claude/settings.json` | blocks `gh pr merge/close` while the "## Test plan" section has unchecked `- [ ]` items | adopt agent tooling | M0 | S | Needs `jq` and `gh`. Add it as a second PreToolUse entry next to qew's hook. Check that qew doesn't already gate merges [unverified]. |
| A9 | `.claude/hooks/deny-bash-writes.sh` | regex denylist meant to keep read-only subagents read-only | reference only | — | — | Reviews found and patched at least 5 bypasses, and live firing was never verified (subagent definitions appear to be cached within a session). The repo's own Open item recommends an allowlist instead. Prefer narrowing the tool grant, as was done for accessibility-tester. |
| A10 | `.claude/agents/ledger-scribe.md`; `docs/ledger.md`; CLAUDE.md, Tracking section | GitHub Project board plus an in-repo ledger | don't carry over | — | — | The qew ledger replaces both. |

**A7 details:**

- **Modes.** The light default runs only the correctness persona. `deep` runs all 4 personas, a reaction round, and a Scrum Master summary.
- **Format.** Findings are tagged CONFIRMED or PLAUSIBLE, with reports capped at about 400 words.
- **Track record.** Most review-caught bugs in §3 came from these personas.
- **Rewrite the persona context.** They hardcode Web Audio, `tick()`, IndexedDB, and "data tied to a person's transition" (III).
- **Re-ground the performance persona on real-time rules:** no allocation or locking in the Oboe callback, and a per-hop time budget.

---

## 3. Lessons and pitfalls

### DSP

- **Normalisation and octave errors.** Normalising by whole-window energy penalised long lags, and taking the global-max lag gave octave-down errors (110 Hz came back as 55 Hz). Unit tests on sines caught both before ship (`bfd30d9`).
- **No voicing or level gate.** The 0.9 threshold doubles as the voicing gate. With no level gate, the scale-invariant NSDF accepts any periodic background, and its clarity value is thrown away (D1).
- **LPC order and sample rate.**
  - The LPC order was hardcoded at 12, and the PR claimed decimation made 44.1 and 48 kHz behave identically. Both were wrong: 16 kHz input was badly under-modelled.
  - The independent dsp-numerics-auditor caught it before merge (`7dba395`).
- **Understated formant bias.**
  - The first doc called the formant bias "a few percent", based on a single F0 (150 Hz).
  - The audit at 220–350 Hz found F1 errors of 12–25 %+, and one F2 off by about 49 % (`7dba395`).
- **Mitigations tested, none helped (`9f11f3f`).**
  - A higher LPC order made things worse.
  - Pitch-synchronous windowing changed errors by less than 1 point.
  - Root cause: at high F0 the harmonics are too sparse near a resonance for peak-picking to tell a harmonic from a resonance.
  - The next candidates were cepstral liftering and LPC root-solving (#67). Both were blocked by "no FFT, no new dependency", a rule that starved the DSP. In Rust, take an FFT crate (e.g. rustfft, MIT/Apache) from day one.
- **Unrealistic test windows.** Test fixtures used 0.5 s windows, about 12× the 2048 samples production code passes. Fixed in `111c4e0`; the existing tolerances still passed.
- **/u/ silently reports "no voice".** Closely spaced formants (/u/) collapse to one peak and return `null`, which looks the same as no voice. On real voices, corner-/u/ validity failures are likely. This was flagged but never measured.
- **The oracle was never built.**
  - The golden-file harness was scheduled first, then deferred, then promised "before custom DSP", then never built.
  - Custom LPC shipped on synthetic self-consistency tests alone (decisions.md §Corrected).
  - The wizard also samples a ~43 ms window every 100 ms, so over half of the calibration audio is never analysed.
- **Fragile range and level.** The comfortable range uses raw min/max (D5). Level is a smoothed spectral peak that is −∞ in silence, which `JSON.stringify` turns into `null` in exports, silently breaking the declared type (`f17524d`; still open).

### Capture and state

- **Retry paths missing initialisation.**
  - The suspended-retry path left `#info` unset (caught by lint, `c6bdce3`) and never allocated its buffers (`bfd30d9`).
  - Every way into the "active" state needs the same initialisation; extract it into one function.
- **Two capture owners raced.**
  - The instrument and the wizard each owned a `MicrophoneCapture`, and both could become active while a permission prompt was pending.
  - The PR description falsely claimed this was prevented.
  - The first regression test checked state after the prompt resolved, so it would never have caught the bug (`ad788b9`).
  - For Vocal Wren: one audio-engine owner, with exclusivity claimed synchronously.
- **Timing source.** Wall-clock timers were chosen for calibration steps because requestAnimationFrame is throttled in background tabs (`88d6777`). In Vocal Wren, time steps by audio frame count.
- **Button races.** Delete and export re-enabled their buttons in a race with capture starting (`c8218e7`).
- **Persistence gaps.** An abrupt exit leaves `endedAt` null; there is no quota handling and no migration path (`docs/session-store.md`).

### Data and privacy

- **Raw calibration frames.**
  - The spec required storing them, but the first PR dropped them; review caught it (`f686930`).
  - The wizard then shipped with an empty map (#56) until `7a5a1db` filled it.
  - Nothing ever reads them.
- **Delete and export are incomplete.** Both cover sessions only. A user's habitual F0, range and formants can be neither deleted nor exported. Vocal Wren's F14 must cover every store.
- **Untyped step readings.** A wrong-shaped reading reported a false "clear reading" and then crashed later. In JS `undefined !== null` is true, so a malformed reading counted as voiced (`1849d65`). Use typed enums instead of shape checks.

### UI and accessibility

- **Announcement flooding.** A polite live region at 10 Hz floods screen readers because announcements queue. The fix was a combined summary once per second (`fd95f50`).
- **Focus handling** (`c8218e7`, `b1a20c3`):
  - Disabling a button drops focus.
  - Unconditional `.focus()` steals focus.
  - Timers raced against cancel.
  - Identical text isn't re-announced.
- **Spectrogram floor.** Signal below the noise floor rendered the same black as a blank canvas (`5d895af`). The floor value (24 vs 8) was never checked on a real display.

### Process and tooling

- **Scope creep in a commit.** An unrelated CLAUDE.md section rode along in a feature commit (`f686930`). Review the whole file diff, not just the intended hunk.
- **CI hang.** The e2e job hung for 4h+ on apt mirror lookups. The fix was a prebuilt Playwright Docker image (`7377da1`). For Android CI, use images with the SDK and NDK preinstalled, and pin versions together.
- **Toolchain pin.** TypeScript 7 broke typescript-eslint, so TS was pinned to 6 (`c6bdce3`). Pin toolchains.
- **Regex hook.** The denylist hook had at least 5 bypasses and its live firing was never verified (`3ec0c07`).
- **Spec Kit cost.**
  - Adopting it cost 18,477 words of skill text, against 4,701 words for all 14 existing agent and skill definitions combined.
  - It is not cheaper, and it contains no code review (ADR 0005).
  - `/wizard-review`'s fan-out cost then led to the light-default change (`5945c4f`, unmerged).
- **Doc drift.** Drift happened despite the docs-in-same-commit rule:
  - The README status is stale.
  - The header of `src/store/calibration.ts` says the wizard isn't wired yet.
  - The `lpcOrder` JSDoc still says "Default 12".
  - One docs-auditor pass found 5 drifts (`4bec825`).
- **Decisions reversed or softened:**
  - "Custom FFT/LPC deferred until golden-file fixtures exist" was abandoned.
  - The blanket streak ban was narrowed to allow adherence streaks.
  - Strain caution was judged "quantitatively overtuned".
  - The `groomer` agent was retired in favour of `/speckit-specify`.
  - "Scrum Master always runs" was reversed (unmerged).
  - The GitHub Actions deferral was reversed.
  - The 20 Hz–Nyquist spectrogram axis vs the 60 Hz–8 kHz spec was never resolved.
- **Self-critique to keep.** `decisions.md` names its own known biases: planning over shipping, scope creep, no SLP curricula examined, and voice science designed by an LLM. Its own action item, an SLP review, never happened. Docs end up roughly the same size as the code. Budget the process.

---

## 4. Conflicts with the Vocal Wren constitution

| VW principle | What in voice-trainer conflicts | Action |
|---|---|---|
| I. On-device, no INTERNET or analytics | Aligned in spirit (ADR 0001). But two backlog ideas would need network access or a bundled model: an optional on-device LLM (transformers.js / WebLLM, with a large first-run download) and a "population-prior overlay". | Drop the LLM idea unless the model ships inside the APK. Bundle any priors. Treat export (a share hand-off) as an explicit user action, covered by an ADR. |
| II. Every metric has a confidence; hide it below a threshold | Estimators return a value or `null`. Clarity and prominence are computed, then discarded. Peak dB is always shown. Validity checks are pass/fail. | Add confidence outputs to D1, D2 and the level measure before porting. StrainSignal (K2) is the model to follow. |
| III. Targets, not identities; never store or infer gender | Detail below the table. | Strip the framing from anything carried over. Don't adopt voice-trainer's III as written; it would block F6. Never key estimator parameters, such as the formant ceiling, to sex. |
| IV. Not medical care | `strain.md` frames CPPS and jitter as dysphonia measures. The off-day flag has a "post-op" option. A prompt says "Say ahh, like at the doctor". Strain gets a "score". | Keep the reasoning; drop diagnostic language from user-facing text. Don't store health reasons. |
| V. Safety cues pre-empt training; session caps | Tier B has only a soft cap, and tier C stays fully accessible. `decisions.md` §Corrected relaxed strain caution as "quantitatively overtuned". No caps were implemented. | Adopt the tiers, but make the caps hard and the cues pre-emptive. Don't import the softening rationale. |
| VI. Encouragement, not coercion; no streak guilt | voice-trainer IV forbids congratulating the user and calling a trend "progress", which is stricter than Vocal Wren. Adherence streaks are allowed. | Settle it in an ADR: keep "no scores, verdicts or performance streaks"; allow encouragement; count adherence only in ways that can never read as broken. |
| VII. Visual-first accessibility, WCAG 2.2 AA, TalkBack | No conflict. The patterns are web-only, and no WCAG audit was ever done (it was explicitly out of scope). | Port the principles (U3, U4) and add real WCAG checks. |
| VIII. Coaching text as versioned content packs | Every string is hardcoded in TypeScript (`src/calibration`, `wizard.ts`, `describe-capture-error.ts`). | Extract them into vt-content v1 (K6). |
| IX. Rust core; real-time callbacks free of allocation and locks | The DSP allocates on every call. Analysis runs on the UI thread, every animation frame. There are two independent capture owners. | One Oboe owner, feeding a lock-free ring buffer read by an analysis thread. Preallocate everything. |
| X. Test-first, oracle-verified | Synthetic self-consistency tests only. The oracle harness was deferred three times and never built. No real-voice validation. | Treat D1 and D2 as unverified ports until the M2 Praat comparisons pass. |
| XI. MADR ADRs | Aligned: a light MADR format, immutable. | Adopt; switch to the full MADR fields if wanted. |
| No GPL/AGPL in the shipped binary | None present. `decisions.md` weighed GPL-3.0 for Resonance Scope itself but never chose a licence. | Choose a non-GPL licence for anything relicensed into Vocal Wren. |

**III detail:**

- **Identity framing.** The product is framed "for vocal feminization" across:
  - the README and CLAUDE.md;
  - the constitution preamble and `docs/index.md`;
  - ADR 0001 ("trans users");
  - the wizard-security persona ("tied to a person's transition").
- **Gendered targets and fixtures.** The docs call F0 220–350 Hz "feminization-training targets", and the test fixtures are male-average formants.
- **The reverse problem.** voice-trainer's own III forbids *all* presets and literature ranges, which is stricter than Vocal Wren's F6 allows.

---

## 5. Licensing

- **Repo licence:** none. There is no LICENSE file; the README says "Not yet decided", and `decisions.md` §Open weighs GPL-3.0 vs MIT. The default is therefore all rights reserved.
  - All 65 commits are by lvndrpup; there are no third-party contributors.
  - Most commits carry `Co-Authored-By: Claude (Sonnet 5 / Opus 5)` trailers.
  - You can relicense any of it into Vocal Wren. Record the provenance in a Vocal Wren ADR or NOTICE. (Not legal advice. The copyright status of AI-written portions is unsettled, but it doesn't restrict your own reuse.)
- **Third-party code:** none vendored.
  - Every algorithm is a textbook method implemented from scratch: NSDF/MPM, Levinson–Durbin, windowed-sinc FIR, Hamming window, parabolic interpolation, LPC envelope.
  - I found no copied snippets on reading.
- **Spec Kit files** (github/spec-kit v1.0.1): MIT [likely — verify against the upstream LICENSE]. Reinstall rather than copy.
- **npm:** 131 packages, **all `dev`**, with no runtime dependencies.
  - Licence counts: MIT 87, Apache-2.0 17, MPL-2.0 12, BSD-2-Clause 6, ISC 6, BSD-3-Clause 2, BlueOak-1.0.0 1.
  - The MPL-2.0 entries are lightningcss and its platform binaries, pulled in by Vite. The BlueOak entry is minimatch.
  - No GPL or AGPL, and nothing here ships in Vocal Wren.
- **Data and content:**
  - Peterson & Barney (1952) averages appear only as fixture numbers, which are facts plus a citation.
  - Cited papers are linked, not copied. One link points to a PDF re-hosted on a teaching site; don't re-host it.
  - **The real Borg CR10 scale (its anchors and layout) is copyrighted and licensed [likely].** The repo only says "CR10-style". For F8, design an original effort scale or license the real one.
  - Praat/parselmouth (GPL) is fine as a CI-only oracle; never ship it in the APK.

---

## 6. Recommended order of salvage

**M0 Foundations**

1. Governance and Quality Gates from S1 into the Vocal Wren constitution; make principle X require test tasks (S5).
2. CLAUDE.md working rules (A1), documentation standards (S3), and Vocal Wren ADRs modelled on S2: on-device, raw capture with session trust, persistence, crate boundaries. Write the layer-model ADR (U6).
3. `.gitattributes` (S9), the PR template (S8) and the `check-test-plan.sh` hook (A8).
4. Agents A3, A4 and A5; A2 re-grounded for Rust and Praat; A7 from `5945c4f`, rewritten for Vocal Wren.
5. Reinstall the current Spec Kit fresh (S7) and adopt the operating rules (S5).

**M1 Spikes**

1. **Pitch (D1):** FFT-based NSDF, relative k, clarity as confidence, and a level gate. Accept against the T2 pitch cases.
2. **Formants (D2):** a baseline port plus a root-solving variant; compare LPC order 10 vs 16. Use the T3 matrix as the acceptance test and record the outcome in an ADR.
3. **Capture (C1):** Oboe `Unprocessed` capture, with detection of AGC/NS/AEC effects. Supersede ADR 0002 with "detect, and record session trust".
4. **Spectrogram (D3 + U1):** a Compose ring-buffer spectrogram, with the U2 L* check on its colour map.

**M2 Corpus + oracle**

1. Port the T1 generators to Rust test-support. Extend them with F3, an F0 sweep and higher formant sets, with no sex labels.
2. Turn T2 and T3 into regression tables compared against Praat; A2 runs them.
3. Use the D7 notes to choose candidate vocal-weight metrics, measured on the corpus only.

**M3 v0.1 (F1–F4, F8 stub, F13, F15)**

- **F1:** whichever D1/D2 variants won in M1, RMS level in place of D6, and D4.
- **F2:**
  - C2 step 0.
  - The C3 noise-floor check, with its threshold re-derived in RMS units.
  - C5 "degrade, do not block".
  - Session trust from C1.
- **F3:**
  - C2 steps 1–5.
  - The C3 engine with Rust enums.
  - The C4 schema, including raw frames.
  - D5 using percentiles.
  - T4 cases and U5 UX.
- **F4:** U1, U2 and D3. No targets until a calibration exists (U6).
- **F8 stub:** the K2 interface, a self-report estimator at confidence 1.0, and the K3 tiers as data.
- **F13:** K5 progressive disclosure (instrument and calibration only in session 1) and the C2 prompt rules.
- **F15:** U3, U4, A6 and the T5 focus scenarios.
- **F14, if in scope:** C6, with delete and export covering calibration data too.

**M4 Content**

- Move the K6 strings into vt-content v1 with versioning. Review the tone (VI) and wording (IV), and write the K3/K4 coaching copy and the off-day copy.
- Get an SLP review, per S4.
- Exercise content has to be sourced fresh; this repo has none.

**M5 v1.0**

- K1 approaches 2 → 3 → 5: range geometry, then H1-H2 with formant correction, then the per-user classifier.
- The K7 adherence decision.
- C5 re-calibration triggers and drift detection.
- C4 recompute-from-raw.
- Opt-in, gated maximum-range capture (C2).

---

## 7. What NOT to bring over

- **Web platform code.** Don't carry `src/audio`, `src/store`, `src/render`, `main.ts`, `wizard.ts`, `dom.ts`, `tick-features.ts`, `describe-capture-error.ts` or `index.html`. They are specific to Web Audio, IndexedDB, Canvas and the DOM. Only their designs carry over (C1, C6, U1–U5).
- **Build and CI files.** Don't carry:
  - `package.json`, `package-lock.json`, `tsconfig.json`;
  - `eslint.config.mjs` (keep only the idea of enforcing boundaries mechanically, which the Cargo crate graph and Gradle module dependencies do natively);
  - `playwright.config.ts` and `ci.yml`.
- **The level measure and its thresholds**: the loudest spectral bin, AnalyserNode smoothing 0.8, the −50 dB noise floor. Wrong unit for Vocal Wren.
- **Weak estimator design choices**:
  - an absolute 0.9 as the only voicing gate;
  - an F0-steadiness threshold in Hz;
  - raw min/max for the range;
  - grid peak-picking as the final formant method.
- **Feminization framing and Resonance Scope naming**, including the database and export file names. Principle III, and the discretion lesson.
- **voice-trainer's constitution principles, verbatim.** Its III would block F6, its IV would block encouragement, and its V is TypeScript module layout.
- **Board and ledger process**: CLAUDE.md's Tracking section, `docs/ledger.md` and `ledger-scribe`. qew replaces them.
- **`deny-bash-writes.sh`**: a regex denylist with known weaknesses.
- **The stock Spec Kit files**: reinstall upstream instead.
- **From the unmerged branches:**
  - `.specify/feature.json` from `5945c4f`;
  - the whole `feat/calibration-raw-frame-persistence` branch.
- **Backlog ideas that break principle I**: a downloadable LLM, or anything that needs a backend (priors pooled from users, sync).
- **Stale comments**: the `lpcOrder` "Default 12" JSDoc and the `src/store/calibration.ts` header.

## Open questions / uncertainties

- **Provenance:**
  - Where "LPC order 10" came from (it isn't in this repo).
  - Whether any deployed Resonance Scope build differs from this repo.
- **Facts quoted from memory, to verify:**
  - the Peterson & Barney values;
  - Praat's defaults (order 10, 5000/5500 Hz ceilings);
  - Spec Kit being MIT;
  - Borg CR10 licensing.
- **Not tested here:**
  - The D1 level-gate problem was inferred from the code, not observed; nothing here was executed.
  - Whether qew already gates merges, which would overlap with A8.
