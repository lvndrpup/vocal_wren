# Vocal weight

*Learn, page 5 of 6. Previous: [Formants and resonance](formants-and-resonance.md). Next:
[Measuring it](measuring-it.md).*

Weight is Wren's third training parameter, after pitch and resonance. It is also the least
settled, scientifically. This page explains what voice trainers mean by it, which
measurements might track it, and where the evidence stops. Read it as "best current
understanding", not settled fact.

## What "weight" means

Say "uh-oh" lightly, almost floating, then say it again like a firm, solid statement at the
same pitch. The second will probably sound **heavier**. Voice trainers use **weight** for
that light–heavy dimension: a quality separate from how high the voice is (pitch) and how
bright or dark its colour is (resonance).

The usual physiological story is that perceived weight follows the **vibrating mass of the
vocal folds**: how much of the folds' thickness takes part in each vibration, which in turn
affects how long the folds stay open in each cycle (the *open quotient*) and how steeply
the harmonics fall off (*spectral slope*) [1]. That fits what we know about registers: in
M1 ("chest") nearly the whole mass of the folds vibrates and the glottis is open for a
short part of each cycle, while in M2 ("head") a smaller part vibrates and the glottis is
open longer [2] (see [Pitch and F0](pitch-and-f0.md#registers)). In computer models,
thicker vibrating folds give a flatter spectrum, with relatively stronger high harmonics
[3].

### How uncertain is this?

Quite. Researchers studying these perceptual qualities say so directly:

- One group notes "more ambiguity" in voice-quality terms when it comes to precise
  definitions, "especially for weight" [4].
- Even trained listeners agree on weight less than on the other qualities they rated,
  which the authors take to mean "labelling weight is a more difficult task" [1].
- A detailed single-speaker study found that weight "has yet to be strongly correlated
  with concrete metrics", and that apart from loudness, the acoustic measures tried failed
  to rank weight independently of other qualities [5].

So weight has **no single agreed acoustic definition**. The measures below are
*candidates*. Wren's plan, inherited from the predecessor project, is to log them on the
test corpus and not show them to users until they are validated (salvage audit D7, and
milestone M2 in the [roadmap](../roadmap.md)). This is constitution principle II in
action.

## Candidate measure 1: spectral tilt

Remember that the voice source is a stack of harmonics that usually get weaker as frequency
goes up (see [The source–filter model](source-filter.md#the-source-the-vocal-folds)). How
fast they fall is the **spectral tilt** (or spectral slope) [2].

- **Steeper tilt** (high harmonics weak): sounds darker, softer or breathier. A breathy
  voice, where the folds never fully close, has a strongly sloping spectrum [2]. A more
  open glottis gives relatively stronger low-frequency and weaker high-frequency
  components [6].
- **Flatter tilt** (high harmonics strong): sounds brighter and fuller. Loud voice, with a
  rapid closure of the folds and a short open phase, has a flatter spectrum [2].

The intuition for weight: a heavier voice tends to have the flatter tilt of firm, full
closure; a lighter voice the steeper tilt of a gentler, shorter contact [1][3].

The big confound is **loudness**. As you get louder, the high frequencies grow faster than
the low ones: in one study, the level around 1.5–3 kHz rose about 1.5 dB for every 1 dB
rise in overall level, against about 0.5 dB at low frequencies [7]. In soft voice the
fundamental is usually the strongest component; in loud voice an overtone usually is [8].
So a tilt measure can't tell "heavier" from "louder" unless loudness is accounted for.
This is one reason automatic gain control is such a problem (see
[Measuring it](measuring-it.md#automatic-gain-control-agc-and-why-it-matters)).

## Candidate measure 2: H1–H2, the first two harmonics

The simplest tilt measure looks at just the first two harmonics: **H1–H2** is the level of
the first harmonic (at F0) minus the level of the second (at 2×F0), in dB.

- **Higher H1–H2** (the fundamental dominates): goes with a more open, breathier voice
  [3][9].
- **Lower H1–H2** (the second harmonic catches up): goes with a more constricted, pressed
  or creaky voice [3].

H1–H2 is related to the open quotient [9]. Related measures compare H1 with the harmonic
nearest the first formant (**H1–A1**, related to the first formant's bandwidth) or the third
(**H1–A3**, related to overall spectral tilt) [10].

Caveats, all from the research literature:

- **Formants get in the way.** A harmonic that happens to sit near a formant is boosted by
  it, so H1–H2 depends on the vowel. Researchers apply a *formant correction* (written
  H1\*–H2\*) [9], which in turn needs accurate formant measurements [3]. For high voices,
  H1\*–H2\* also depends on F1 and vowel height [9], and high voices are exactly where
  formants are hard to measure (see
  [Formants and resonance](formants-and-resonance.md#why-formants-get-hard-to-measure-at-high-pitch)).
- **Raw values don't transfer between people.** One person's creaky voice can average −2 dB
  and another's 5 dB [3]. H1–H2 is more useful for change within one person than as an
  absolute target, which suits Wren's approach of targets relative to your own baseline.
- **Labels are ambiguous.** "H1–H2" sometimes means the uncorrected value and sometimes the
  value computed from the estimated source [3]. Wren's docs should say which.
- **Notation.** A 2015 consensus paper on notation recommends dropping "H" labels for
  harmonics [11], but H1–H2 remains the common name in the literature.

## Candidate measure 3: CPP, cepstral peak prominence

**Cepstral peak prominence (CPP)** measures how strongly periodic the voice is, compared with
the noise around it. It is computed on the *cepstrum*, roughly "the spectrum of the
spectrum": a strongly periodic voice has a neat, regular comb of harmonics, and the
cepstrum turns that regularity into one tall peak. CPP is how far that peak stands above
the background [12]. Introduced in 1994, it correlated very strongly (r = −0.92) with
listeners' ratings of breathiness [13][14]. A smoothed version, **CPPS**, averages the
cepstrum over time and quefrency [14][15], and Praat implements it [12][16].

For weight, CPP is a partial signal at best: it tracks breathiness (noise), not the light–
heavy dimension directly. The predecessor project also noted that pressed, strained voice
is highly periodic, so CPP can *rise* under strain: a reminder not to read "higher CPP" as
"better" (salvage audit D7, reasoning not yet tested).

## What isn't on the list

**Jitter, shimmer and HNR** (cycle-to-cycle variation and harmonics-to-noise ratio) are
standard voice-analysis measures, covered in Praat's voice tutorial [17], but on phone and laptop microphones they "mostly
measure the room" (salvage audit D7). Wren doesn't plan to use them for weight.

## Safety note

Training weight can mean changing how firmly the vocal folds meet, so it sits close to
strain. Wren's safety logic (feature F8) watches for strain, and constitution principle V
puts safety cues ahead of training cues. If voicing hurts, or hoarseness lasts more than about three weeks, see a
doctor [18]; speech-language pathologists assess and treat voice problems [19]. Wren is a
training aid, not medical care (principle IV).

## Sources

1. Netzorg, R., Yu, B., Guzman, A., Wu, P., McNulty, L. and Anumanchipalli, G. (2024).
   *Towards an interpretable representation of speaker identity via perceptual voice
   qualities*. Proc. ICASSP 2024. doi:10.1109/ICASSP48485.2024.10446197. Free preprint:
   <https://arxiv.org/pdf/2310.02497>
2. Wolfe, J., Garnier, M. and Smith, J. (2009, updated online). *Voice Acoustics: an
   introduction to the science of speech and singing*. UNSW Music Acoustics.
   <https://newt.phys.unsw.edu.au/jw/voice.html>
3. Garellek, M. (2019). *The phonetics of voice*. In W. F. Katz and P. F. Assmann (eds.),
   *The Routledge Handbook of Phonetics*, 75–106. doi:10.4324/9780429056253-5. Free
   preprint:
   <https://idiom.ucsd.edu/~mgarellek/files/Garellek_Phonetics_of_Voice_Handbook_final.pdf>
4. Netzorg, R., Cote, A., Koshin, S., Garoute, K. V. and Anumanchipalli, G. K. (2024).
   *Speech after gender: A trans-feminine perspective on next steps for speech science and
   technology*. Proc. Interspeech 2024. doi:10.21437/Interspeech.2024-2269.
   <https://www.isca-archive.org/interspeech_2024/netzorg24_interspeech.pdf>
5. Netzorg, R., Carvalho, N., Guzman, A., Wang, L., Francis, J., Garoute, K. V., Johnson,
   K. and Anumanchipalli, G. K. (2025). *On the production and perception of a single
   speaker's gender*. Proc. Interspeech 2025.
   <https://www.isca-archive.org/interspeech_2025/netzorg25_interspeech.pdf>
6. Hanson, H. M. (1997). *Glottal characteristics of female speakers: Acoustic
   correlates*. Journal of the Acoustical Society of America 101(1), 466–481.
   doi:10.1121/1.417991. Abstract: <https://pubmed.ncbi.nlm.nih.gov/9000737/>
7. Nordenberg, M. and Sundberg, J. (2004). *Effect on LTAS of vocal loudness variation*.
   Logopedics Phoniatrics Vocology 29(4), 183–191. doi:10.1080/14015430410004689.
   Abstract: <https://pubmed.ncbi.nlm.nih.gov/15764212/>
8. Gramming, P. and Sundberg, J. (1988). *Spectrum factors relevant to phonetogram
   measurement*. Journal of the Acoustical Society of America 83(6), 2352–2360.
   doi:10.1121/1.396366. Abstract: <https://pubmed.ncbi.nlm.nih.gov/3411026/>
9. Iseli, M., Shue, Y.-L. and Alwan, A. (2007). *Age, sex, and vowel dependencies of
   acoustic measures related to the voice source*. Journal of the Acoustical Society of
   America 121(4), 2283–2295. doi:10.1121/1.2697522. Abstract:
   <https://pubmed.ncbi.nlm.nih.gov/17471742/>
10. MIT OpenCourseWare, 6.542J *Laboratory on the Physiology, Acoustics, and Perception of
    Speech* (Fall 2005), Lab 5 handout (built on Hanson 1997).
    <https://ocw.mit.edu/courses/6-542j-laboratory-on-the-physiology-acoustics-and-perception-of-speech-fall-2005/9a410aa5de0a94d085b680f35b0d5954_lab5.pdf>
11. Titze, I. R. and 21 co-authors (2015). *Toward a consensus on symbolic notation of
    harmonics, resonances, and formants in vocalization*. Journal of the Acoustical Society
    of America 137(5), 3005–3007. doi:10.1121/1.4919349. Free full text:
    <https://pmc.ncbi.nlm.nih.gov/articles/PMC5392060/>
12. Weenink, D. *Praat manual: PowerCepstrogram: Get CPPS...*.
    <https://www.fon.hum.uva.nl/praat/manual/PowerCepstrogram__Get_CPPS___.html>
13. Hillenbrand, J., Cleveland, R. A. and Erickson, R. L. (1994). *Acoustic correlates of
    breathy vocal quality*. Journal of Speech and Hearing Research 37(4), 769–778.
    doi:10.1044/jshr.3704.769. Abstract: <https://pubmed.ncbi.nlm.nih.gov/7967562/>
14. Skowronski, M. D., Shrivastav, R. and Hunter, E. J. (2015). *Cepstral peak
    sensitivity: A theoretic analysis and comparison of several implementations*. Journal
    of Voice 29(6), 670–681. doi:10.1016/j.jvoice.2014.11.005. Free full text:
    <https://pmc.ncbi.nlm.nih.gov/articles/PMC4630216/>
15. Hillenbrand, J. and Houde, R. A. (1996). *Acoustic correlates of breathy vocal
    quality: Dysphonic voices and continuous speech*. Journal of Speech and Hearing
    Research 39(2), 311–321. doi:10.1044/jshr.3902.311. Abstract:
    <https://pubmed.ncbi.nlm.nih.gov/8729919/>
16. Maryn, Y. and Weenink, D. (2015). *Objective dysphonia measures in the program Praat:
    Smoothed cepstral peak prominence and acoustic voice quality index*. Journal of Voice
    29(1), 35–43. doi:10.1016/j.jvoice.2014.06.015. Abstract:
    <https://pubmed.ncbi.nlm.nih.gov/25499526/>
17. Boersma, P. and Weenink, D. *Praat manual: Voice* (tutorial covering jitter, shimmer
    and HNR). <https://www.fon.hum.uva.nl/praat/manual/Voice.html>
18. National Institute on Deafness and Other Communication Disorders (NIDCD). *Hoarseness*.
    <https://www.nidcd.nih.gov/health/hoarseness>
19. American Speech-Language-Hearing Association (ASHA). *Practice Portal: Voice
    Disorders*. <https://www.asha.org/practice-portal/clinical-topics/voice-disorders/>
