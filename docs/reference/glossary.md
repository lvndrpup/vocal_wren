# Glossary

Terms used in Vocal Wren's docs, in alphabetical order, with a link to the
[Learn](../learn/README.md) page that explains each one. Sources for the facts are on the
linked pages.

Jump to: [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [H](#h) · [J](#j) ·
[L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) ·
[V](#v) · [W](#w)

## A

### ADR-*nnnn*
An **architecture decision record**: a short document, in MADR 4 format, recording one
significant decision with its context and alternatives. Numbered `ADR-0000`, `ADR-0001` ...
in [`docs/adr/`](https://github.com/lvndrpup/vocal_wren/tree/main/docs/adr). Agents propose them with status Proposed; only the owner accepts
them (constitution principle XI).

### AEC (acoustic echo cancellation)
Input processing that removes the phone's own speaker output from the microphone signal.
Useful for calls, unwanted for measurement. See [Measuring it](../learn/measuring-it.md#automatic-gain-control-agc-and-why-it-matters).

### AGC (automatic gain control)
Input processing that automatically raises the level of quiet sound and lowers loud sound
to keep the level steady. It hides how loud you really were and confounds weight
measures, so Wren plans to detect it (an M1 spike). See
[Measuring it](../learn/measuring-it.md#automatic-gain-control-agc-and-why-it-matters).

### Articulators
The movable parts that shape the vocal tract: tongue, jaw, lips, soft palate and so on.
Moving them moves the formants. See [Formants and resonance](../learn/formants-and-resonance.md#what-moves-the-formants).

### Autocorrelation
A measure of how well a signal matches a delayed copy of itself, as a function of the
delay. Pitch methods, including Praat's and NSDF, are built on this idea. See
[Measuring it](../learn/measuring-it.md#pitch-does-the-wave-match-a-shifted-copy-of-itself).

## B

### Bandwidth (of a formant)
How wide a formant peak is, in hertz: narrow means a sharp resonance. LPC root-solving
gives bandwidths, which can feed formant confidence. See
[Measuring it](../learn/measuring-it.md#formants-lpc).

### Baseline / calibration
A short guided recording of your own voice (quiet room, habitual pitch, a few vowels,
comfortable range) that later measures and targets are compared against. Features F2
(environment calibration) and F3 (baseline capture) in the [roadmap](../roadmap.md).

### Brightness
How bright or dark a voice sounds. It is linked loosely both to higher formants and to
stronger high harmonics, so it sits between resonance and weight. See
[Formants and resonance](../learn/formants-and-resonance.md#what-voice-trainers-mean-by-resonance).

### Burg (algorithm)
The method Praat uses to fit LPC coefficients for formant analysis. See
[Measuring it](../learn/measuring-it.md#formants-lpc).

## C

### Cepstral peak prominence (CPP, CPPS)
How much the voice's periodicity stands out from noise, measured on the *cepstrum* (a
spectrum of the log spectrum). Lower CPP goes with breathier or less periodic voice.
CPPS is the smoothed version. It is a candidate weight/quality measure, with caveats. See
[Vocal weight](../learn/vocal-weight.md#candidate-measure-3-cpp-cepstral-peak-prominence).

### Clarity
In the McLeod pitch method, the height of the chosen NSDF peak (up to 1): how periodic the
frame is. Wren plans to use it as the F0 confidence. See
[Measuring it](../learn/measuring-it.md#pitch-does-the-wave-match-a-shifted-copy-of-itself).

### Confidence
A value computed in the core alongside each user-facing metric, saying how far to trust
it. Below threshold, the app shows no number, trend or claim (constitution principle II).
In code: `Confidence`, e.g. `Frame.f0Confidence`. See
[Measuring it](../learn/measuring-it.md#confidence-and-why-wren-sometimes-shows-nothing).

### Content pack
A versioned bundle of coaching text kept outside the code, so wording can be reviewed and
changed without a rebuild (constitution principle VIII; milestone M4, feature F16).

### Corpus
The set of consented voice recordings, with hand-labelled vowels, used to test Wren's
measures against the oracle (milestone M2).

## D

### dB, dBFS
**Decibel**: a logarithmic unit for the ratio between two levels (×2 in power ≈ +3 dB; ×2
in pressure ≈ +6 dB). **dBFS** is dB relative to the largest value the recorder can
represent ("full scale"), so it is always 0 or negative. See
[Sound and frequency](../learn/sound-and-frequency.md#decibels).

### DFT / FFT
The **discrete Fourier transform** turns a frame of samples into its spectrum; the **fast
Fourier transform** is the fast algorithm for it. See
[Sound and frequency](../learn/sound-and-frequency.md#the-spectrum-a-sounds-recipe).

### DSP
**Digital signal processing**: the maths that turns audio samples into measurements. All of
Wren's DSP lives in the pure-Kotlin core (constitution principle IX).

## E

### Envelope (spectral envelope)
The smooth curve over the tops of a spectrum's harmonic peaks. Its peaks are the formants.
See [Sound and frequency](../learn/sound-and-frequency.md#the-spectrum-a-sounds-recipe).

## F

### F0 (fundamental frequency)
The rate at which the vocal folds vibrate, in hertz; the physical basis of pitch. In code,
`Frame.f0Hz`. A 2015 consensus paper recommends writing it *f*o (letter o, for
"oscillation"); most of the literature and these docs write F0. See
[Pitch and F0](../learn/pitch-and-f0.md).

### F1, F2, F3 (formants)
The first, second and third formants, counted from the lowest frequency. F1 tracks mouth
opening, F2 mainly tongue position; together they largely identify the vowel. **Not to be
confused with feature IDs F1–F16** (next entry). See
[Formants and resonance](../learn/formants-and-resonance.md).

### F*n* (feature IDs)
Features planned in the [roadmap](../roadmap.md), each to get a spec under `specs/`: F1
Audio engine, F2 Environment calibration, F3 Baseline capture, F4 Live visual feedback, F5
Coaching engine, F6 Targets & presets, F7 Guided training, F8 Safety, F9 Progress basics,
F13 Onboarding, F14 Privacy & data, F15 Accessibility baseline, F16 Content pipeline (F10–F12
are not yet listed). They share names with formants F1–F3; context tells them apart.

### Formant
A broad peak in the spectral envelope of a voice, produced by a resonance of the vocal
tract. Strictly, the *resonance* is the tract's property (R1, R2 ...) and the *formant* is
the sound's (F1, F2 ...), though they're usually used interchangeably. See
[Formants and resonance](../learn/formants-and-resonance.md#resonance-vs-formant-two-words-two-things).

### Formant ceiling
The top of the frequency range a formant analysis searches (Praat calls it "Formant
ceiling" or "maximum formant"). It should suit the vocal tract; Wren won't choose it from a
category of person. See [Formants and resonance](../learn/formants-and-resonance.md#why-formants-get-hard-to-measure-at-high-pitch).

### Frame
A short, overlapping slice of audio analysed as one unit; Wren plans about 100 per second.
Also the core type `Frame` (index, F0, F0 confidence). See
[Measuring it](../learn/measuring-it.md#frames-listening-in-short-slices).

### Frequency, hertz (Hz)
Repetitions per second. 1 Hz = one cycle per second; 1 kHz = 1000 Hz. See
[Sound and frequency](../learn/sound-and-frequency.md#frequency-and-hertz).

### Fundamental
The lowest harmonic of a periodic sound, at F0. See
[Sound and frequency](../learn/sound-and-frequency.md#harmonics).

## H

### H1–H2 (also H1–A1, H1–A3)
The level of the first harmonic minus the second, in dB. Higher values go with a more
breathy, less firmly closed voice; lower with a more pressed one. It needs correcting for
formants, depends on the vowel and F0, and raw values don't compare well between people. H1–A1 and H1–A3 compare H1 with the
harmonic nearest F1 or F3. See [Vocal weight](../learn/vocal-weight.md#candidate-measure-2-h1h2-the-first-two-harmonics).

### Habitual F0
A person's typical speaking pitch, summarised as the median F0 over voiced frames of
ordinary speech (salvage audit D4). See [Pitch and F0](../learn/pitch-and-f0.md#typical-ranges-without-labels).

### Harmonic
A component of a periodic sound at a whole-number multiple of F0 (F0, 2×F0, 3×F0 ...). See
[Sound and frequency](../learn/sound-and-frequency.md#harmonics).

### HNR (harmonics-to-noise ratio)
How much of a voice's energy is periodic versus noise, in dB. Like jitter and shimmer, it
is easily swamped by room and microphone effects. See [Vocal weight](../learn/vocal-weight.md).

## J

### Jitter and shimmer
Small cycle-to-cycle variations in the period (jitter) and amplitude (shimmer) of the
voice. Clinical-style measures; on phone or laptop microphones they "mostly measure the
room" (salvage audit D7), so Wren doesn't plan to show them. See
[Vocal weight](../learn/vocal-weight.md).

## L

### Larynx
The "voice box" in the throat that houses the vocal folds. Raising or lowering it shortens
or lengthens the vocal tract and moves the formants. See
[Formants and resonance](../learn/formants-and-resonance.md#what-moves-the-formants).

### Levinson–Durbin
A fast algorithm for solving the LPC equations from a frame's autocorrelation. See
[Measuring it](../learn/measuring-it.md#formants-lpc).

### LPC (linear predictive coding)
Predicts each sample from the previous few; the resulting all-pole filter gives a smooth
spectral envelope whose peaks are the formant estimates. Standard for formants; weak at
high F0. See [Measuring it](../learn/measuring-it.md#formants-lpc).

## M

### M*n* (milestones)
Roadmap milestones M0–M8: M0 Foundations, M1 Spikes, M2 Test corpus + oracle, M3 v0.1
internal, M4 Content packs, M5 v1.0 features, M6 SLP review, M7 Play closed test, M8 v1.0
release. See the [roadmap](../roadmap.md). **Not to be confused with** vocal-fold
mechanisms M0–M3 (see [Register](#register-mechanism)).

### MADR
"Markdown Architectural Decision Records", the template Wren's ADRs follow (version 4). See
[ADR-0000](../adr/0000-record-architecture-decisions.md).

### McLeod pitch method (MPM)
A pitch detector by McLeod and Wyvill (2005) based on the NSDF that picks the first strong
peak to avoid octave errors and reports a clarity value. The basis of Wren's F0 estimator.
See [Measuring it](../learn/measuring-it.md#pitch-does-the-wave-match-a-shifted-copy-of-itself).

## N

### Noise floor
The level of the background sound when nobody is speaking; measured in calibration (F2) so
quiet frames can be gated out.

### NS (noise suppression)
Phone input processing that removes steady background noise. Like AGC, it can change the
spectrum being measured. See [Measuring it](../learn/measuring-it.md#automatic-gain-control-agc-and-why-it-matters).

### NSDF (normalised square difference function)
The McLeod pitch method's similarity score between a frame and a delayed copy of itself,
from −1 to +1. See [Measuring it](../learn/measuring-it.md#pitch-does-the-wave-match-a-shifted-copy-of-itself).

### Nyquist frequency
Half the sample rate: the highest frequency a sampled signal can represent (24 kHz at 48
kHz). See [Sound and frequency](../learn/sound-and-frequency.md#sound-is-a-pressure-wave).

## O

### Octave, octave error
An **octave** is a doubling of frequency. An **octave error** is a pitch tracker reporting
half or double (or another multiple of) the true F0. See
[Pitch and F0](../learn/pitch-and-f0.md#octave-errors-the-classic-pitch-tracker-mistake).

### OQ-*x* (open questions)
Questions waiting for the owner's answer, listed in [open-questions.md](../open-questions.md)
with a letter each (e.g. OQ-F, per-formant confidence; OQ-O, oracle tolerances at high
pitch).

### Oracle
An independent, trusted tool whose results Wren's measurements are checked against in CI.
Wren's oracle is Praat, driven through parselmouth (constitution principle X). See
[Measuring it](../learn/measuring-it.md#the-oracle-checking-against-praat).

## P

### parselmouth
A Python library that runs Praat's own analysis code, used to drive the oracle in CI.
GPL-licensed, so it never ships in the app. See
[Measuring it](../learn/measuring-it.md#the-oracle-checking-against-praat).

### Pitch
The *perceived* highness or lowness of a sound. For voices it closely follows F0, but it is
a perception, not a measurement. See [Pitch and F0](../learn/pitch-and-f0.md#pitch-what-you-hear).

### Praat
Free phonetics software by Paul Boersma and David Weenink, widely used for voice and
speech analysis, and Wren's oracle. GPL-licensed. See
[Measuring it](../learn/measuring-it.md#the-oracle-checking-against-praat) and its
[manual](https://www.fon.hum.uva.nl/praat/manual/Intro.html).

### Pre-emphasis
Boosting higher frequencies (about +6 dB per octave) before LPC, so the model fits the
formant peaks rather than the overall downward slope. See
[Measuring it](../learn/measuring-it.md#formants-lpc).

## Q

### qew, qew item IDs
qew is the work ledger that tracks all of Wren's work ([ADR-0003](../adr/0003-qew-work-ledger.md)).
Issues and tasks have 9-character time-based IDs such as `043ea313v`; epics (phases) have
letters (`A`, `B`, ...). Commits carry a `Refs: <qew id>` trailer.

## R

### Register (mechanism)
A distinct way the vocal folds vibrate. M0 is creak/vocal fry, M1 chest or modal voice (more
of the folds vibrating), M2 head voice or falsetto (less), M3 whistle. Closely related to
weight. See [Pitch and F0](../learn/pitch-and-f0.md#registers).

### Resonance
In acoustics, a frequency that the vocal tract passes especially well (R1, R2 ...),
producing a formant. In voice training, the perceived brightness/darkness or "size" of a
voice, carried mainly by formant frequencies. One of Wren's three training parameters. See
[Formants and resonance](../learn/formants-and-resonance.md).

### RMS (root mean square)
A standard measure of a signal's average level over a frame; Wren plans to report level as
RMS in dBFS (salvage audit D6).

## S

### Sample rate
How many samples per second a recording has. Wren plans 48 kHz. See
[Sound and frequency](../learn/sound-and-frequency.md#sound-is-a-pressure-wave).

### Semitone
One twelfth of an octave: a frequency ratio of about 1.059. Wren prefers semitones to hertz
for pitch changes. See [Pitch and F0](../learn/pitch-and-f0.md#octaves-and-semitones).

### SLP (speech-language pathologist)
A clinician who assesses and treats voice and speech problems. See one for pain,
lasting hoarseness or voice loss. An SLP reviews Wren's content before v1.0 (milestone M6).

### Source–filter model
The voice as a source (vocal folds making a buzz) shaped by a filter (the vocal tract). See
[The source–filter model](../learn/source-filter.md).

### Spectral tilt
How quickly harmonic levels fall as frequency rises. Steeper tilt sounds darker, softer or
breathier; flatter tilt brighter and more pressed or louder. A main acoustic correlate of
weight. See [Vocal weight](../learn/vocal-weight.md#candidate-measure-1-spectral-tilt).

### Spectrogram
A picture of sound over time: time left to right, frequency bottom to top, energy as
darkness or colour. See [Sound and frequency](../learn/sound-and-frequency.md#the-spectrum-a-sounds-recipe).

### Spectrum
The amounts of each frequency in a short piece of sound. See
[Sound and frequency](../learn/sound-and-frequency.md#the-spectrum-a-sounds-recipe).

### Spike
A short, time-boxed experiment that answers one technical question and ends in an ADR
(milestone M1).

### Strain
Excess effort or tension in voicing. Wren's safety logic (F8) aims to detect it, starting
from self-report, and to put safety cues ahead of training cues (constitution principle V).

## T

### Timbre
Whatever makes two sounds of the same pitch and loudness sound different; mostly the shape
of the spectrum. See [Sound and frequency](../learn/sound-and-frequency.md#the-spectrum-a-sounds-recipe).

### Tolerance
How far Wren's result may differ from the oracle's before a test fails. Changed only through
an ADR (constitution principle X).

## V

### Vocal folds
Two folds of tissue in the larynx whose vibration makes voiced sound (sometimes, misleadingly,
called "vocal cords"). See [The source–filter model](../learn/source-filter.md#the-source-the-vocal-folds).

### Vocal tract
The air passage from the vocal folds to the lips (and nose): the voice's filter. See
[The source–filter model](../learn/source-filter.md#the-filter-the-vocal-tract).

### Voicing
Whether a frame contains vocal-fold vibration at all. A pitch is only reported for voiced
frames. See [Measuring it](../learn/measuring-it.md#pitch-does-the-wave-match-a-shifted-copy-of-itself).

## W

### Weight (vocal weight)
A voice-training term for how light or heavy a voice sounds, linked to how much of the
vocal folds vibrate and how firmly they close. It has no single agreed acoustic definition;
candidate correlates are spectral tilt, H1–H2 and CPP. One of Wren's three training
parameters. See [Vocal weight](../learn/vocal-weight.md).

### Window, hop
The **window** is a frame's length (and the taper applied to its edges); the **hop** (Praat:
time step) is how far the window moves between frames. See
[Measuring it](../learn/measuring-it.md#frames-listening-in-short-slices).
