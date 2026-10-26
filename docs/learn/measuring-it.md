# Measuring it

*Learn, page 6 of 6. Previous: [Vocal weight](vocal-weight.md).*

The other pages describe the voice. This one describes how Wren will turn microphone
samples into numbers, and why some of those numbers are deliberately withheld. It covers
the plan as of milestone M0; the M1 spikes will settle the details in ADRs
([roadmap](../roadmap.md)).

## Frames: listening in short slices

A voice changes from moment to moment, so analysis works on short, overlapping slices of
audio called **frames** (or analysis *windows*). Each frame is treated as if the sound were
steady inside it, analysed, and turned into one set of numbers. Then the window slides
forward by a **hop** (Praat calls it the *time step*) and the process repeats [1][2].

Wren's core plans on roughly 100 frames a second, a 10 ms hop
([ADR-0006](../adr/0006-pure-kotlin-core-module.md)). The core's `Frame` type is one such
slice: a frame number, an F0 (or nothing) and the F0's confidence.

Frame length is a trade-off:

- **Long enough to see the pattern.** Pitch detection needs a few periods of the lowest
  pitch it might meet. Praat's pitch analysis uses a window of 3 periods of the pitch
  floor: 60 ms for a 50 Hz floor [2].
- **Short enough to follow change.** A longer window blurs fast movements [2]. Praat's
  formant analysis uses a much shorter effective window (25 ms by default) [3].
- **Frequency detail costs time.** The longer the window, the finer the frequency detail
  in its spectrum [3].

Each frame is also tapered at its edges by a *window function* (Hamming, Gaussian and so on)
so that the cut-off edges don't smear false frequencies across the spectrum [3][4].

## Pitch: does the wave match a shifted copy of itself?

Every mainstream pitch method in this family asks one question: *if I slide the waveform
along by some delay, does it line up with itself?* If the wave looks almost identical when
shifted by 5 ms, the F0 is probably 200 Hz [5].

Wren's estimator is based on the **McLeod pitch method (MPM)** [6], which the predecessor
project also used ([salvage audit](../salvage/voice-trainer.md), D1). In outline:

1. **Score every delay.** For each candidate delay τ, compute the **normalised square
   difference function (NSDF)**: a similarity score between the frame and itself shifted
   by τ, scaled so that it runs from −1 to +1, where +1 means a perfect match [6].
   Normalising this way means a quiet voice and a loud voice score the same [6]; the
   predecessor also found that normalising each delay by its own overlap stopped long
   delays being unfairly penalised (salvage audit §3, DSP).
2. **Find the peaks.** The NSDF has a peak at the true period, and also at 2×, 3× the
   period (because a wave that matches after one period also matches after two). MPM
   collects the main peaks ("key maxima") [6].
