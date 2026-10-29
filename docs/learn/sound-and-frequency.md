# Sound and frequency

*Learn, page 1 of 6. Next: [Pitch and F0](pitch-and-f0.md).*

Everything Wren measures starts as a wobble in air pressure. This page covers the handful
of ideas the rest of Learn builds on: waves, hertz, harmonics, the spectrum and the
decibel.

## Sound is a pressure wave

When you speak, your voice pushes the air in front of you into tiny, rapid ups and downs
of pressure. A microphone is just a pressure sensor: it turns those ups and downs into a
voltage, and a converter in the phone turns that voltage into a stream of numbers, one
per *sample* [1]. Wren records at 48,000 samples per second (48 kHz), as planned in the
[roadmap](../roadmap.md) M1 spikes.

A sampled signal can only describe frequencies up to half its sample rate, a limit called
the **Nyquist frequency** (also called the Nyquist limit) [6]. At 48 kHz that is 24 kHz, comfortably above everything the
voice analysis needs.

## Frequency and hertz

If a pattern repeats, the time one repetition takes is its **period**, and the number of
repetitions per second is its **frequency** [2]. Frequency is measured in **hertz (Hz)**:
1 Hz is one cycle per second, and 1 kHz is 1,000 Hz [1]. Frequency and period are two views
of the same thing: *f* = 1/*T* [2]. A wave that repeats every 5 milliseconds has a
frequency of 1/0.005 s = 200 Hz.

The simplest possible wave is a **sine wave** (a "pure tone"), which contains exactly one
frequency [1].

## Harmonics

A voice is not a pure tone. When a sound repeats exactly (it is *periodic*), it can always
be rebuilt by adding together sine waves at the repetition frequency *f* and its whole-
number multiples 2*f*, 3*f*, 4*f* and so on. Each of these components is a **harmonic**;
the lowest one, *f* itself, is the **fundamental** [2]. This is Fourier's theorem, and it
works in reverse too: adding up harmonics always gives a periodic wave [2].

So a voice humming at 200 Hz is really a stack of components at 200, 400, 600, 800 Hz and
up. Those components are spaced exactly *f* apart, which matters later: **the higher the
voice, the wider the gaps between harmonics** (see
[Formants and resonance](formants-and-resonance.md)).

Voiced speech is close to periodic because the vocal folds vibrate in a way that is not a
simple sine, so the sound they make is rich in harmonics [3].

## The spectrum: a sound's recipe

A **spectrum** shows how much of each frequency is in a short piece of sound. Think of it
as a recipe: "this much of 200 Hz, this much of 400 Hz, ..." [1]. Software computes it
with a discrete Fourier transform (DFT; the fast algorithm is the FFT) over a short sample
of the recording [1]. For a voiced sound the spectrum looks like a comb: a row of evenly
spaced spikes, one per harmonic.

The heights of those spikes are what make an "ah" sound different from an "ee" at the
same pitch and loudness. Whatever differs between two sounds of equal pitch and loudness
is, by definition, their **timbre** [1].

The smooth curve you could draw over the tops of the spikes is the **spectral envelope**.
It is the shape of the recipe, independent of which pitch is being sung, and it is where
formants live ([Formants and resonance](formants-and-resonance.md)).

A **spectrogram** is many spectra side by side over time: time runs left to right,
frequency bottom to top, and darkness or colour shows energy [4]. It is the picture most
voice tools (including Praat) show you.

## Decibels

Sound levels cover an enormous range, so they are measured on a logarithmic scale, the
**decibel (dB)**. A decibel value always describes a *ratio* between two quantities
[5]:

- For power: level difference = 10 log₁₀(*P*₂/*P*₁). Doubling the power adds about 3 dB [5].
- For pressure or amplitude: level difference = 20 log₁₀(*p*₂/*p*₁). Doubling the pressure
  adds about 6 dB [5].

Because dB is a ratio, a dB number only means something once you know the reference.
Wren's own levels will be in **dBFS** (dB relative to the loudest value the recorder can
represent, so 0 dBFS is the top and everything else is negative). That is a property of
the recording, not of how loud you were in the room; see [Measuring it](measuring-it.md).

Human hearing is not equally sensitive at all frequencies: most people are most sensitive
around 1–4 kHz and less sensitive at low and very high frequencies [7].

## Why this matters for Wren

- **Pitch** is about the spacing of the harmonics (the fundamental). See
  [Pitch and F0](pitch-and-f0.md).
- **Resonance** is about the shape of the spectral envelope. See
  [Formants and resonance](formants-and-resonance.md).
- **Weight** is (roughly) about how fast the harmonics fade as you go up in frequency. See
  [Vocal weight](vocal-weight.md).

## Sources

1. Wolfe, J. *What is a Sound Spectrum?* Free web page.
   <https://newt.phys.unsw.edu.au/jw/sound.spectrum.html>
2. Wolfe, J. *How harmonic are harmonics?* Free web page.
   <https://newt.phys.unsw.edu.au/jw/harmonics.html>
3. Wolfe, J., Garnier, M. and Smith, J. (2009, updated online). *Voice Acoustics: an
   introduction to the science of speech and singing*. UNSW Music Acoustics, free web
   essay. <https://newt.phys.unsw.edu.au/jw/voice.html>
4. Boersma, P. and Weenink, D. *Praat manual: Intro 3.1. Viewing a spectrogram*.
   <https://www.fon.hum.uva.nl/praat/manual/Intro_3_1__Viewing_a_spectrogram.html>
5. Wolfe, J. *dB: What is a decibel?* Free web page.
   <https://newt.phys.unsw.edu.au/jw/dB.html>
6. Smith, J. O. III. *Mathematics of the Discrete Fourier Transform (DFT)*, section
   "Sampling Theorem". CCRMA, Stanford University, free online book.
   <https://ccrma.stanford.edu/~jos/mdft/Sampling_Theorem.html>
7. Wolfe, J. *Hearing test on-line: sensitivity, equal loudness
   contours and audiometry*. Free web page. <https://newt.phys.unsw.edu.au/jw/hearing.html>
