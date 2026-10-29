# Formants and resonance

*Learn, page 4 of 6. Previous: [The source–filter model](source-filter.md). Next:
[Vocal weight](vocal-weight.md).*

"Formant" is the word that sounds most like jargon and is the most worth knowing. It is
how voice science talks about the *filter* half of the voice, and it is the physics behind
what voice trainers call **resonance**.

## The tube, again

Picture the vocal tract as a tube about 17 cm long, nearly closed at the vocal folds and
open at the lips. A tube like that resonates when a quarter of a wavelength fits in it, and
again at 3 and 5 times that frequency. With the speed of sound at about 340 m/s, that puts
the resonances near **500, 1500 and 2500 Hz** [1]. Praat's manual does the same sum for a
16 cm tube and gets 550, 1650, 2750 Hz and up [2]. A neutral vowel like the one in
"heard" comes out close to these numbers [1].

The same physics scales with size: a shorter tube resonates higher, so a shorter vocal
tract has higher resonances overall [1][3].

## Resonance vs formant (two words, two things)

Strictly speaking [4][5]:

- A **resonance** (written R1, R2, R3 ...) is a property of the *tube*: a frequency it
  passes especially well.
- A **formant** (written **F1, F2, F3** ...) is a property of the *sound*: a broad peak in
  the spectral envelope, usually caused by a resonance. The Acoustical Society of America
  defines it as a range of frequencies with a maximum in the sound spectrum [4].

