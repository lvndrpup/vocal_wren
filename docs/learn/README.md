# Learn: the voice science behind Wren

Learn is a short primer on the ideas Vocal Wren is built on: what pitch, resonance and
weight actually are, how they show up in sound, and how an app can (and can't) measure
them.

## Who it's for

It's written for the project owner and contributors: people who are comfortable with code
but haven't studied voice science or signal processing. Every page explains an idea in
plain language before naming it, and every factual claim links to a source you can read
yourself, most of them free.

Learn is background, not product copy. In-app coaching text lives in content packs
(constitution principle VIII), and it will be reviewed by a speech-language pathologist
before v1.0 (milestone M6).

A few ground rules that apply throughout, from the [constitution](../constitution.md):

- **Targets, not identities (III).** Voices are described with parameters and directions:
  higher or lower, brighter or darker, lighter or heavier. Nothing here sorts voices into
  categories of people.
- **Not medical care (IV).** Nothing here diagnoses or treats anything. If speaking or
  singing hurts, or hoarseness or voice loss doesn't clear up, see a doctor or a
  speech-language pathologist (SLP), the professionals who assess and treat voice
  problems [1]. The US National Institutes of Health advise seeing a doctor if hoarseness
  lasts more than three weeks [10].
- **Measurement honesty (II).** Where the science is uncertain, the pages say so.

## Suggested reading order

Each page builds on the one before. Allow about ten minutes per page.

1. [Sound and frequency](sound-and-frequency.md): waves, hertz, harmonics, the spectrum,
   decibels.
2. [Pitch and F0](pitch-and-f0.md): the number vs the perception, semitones, typical
   ranges, octave errors.
3. [The source–filter model](source-filter.md): the vocal folds make the buzz, the vocal
   tract shapes it.
4. [Formants and resonance](formants-and-resonance.md): F1/F2/F3, what moves them, what
   trainers mean by resonance, why high voices are hard to measure.
5. [Vocal weight](vocal-weight.md): what "weight" means, its acoustic correlates (spectral
   tilt, H1–H2, CPP), and how much is still uncertain.
6. [Measuring it](measuring-it.md): frames, pitch detection, LPC, confidence, and why
   automatic gain control is a problem.

Terms and repo ID prefixes (OQ-, ADR-, F*n*, M*n*, qew ids) are in the
[glossary](../reference/glossary.md).

## Where to learn more

Roughly from gentlest to most technical. The free sources are linked; the books are
paid (library or second-hand copies work well). The one-line summaries are guidance on
where to start, not reviews.

| Source | Good for | Level |
|---|---|---|
| Joe Wolfe, Maëva Garnier, John Smith, [*Voice Acoustics*](https://newt.phys.unsw.edu.au/jw/voice.html) (UNSW, free web essay) [2] | The best free starting point: source–filter, registers, resonances, formants, with experiments to try with your own voice. Most Learn pages lean on it. | Beginner–intermediate |
| UNSW Music Acoustics [short pages](https://newt.phys.unsw.edu.au/jw/basics.html) on [harmonics](https://newt.phys.unsw.edu.au/jw/harmonics.html), [decibels](https://newt.phys.unsw.edu.au/jw/dB.html), [spectra](https://newt.phys.unsw.edu.au/jw/sound.spectrum.html) and [formants](https://newt.phys.unsw.edu.au/jw/formant.html) (free) | Filling single gaps in the basics. | Beginner |
| The [Praat manual](https://www.fon.hum.uva.nl/praat/manual/Intro.html), by Paul Boersma and David Weenink (free) [3] | What Wren's oracle actually does: pitch and formant analysis settings, with candid notes on when they fail. Start with "Intro", then "how to choose a pitch analysis method" and "Sound: To Formant (burg)...". | Intermediate |
| Brad H. Story, ["An overview of the physiology, physics and modeling of the sound source for vowels"](https://www.jstage.jst.go.jp/article/ast/23/4/23_4_195/_pdf) (2002, free) [11] | A free, careful tour of the voice source and the source–filter model, with the maths. | Intermediate–advanced |
| K. Johnson, *Acoustic and Auditory Phonetics*, 3rd ed. (Wiley-Blackwell, 2011) [4] | A readable textbook on speech acoustics and hearing. | Intermediate |
| R. D. Kent and C. Read, *The Acoustic Analysis of Speech*, 2nd ed. (Singular/Thomson Learning, 2002) [5] | A widely used reference for measuring speech: spectrograms, formants, LPC. | Intermediate–advanced |
| Johan Sundberg, *The Science of the Singing Voice* (Northern Illinois University Press, 1987) [6] | Singing-voice science from one of its leading researchers: formants, larynx height, registers. | Intermediate |
| Ingo R. Titze, *Principles of Voice Production* (Prentice Hall, 1994; reprinted by the National Center for Voice and Speech, 2000) [7] | The physics and physiology of the vocal folds; the deep end for "weight". | Advanced |
| P. McLeod and G. Wyvill, ["A smarter way to find pitch"](http://web.archive.org/web/20210206201756/http://www.cs.otago.ac.nz/tartini/papers/A_Smarter_Way_to_Find_Pitch.pdf) (ICMC 2005, free, 4 pages) [8] | The pitch method Wren's estimator is based on. Short and readable. | Advanced (DSP) |
| Marc Garellek, ["The phonetics of voice"](https://idiom.ucsd.edu/~mgarellek/files/Garellek_Phonetics_of_Voice_Handbook_final.pdf) (2019 handbook chapter; free preprint) [9] | A survey of voice-quality measures (H1–H2, CPP and friends) and their limits. | Advanced |

## Sources

1. American Speech-Language-Hearing Association (ASHA). *Practice Portal: Voice
   Disorders*. <https://www.asha.org/practice-portal/clinical-topics/voice-disorders/>
2. Wolfe, J., Garnier, M. and Smith, J. (2009, updated online). *Voice Acoustics: an
   introduction to the science of speech and singing*. UNSW Music Acoustics.
   <https://newt.phys.unsw.edu.au/jw/voice.html>
3. Boersma, P. and Weenink, D. *Praat: doing phonetics by computer* (software and
   manual). <https://www.fon.hum.uva.nl/praat/>
4. Johnson, K. (2011). *Acoustic and Auditory Phonetics* (3rd ed.). Wiley-Blackwell.
   Catalogue record: <https://openlibrary.org/works/OL15921417W>
5. Kent, R. D. and Read, C. (2002). *The Acoustic Analysis of Speech* (2nd ed.). Albany,
   NY: Singular/Thomson Learning. Catalogue record:
   <https://openlibrary.org/works/OL2645467W>
6. Sundberg, J. (1987). *The Science of the Singing Voice*. DeKalb: Northern Illinois
   University Press. Catalogue record: <https://openlibrary.org/works/OL1634043W>
7. Titze, I. R. (1994). *Principles of Voice Production*. Englewood Cliffs, NJ: Prentice
   Hall; 2nd printing, National Center for Voice and Speech, 2000. Catalogue record:
   <https://openlibrary.org/works/OL3916455W>
8. McLeod, P. and Wyvill, G. (2005). *A smarter way to find pitch*. Proceedings of the
   International Computer Music Conference (ICMC 2005), Barcelona. Free PDF (archived copy):
   <http://web.archive.org/web/20210206201756/http://www.cs.otago.ac.nz/tartini/papers/A_Smarter_Way_to_Find_Pitch.pdf>
9. Garellek, M. (2019). *The phonetics of voice*. In W. F. Katz and P. F. Assmann (eds.),
   *The Routledge Handbook of Phonetics*, 75–106. doi:10.4324/9780429056253-5. Free
   preprint:
   <https://idiom.ucsd.edu/~mgarellek/files/Garellek_Phonetics_of_Voice_Handbook_final.pdf>
10. National Institute on Deafness and Other Communication Disorders (NIDCD). *Hoarseness*.
    <https://www.nidcd.nih.gov/health/hoarseness>
11. Story, B. H. (2002). *An overview of the physiology, physics and modeling of the sound
    source for vowels*. Acoustical Science and Technology 23(4), 195–206.
    doi:10.1250/ast.23.195. <https://www.jstage.jst.go.jp/article/ast/23/4/23_4_195/_pdf>