3. **Take the first good peak, not the biggest.** It picks the *first* key maximum that is
   at least a fraction *k* of the highest one. Picking the wrong peak gives a pitch error,
   "usually a 'wrong octave'" [6]. The predecessor saw exactly this when it took the
   biggest peak: a 110 Hz tone read as 55 Hz (salvage audit §3; see
   [Pitch and F0](pitch-and-f0.md#octave-errors-the-classic-pitch-tracker-mistake)).
4. **Refine.** Fit a parabola through the peak and its neighbours to get a delay between
   samples, and so a more precise F0 [6].
5. **Keep the score.** The height of the chosen peak, called the **clarity**, says how
   periodic the frame was [6]. Wren plans to use it as the F0's confidence
   ([salvage audit](../salvage/voice-trainer.md), D1 port notes).

The paper suggests *k* "usually in the range 0.8 to 1.0", says the method can work with as
little as two periods of the wave in the window, and computes the underlying correlation
quickly with an FFT [6]. It was built for real-time use with singers and instruments [6].

Because NSDF ignores loudness, any quiet periodic noise (a fan, mains hum) can look like a
voice. The salvage audit therefore recommends a separate level gate before trusting a
pitch (D1, change 4).

## Formants: LPC

Formants are peaks in the spectral *envelope*, but the spectrum we can compute directly is
a comb of harmonics (see [Formants and resonance](formants-and-resonance.md)). **Linear
predictive coding (LPC)** is the standard way to get a smooth envelope out of it [3][7].

The intuition: try to **predict each sample from the few samples before it**, using a fixed
recipe of weights. The best recipe for a frame is a compact description of the filter
that shaped the sound. Mathematically it is an *all-pole* filter: a filter made only of
resonances (poles) [7]. Voice researchers routinely model the vocal tract with such a
filter, and its poles fall close to the formants [16]. The frequency response of that filter is a smooth curve over the spectrum, and its
peaks are a good estimate of the spectral envelope [7]. The envelope's peaks (or, more
exactly, the filter's *poles*) are then taken as the formant estimates; Praat works this
way, and classic vowel studies measured their formants from LPC spectra [3][12].

Praat's standard formant method shows the practical steps [3]:

- **Resample** the sound to twice the *formant ceiling* (the top of the frequency range to
  search), so the model spends its effort where the formants are.
- **Pre-emphasise**: boost higher frequencies by about 6 dB per octave, because vowel
  spectra tend to fall by about that much and the model should fit the formant peaks, not
  the overall slope.
- **Fit** LPC with the Burg algorithm, with twice as many poles as the number of formants
  wanted (5 formants means 10 poles).
- **Discard** "formants" very near 0 Hz or near the ceiling, which are usually artefacts of
  the model fitting the spectral slope.

Two choices dominate the result: the **formant ceiling** and the **model order** (how many
poles). Too high a ceiling can merge two close formants into one [3]. The predecessor's
experiments found that a *higher* order made high-pitch errors much worse
([salvage audit](../salvage/voice-trainer.md), D2), which is one of the M1 spikes.

Solving for the poles directly ("root-solving") also yields each formant's **bandwidth**
(how sharp the peak is), which is a useful input to a formant confidence (salvage audit D2,
recommendation 1).

LPC has a known weak spot: at high F0, the harmonics are too sparse to define the
envelope, and formant errors grow with F0. See
[Formants and resonance](formants-and-resonance.md#why-formants-get-hard-to-measure-at-high-pitch).

## Confidence, and why Wren sometimes shows nothing

Every number above can be wrong in ways that look perfectly confident: an octave error, a
harmonic mistaken for a formant, a fan mistaken for a voice. People change how they use
their voice based on what the app tells them, so the constitution makes this rule
non-negotiable (principle II): **every user-facing metric carries a confidence computed in
the core, and below the threshold the app shows no number, no trend and no claim.**

Where the confidence comes from depends on the measure:

- **Pitch:** the MPM clarity, plus a level gate (above).
- **Formants:** planned from things like bandwidth and stability across frames, possibly
  per formant ([OQ-F](../open-questions.md)).
- **Weight measures:** planned to be logged but not shown until validated (see
  [Vocal weight](vocal-weight.md)).

The core's `Frame` already has this shape: `f0Hz` is null when nothing was measured, and
`f0Confidence` says how far to trust it.

## The oracle: checking against Praat

How do we know Wren's numbers are right? Constitution principle X requires DSP results to
be checked against an **oracle**: an independent, established tool run on the same audio.
Wren's oracle is **Praat** [8], driven from Python through **parselmouth** [9], running in
CI from milestone M2. Tolerances (how far Wren may differ from Praat) are loosened only
through an ADR. Praat and parselmouth are GPL-licensed, which is fine for a CI-only test
tool but means they must never ship in the app ([salvage audit](../salvage/voice-trainer.md)
§5; constitution licensing constraint) [8][9].

## Automatic gain control (AGC), and why it matters

Phones are built for calls, and their audio input can run the microphone signal through
processing such as **automatic gain control (AGC)**, which automatically turns the level up
when you are quiet and down when you are loud, to keep the output level steady. On some devices the platform inserts it by default,
depending on the input source [10]. Some
input sources also apply echo cancellation or noise reduction [14][15].

For a call that's helpful. For measurement it is a problem:

- **Loudness becomes meaningless.** If the phone keeps the level steady, the recording no
  longer shows how loudly you actually spoke. Level measures and anything compared across
  a session (such as "you got louder") stop meaning what they claim.
- **Weight gets confounded.** How bright or steep the spectrum is (spectral tilt) changes
  with how loudly you phonate: louder voices tend to have relatively stronger high
  harmonics [11][13]. With AGC on, the app can no longer tell "heavier because louder" from
  "heavier at the same loudness", a distinction weight training needs.
- **The spectrum itself can be altered** by noise suppression and similar processing,
  which can change the very envelope that formant and weight measures read.

Android offers two ways around it [14][15]:

- The `VOICE_RECOGNITION` input source. Android's compatibility rules say devices **must**,
  by default, disable noise reduction and automatic gain control on it, and **should** keep
  the frequency response roughly flat (±3 dB from 100 Hz to 4 kHz) [15].
- The `UNPROCESSED` input source (API 24+), which must have no processing other than a
  level multiplier. Supporting it is **optional**; apps check
  `AudioManager.PROPERTY_SUPPORT_AUDIO_SOURCE_UNPROCESSED`, and without support it behaves
  like the default source [14][15].

Android's own documentation also tells apps to check whether AGC is switched on [10]. Devices may
also fall short of the rules. So the M1 spikes include *detecting* AGC on the input path,
and the plan (building on the predecessor's capture design) is to detect it and lower the
session's trust rather than refuse to run ([roadmap](../roadmap.md) M1; salvage audit C1).

## Sources

1. Boersma, P. and Weenink, D. *Praat manual: Sound: To Formant (burg)...* (time
   step and analysis frames).
   <https://www.fon.hum.uva.nl/praat/manual/Sound__To_Formant__burg____.html>
2. Boersma, P. and Weenink, D. *Praat manual: Intro 4.2. Configuring the pitch
   contour*.
   <https://www.fon.hum.uva.nl/praat/manual/Intro_4_2__Configuring_the_pitch_contour.html>
3. Same page as [1] (settings and algorithm sections).
4. Smith, J. O. III (2011). *Spectral Audio Signal Processing*, section "Mathematical
   Definition of the STFT" (window function and hop size). CCRMA, Stanford University,
   free online book. <https://ccrma.stanford.edu/~jos/sasp/Mathematical_Definition_STFT.html>
5. Boersma, P. and Weenink, D. *Praat manual: how to choose a pitch analysis method*.
   <https://www.fon.hum.uva.nl/praat/manual/how_to_choose_a_pitch_analysis_method.html>
6. McLeod, P. and Wyvill, G. (2005). *A smarter way to find pitch*. Proceedings of the
   International Computer Music Conference (ICMC 2005), Barcelona. Free PDF (archived copy):
   <http://web.archive.org/web/20210206201756/http://www.cs.otago.ac.nz/tartini/papers/A_Smarter_Way_to_Find_Pitch.pdf>
7. Makhoul, J. (1975). *Linear prediction: A tutorial review*. Proceedings of the IEEE
   63(4), 561–580. doi:10.1109/PROC.1975.9792. Free scan hosted by IIT Kharagpur:
   <https://cse.iitkgp.ac.in/~ksrao/pdf/atsp/LP-tutorial.pdf>
8. Boersma, P. and Weenink, D. (1992–2026). *Praat: doing phonetics by computer*
   [computer program]. <https://www.praat.org>. Licence (GPL version 3 or later) stated in
   the source repository README: <https://github.com/praat/praat.github.io>
9. Jadoul, Y., Thompson, B. and de Boer, B. (2018). *Introducing Parselmouth: A Python
   interface to Praat*. Journal of Phonetics 71, 1–15. doi:10.1016/j.wocn.2018.07.001.
   Project page and licence (GPL version 3 or later):
   <https://github.com/YannickJadoul/Parselmouth>
10. Android Developers. *AutomaticGainControl* (API reference).
    <https://developer.android.com/reference/android/media/audiofx/AutomaticGainControl>
11. Wolfe, J., Garnier, M. and Smith, J. (2009, updated online). *Voice Acoustics: an
    introduction to the science of speech and singing*. UNSW Music Acoustics.
    <https://newt.phys.unsw.edu.au/jw/voice.html>
12. Hillenbrand, J., Getty, L. A., Clark, M. J. and Wheeler, K. (1995). *Acoustic
    characteristics of American English vowels*. Journal of the Acoustical Society of
    America 97(5), 3099–3111. doi:10.1121/1.411872. Free PDF (archived copy):
    <http://web.archive.org/web/20201112020803/https://homepages.wmich.edu/~hillenbr/Papers/HillenbrandGettyClarkWheeler.pdf>
13. Nordenberg, M. and Sundberg, J. (2004). *Effect on LTAS of vocal loudness variation*.
    Logopedics Phoniatrics Vocology 29(4), 183–191. doi:10.1080/14015430410004689.
    Abstract: <https://pubmed.ncbi.nlm.nih.gov/15764212/>
14. Android Developers. *MediaRecorder.AudioSource* and *AudioManager* (API reference).
    <https://developer.android.com/reference/android/media/MediaRecorder.AudioSource>,
    <https://developer.android.com/reference/android/media/AudioManager>
15. Android Open Source Project. *Android Compatibility Definition Document*, §5.4.2
    "Capture for Voice Recognition" and §5.11 "Capture for Unprocessed".
    <https://source.android.com/docs/compatibility/cdd>
16. Wolfe, J. *Formant: what is a formant?* UNSW Music Acoustics.
    <https://newt.phys.unsw.edu.au/jw/formant.html>