Usually the two are at nearly the same frequency, so many writers (and most of these
docs) use them interchangeably [4]. They can come apart, though, and when they do it
matters for Wren (see [below](#why-formants-get-hard-to-measure-at-high-pitch)). There is
even a third use: the "formants" an algorithm reports are often the poles of a
mathematical filter model, which are an estimate of the other two [4].

Formants are numbered from the bottom: **F1** is the lowest, **F2** the next, and so on.

> Naming clash: in Wren's roadmap, **F1–F16 are also feature IDs** (F1 Audio engine,
> F4 Live visual feedback, ...). In voice-science text, F1/F2/F3 mean formants. See the
> [glossary](../reference/glossary.md#f1-f2-f3-formants).

## What moves the formants

Your articulators reshape the tube, and each reshaping moves the resonances in a
predictable direction:

| Move | Effect | Source |
|---|---|---|
| Open the mouth / drop the jaw | **F1 rises** strongly (R1 spans about 200–800 Hz across vowels) | [1] |
| Move the tongue's narrowest point forward or back | **F2** changes most (about 800–2000 Hz in speech) | [1] |
| Widen the opening at the lips (spread) | resonances rise; narrowing it (rounding) lowers them | [1] |
| Lower the larynx (lengthen the tract) | formants fall; raising it raises them (which formants move most depends on the vowel) | [1][6] |

Two general rules from tube acoustics sit behind the table: widening the open end raises
the resonances, and narrowing or widening the tube at particular points raises or lowers
particular resonances depending on where along the standing wave the change happens [1].

**Vowels are mostly F1 and F2.** Listeners identify vowels largely from F1 and F2; F3 plays
a smaller role, and F4 and F5 mainly affect the voice's timbre [1]. Measured formants for
the same vowel vary a lot from speaker to speaker, and adjacent vowels crowd
together and overlap across speakers [10].

## What voice trainers mean by "resonance"

In voice training, "resonance" is used for the quality of the voice that comes from the
vocal tract rather than the folds: whether it sounds brighter or darker, smaller or larger,
separate from pitch. Speech-language pathologists assess it alongside pitch and voice
quality, and some clients aim at "moving resonance forward" [9].

Acoustically, the main correlate is where the formants sit. A longer vocal tract has lower
formants, and listeners use formant frequencies as a cue to the size of the speaker,
independently of pitch [3]. Higher formants overall therefore point towards a "smaller"-sounding
voice and lower ones towards a "larger" one. Trainers' "brighter" and "darker" map loosely
onto the same direction; that mapping is an interpretation, not a measured equivalence. In one small study,
voice therapy that targeted **spreading the lips and carrying the tongue further forward**
raised F1, F2 and F3, with F3 rising most [7]. Those are exactly moves from the table
above.

This is why Wren treats resonance as a **parameter with a direction** (brighter or darker,
in practice higher or lower formants), and why targets can be expressed relative to your
own baseline vowels (the [salvage audit](../salvage/voice-trainer.md) suggests "% shift from
your own corner vowels", P1).

Two honest caveats:

- Wren only measures what is in the sound. Whatever a singer or trainer *feels* when they
  talk about resonance is outside what a microphone can check.
- Brightness also depends on the *source*: a voice with stronger high harmonics sounds
  brighter too [1]. That overlaps with weight (see [Vocal weight](vocal-weight.md)).

## Why formants get hard to measure at high pitch

Here is the catch. The voice's spectrum is a comb of harmonics spaced F0 apart (see
[Sound and frequency](sound-and-frequency.md#harmonics)). The formant envelope is only
"visible" where a harmonic happens to land. You are trying to trace the shape of a hill
using only the fence posts that happen to stand on it.

- At F0 = 100 Hz there are posts every 100 Hz: plenty to trace a resonance about 100 Hz
  wide (a typical width for a vocal-tract resonance [4]).
- At F0 = 300 Hz there are posts every 300 Hz. A resonance between two harmonics may have
  only one post on it, or none.
- At the extreme, with a resonance at 500 Hz and F0 at 1000 Hz, there is no harmonic near
  500 Hz at all: the tract still has its resonance, but **the sound has no F1 peak** to
  measure [4].

Researchers who study high voices put it bluntly: the wide spacing of harmonics in high
voices can make it "impossible to define a formant" in the spectrum of a single note [11].
Measurement tools struggle accordingly. In a test on synthetic vowels, both LPC and
traditional spectrogram reading were accurate to about ±60 Hz for F0 between 100 and 300
Hz, but their accuracy "decreases greatly" from F0 = 350 Hz up [12]. One analysis of LPC
errors attributes an error of about 10 % of F0 to the harmonic spacing alone, which
matters most for voices above about 250 Hz [13][14].

The predecessor project measured this: first-formant errors of 12–25 % or more at F0
220–350 Hz, where they had been a few percent at 150 Hz, and two formants close together
(as in "oo") merging into one ([salvage audit](../salvage/voice-trainer.md), D2 and §3).

This matters a lot for a voice trainer, because many users will be practising exactly in
the higher range where measurement is weakest. Wren's answers:

- Every formant estimate carries a **confidence**; below threshold the app shows nothing
  (constitution principle II).
- [OQ-F](../open-questions.md) asks whether confidence should be **per formant**, so F2 can
  still be shown when F1 is unreliable.
- [OQ-O](../open-questions.md) notes that the oracle (Praat) will still report values at
  high pitch where Wren correctly declines, so tests need their own tolerances there.
- Praat's formant analysis needs a **formant ceiling** that suits the speaker's vocal tract
  length, and its manual notes that the difference between one person's front and back
  vowels can exceed the average difference between groups of speakers [8]. Wren will not
  pick that ceiling from a category of person; it uses a fixed value or one derived from
  your own calibration (salvage audit D2, recommendation 4; constitution principle III).

## Sources

1. Wolfe, J., Garnier, M. and Smith, J. (2009, updated online). *Voice Acoustics: an
   introduction to the science of speech and singing*. UNSW Music Acoustics, free web
   essay. <https://newt.phys.unsw.edu.au/jw/voice.html>
2. Boersma, P. and Weenink, D. *Praat manual: Source-filter synthesis 2. Filtering a
   source*.
   <https://www.fon.hum.uva.nl/praat/manual/Source-filter_synthesis_2__Filtering_a_source.html>
3. Smith, D. R. R., Patterson, R. D., Turner, R., Kawahara, H. and Irino, T. (2005).
   *The processing and perception of size information in speech sounds*. Journal of the
   Acoustical Society of America 117(1), 305–318. doi:10.1121/1.1828637. Free full text:
   <https://pmc.ncbi.nlm.nih.gov/articles/PMC2346562/>
4. Wolfe, J. *Formant: what is a formant?* Free web page.
   <https://newt.phys.unsw.edu.au/jw/formant.html>
5. Titze, I. R. and 21 co-authors (2015). *Toward a consensus on symbolic notation
   of harmonics, resonances, and formants in vocalization*. Journal of the Acoustical Society of America 137(5), 3005–3007.
   doi:10.1121/1.4919349. Free full text: <https://pmc.ncbi.nlm.nih.gov/articles/PMC5392060/>
6. Sundberg, J. and Nordström, P.-E. (1976). *Raised and lowered larynx – the effect on
   vowel formant frequencies*. STL-QPSR 17(2–3), 35–39. KTH, free PDF:
   <https://www.speech.kth.se/qpsr/1976/1976_17_2-3_035-039.pdf>
7. Carew, L., Dacakis, G. and Oates, J. (2007). *The effectiveness of oral resonance
   therapy on the perception of femininity of voice in male-to-female transsexuals*.
   Journal of Voice 21(5), 591–603. doi:10.1016/j.jvoice.2006.05.005. Abstract:
   <https://pubmed.ncbi.nlm.nih.gov/16822646/> (Small study, n = 10; the authors call it
   preliminary evidence. The title's framing is the paper's own, not Wren's.)
8. Boersma, P. and Weenink, D. *Praat manual: Sound: To Formant (burg)...*.
   <https://www.fon.hum.uva.nl/praat/manual/Sound__To_Formant__burg____.html>
9. American Speech-Language-Hearing Association (ASHA). *Practice Portal: Gender Affirming
   Voice and Communication*.
   <https://www.asha.org/practice-portal/professional-issues/gender-affirming-voice-and-communication/>
10. Hillenbrand, J., Getty, L. A., Clark, M. J. and Wheeler, K. (1995). *Acoustic
    characteristics of American English vowels*. Journal of the Acoustical Society of
    America 97(5), 3099–3111. doi:10.1121/1.411872. Abstract:
    <https://pubmed.ncbi.nlm.nih.gov/7759650/>. Free PDF (archived copy):
    <http://web.archive.org/web/20201112020803/https://homepages.wmich.edu/~hillenbr/Papers/HillenbrandGettyClarkWheeler.pdf>
11. Wolfe, J., Garnier, M. and Smith, J. (2009). *Vocal tract resonances in speech,
    singing, and playing musical instruments*. HFSP Journal 3(1), 6–23.
    doi:10.2976/1.2998482. Free full text: <https://pmc.ncbi.nlm.nih.gov/articles/PMC2689615/>
12. Monsen, R. B. and Engebretson, A. M. (1983). *The accuracy of formant frequency
    measurements: a comparison of spectrographic analysis and linear prediction*. Journal
    of Speech and Hearing Research 26(1), 89–97. doi:10.1044/jshr.2601.89. Abstract:
    <https://pubmed.ncbi.nlm.nih.gov/6223180/>
13. Vallabha, G. K. and Tuller, B. (2002). *Systematic errors in the formant analysis of
    steady-state vowels*. Speech Communication 38(1–2), 141–160.
    doi:10.1016/S0167-6393(01)00049-8. (Paywalled; claim taken from the summary in [14].)
14. Burris, C., Vorperian, H. K., Fourakis, M., Kent, R. D. and Bolt, D. M. (2014).
    *Quantitative and descriptive comparison of four acoustic analysis systems: vowel
    measurements*. Journal of Speech, Language, and Hearing Research. Free full text:
    <https://pmc.ncbi.nlm.nih.gov/articles/PMC3972630/>
