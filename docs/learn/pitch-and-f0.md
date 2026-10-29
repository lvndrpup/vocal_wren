# Pitch and F0

*Learn, page 2 of 6. Previous: [Sound and frequency](sound-and-frequency.md). Next:
[The source–filter model](source-filter.md).*

Pitch is the dial most people think of first. Voice science uses two words for it, and the
difference matters for an app that claims to measure it.

## F0: the physical number

When your vocal folds vibrate, the sound repeats once per vibration. The repetition rate is
the **fundamental frequency**, written **F0** (say "F-zero" or "F-nought") and measured in
hertz [1][2]. (A 2015 consensus paper on notation recommends writing it *f*o, with the
letter o for "oscillation" [10]; most of the literature, and these docs, still write F0.)
If the folds open and close 200 times a second, F0 is 200 Hz, and the
voice's harmonics sit at 200, 400, 600 Hz and so on (see
[Sound and frequency](sound-and-frequency.md#harmonics)).

F0 is a property of the signal. It can be measured, and it is what Wren's core reports
(`Frame.f0Hz` in [`android/core`](../../android/core/src/main/kotlin/dog/lavenderpuppy/vocalwren/core/Frame.kt)).

## Pitch: what you hear

**Pitch** is a *perception*: how high or low a sound seems to a listener. It depends mainly
on frequency, but also, weakly, on loudness and on the mix of harmonics [3]. For a voice,
perceived pitch follows F0 very closely, which is why the two words are often used interchangeably. But they are not the same
thing. A classic demonstration is the **missing fundamental**: if you remove the 200 Hz
component from a voice and keep 400, 600, 800 Hz and up, listeners still hear a pitch of
200 Hz, because for periodic sounds our sense of pitch follows the spacing of the
harmonics [4].

So: Wren *measures* F0, and talks about pitch because that is what you experience.

## Octaves and semitones

Musical pitch works on ratios, not differences. Going up an **octave** means doubling
the frequency: 100 → 200 Hz is an octave, and so is 200 → 400 Hz [5]. An octave is divided
into 12 **semitones**, each a frequency ratio of 2^(1/12), about 1.059 [5]. A step of
*n* semitones from *f*₁ to *f*₂ is

    n = 12 × log₂(f₂ / f₁)

This is why voice trainers (and Wren) prefer semitones to hertz for *changes*: a 20 Hz rise
is a big step at 100 Hz (about 3.2 semitones) and a small one at 300 Hz (about 1.1
semitones). The salvage audit makes the same point about steadiness thresholds
([`docs/salvage/voice-trainer.md`](../salvage/voice-trainer.md), C3).

## Typical ranges, without labels

Voices vary enormously, and Wren never assumes a range from who you are (constitution
principle III). Some reference numbers, stated as ranges of the voice in general:

- **Speech** F0 is typically somewhere in 100–400 Hz; **singing** can run from about 60 Hz
  to over 1500 Hz [1].
- Very low, creaky phonation ("vocal fry") can go down to about 30 Hz, and children
  yelling can approach 2000 Hz [6].
- Praat's standard analysis range for pitch (filtered autocorrelation) is 50–800 Hz, and
  its authors note that this range "may not have to be adapted" to the speaker [6][7].
- In a classic study of 139 adult and child talkers reading the same vowels, the average
  F0 for each vowel within each talker group fell between about 120 Hz and about 250 Hz
  [9]. Those are averages of averages; individual voices spread further.

Within one person, speaking F0 moves constantly: up and down within each phrase and
syllable [1]. That is why a single "my pitch" number is usually summarised as a typical
(median) value over a stretch of speech, plus a range (salvage audit D4 and D5).

### Registers

The folds can vibrate in different ways, called **mechanisms** or **registers** [1]:

- **M0**, creak or vocal fry: so slack that the vibration is irregular and has no clear
  pitch [1]. Pitch trackers may report creak as voiceless, for example when it drops below
  their pitch floor [11]; Wren should hide F0 here rather than guess.
- **M1**, often called chest or modal voice: nearly the whole mass and length of the folds
  vibrates, and the glottis is open for a relatively short part of each cycle [1].
- **M2**, often called head voice or falsetto: a smaller part of the folds vibrates and the
  glottis is open for longer [1].

Singers typically switch from M1 to M2 somewhere around 350–370 Hz, often called the
"break" [1].
Register is closely tied to what voice trainers call weight; see
[Vocal weight](vocal-weight.md).

## Octave errors: the classic pitch-tracker mistake

Pitch trackers look for the time shift at which the waveform best matches itself (see
[Measuring it](measuring-it.md)). A wave that repeats every 5 ms (200 Hz) also matches
itself after 10 ms and 15 ms. If noise makes the 10 ms match look slightly better, the
tracker reports 100 Hz: an **octave drop** [7]. Going the other way, a strong harmonic can
be mistaken for the fundamental. Praat's manual gives the example of F0 = 150 Hz with the
first formant at 450 Hz, exactly three times F0, sometimes being read as 450 Hz [7]. Gross
errors like these, reading "too low" (often half, or a lower fraction of, the true F0) or
"too high", are the typical failure of autocorrelation-style methods [8]. They are
commonly called **octave errors**, although the YIN paper points out that the wrong value
is not always exactly an octave away [8].

The predecessor project hit exactly this: a 110 Hz test tone came back as 55 Hz until the
algorithm was fixed ([salvage audit](../salvage/voice-trainer.md), §3 DSP).

For a trainer, an octave error is worse than no reading: it tells someone their voice
dropped by 12 semitones when it didn't. That is why each F0 in Wren carries a confidence
and is hidden when the confidence is low (constitution principle II; see
[Measuring it](measuring-it.md#confidence-and-why-wren-sometimes-shows-nothing)).

## Sources

1. Wolfe, J., Garnier, M. and Smith, J. (2009, updated online). *Voice Acoustics: an
   introduction to the science of speech and singing*. UNSW Music Acoustics, free web
   essay. <https://newt.phys.unsw.edu.au/jw/voice.html>
2. Boersma, P. and Weenink, D. *Praat manual: how to choose a pitch analysis method*
   (also the source for octave drops and rises, below).
   <https://www.fon.hum.uva.nl/praat/manual/how_to_choose_a_pitch_analysis_method.html>
3. Wolfe, J. *Frequency and pitch* (UNSW physics animations). Free web page.
   <https://www.animations.physics.unsw.edu.au/jw/frequency-pitch-sound.htm>
4. Wolfe, J. *Music acoustics FAQ: What is the frequency, and how does it relate to
   pitch?* UNSW Music Acoustics. <https://newt.phys.unsw.edu.au/jw/musFAQ.html#pitch>
5. Wolfe, J. *Note names, MIDI numbers and frequencies*. UNSW Music Acoustics.
   <https://newt.phys.unsw.edu.au/jw/notes.html>
6. Boersma, P. and Weenink, D. *Praat manual: Intro 4.2. Configuring the pitch contour*.
   <https://www.fon.hum.uva.nl/praat/manual/Intro_4_2__Configuring_the_pitch_contour.html>
7. Same page as [2], sections on octave drops and rises.
8. de Cheveigné, A. and Kawahara, H. (2002). *YIN, a fundamental frequency estimator for
   speech and music*. Journal of the Acoustical Society of America 111(4), 1917–1930.
   doi:10.1121/1.1458024. Free PDF (archived copy):
   <http://web.archive.org/web/20201112014247/http://audition.ens.fr/adc/pdf/2002_JASA_YIN.pdf>
9. Hillenbrand, J., Getty, L. A., Clark, M. J. and Wheeler, K. (1995). *Acoustic
   characteristics of American English vowels*. Journal of the Acoustical Society of
   America 97(5), 3099–3111. doi:10.1121/1.411872. Abstract:
   <https://pubmed.ncbi.nlm.nih.gov/7759650/>. Free PDF (archived copy):
   <http://web.archive.org/web/20201112020803/https://homepages.wmich.edu/~hillenbr/Papers/HillenbrandGettyClarkWheeler.pdf>
10. Titze, I. R. and 21 co-authors (2015). *Toward a consensus on symbolic notation of
    harmonics, resonances, and formants in vocalization*. Journal of the Acoustical Society
    of America 137(5), 3005–3007. doi:10.1121/1.4919349. Free full text:
    <https://pmc.ncbi.nlm.nih.gov/articles/PMC5392060/>
11. Boersma, P. and Weenink, D. *Praat manual: FAQ: Pitch analysis*.
    <https://www.fon.hum.uva.nl/praat/manual/FAQ__Pitch_analysis.html>
