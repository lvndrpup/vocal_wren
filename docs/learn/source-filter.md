# The source–filter model

*Learn, page 3 of 6. Previous: [Pitch and F0](pitch-and-f0.md). Next:
[Formants and resonance](formants-and-resonance.md).*

This is the single most useful idea in voice science, and it explains why Wren can treat
pitch, resonance and weight as separate dials.

## The picture: a buzz and a tube

Imagine a buzzer at the bottom of a tube. The buzzer makes a raw, buzzy sound. The tube
doesn't create sound of its own, but it lets some frequencies through more easily than
others, so what comes out of the top is the buzz, *reshaped*. Change the buzzer's speed and
the note changes. Change the tube's shape and the colour of the sound changes.

That is the **source–filter model** of the voice [1][2]:

- The **source** is the sound made at the larynx (voice box) by the vibrating **vocal
  folds** [1].
- The **filter** is the **vocal tract**: the air passage from the vocal folds up through
  the throat and mouth (and nose) to the lips, shaped by the tongue, jaw, lips and other
  *articulators* [1].

The theory was set out by Gunnar Fant in 1960 [2]. Speech synthesizers such as the Klatt
synthesizer are built on it, and Praat's synthesis tools let you build a source and a
filter separately and combine them [3].

## The source: the vocal folds

Air pushed from the lungs passes between the two vocal folds. With the right air pressure
and the right tension and position of the folds, they vibrate, letting air through in
puffs [1]. Muscles do not flap the folds directly (they vibrate far too fast, typically
over 100 times a second); the energy comes from the airflow, and the muscles set the
conditions: how hard the folds are pressed together and how much they are stretched [1].

Because the folds don't move as a smooth sine wave, the puffs contain many harmonics: the
fundamental (the **F0**, see [Pitch and F0](pitch-and-f0.md)) plus multiples of it [1].
Generally the harmonics get weaker as frequency goes up; the steepness of that fall-off is
called **spectral tilt**, and it differs between ways of using the voice [1]. That tilt is
one of the main acoustic handles on vocal **weight** (see [Vocal weight](vocal-weight.md)).

The source mostly controls:

- **pitch** (how fast the folds vibrate), and
- **voice quality**: for example breathy (the folds never fully close) versus a firm,
  quick closure, and the register, which depends on how much of the folds' mass
  vibrates [1]. Voice trainers group some of this under "weight" (see [Vocal weight](vocal-weight.md)).

## The filter: the vocal tract

The vocal tract is roughly a tube about 15–20 cm long, closed-ish at the vocal folds and
open at the lips [1]. Like any tube, it has **resonances**: frequencies that it passes
especially well. Those resonances boost whichever source harmonics happen to lie near them,
which puts broad peaks into the spectral envelope. Those peaks are the **formants** [1][4].

Moving your tongue, jaw and lips changes the tube's shape, which moves the resonances, which
changes the vowel and the colour of the voice [1]. That is the subject of
[Formants and resonance](formants-and-resonance.md).

## Why "separate dials" is (mostly) true

The model's big promise is that source and filter are independent: you can sing "ah" and
"ee" on the same note, or slide the note up without changing the vowel [1]. For most speech
this is a good approximation, and it is why Wren can describe a voice with separate numbers
for pitch, resonance and weight.

It is not perfectly true, and two caveats matter for Wren:

1. **Not like a trumpet.** In a brass instrument the tube controls the note: the player's
   lips tend to vibrate at or near one of the bore's resonances [1]. The voice is
   different. A trombone's range
   overlaps a low speaking voice, but the trombone is metres long and the vocal tract is
   about 0.2 m, so in ordinary speech the voice's fundamental sits *below* the tract's
   resonances and the tract barely steers the folds [1]. The tube analogy is good for the
   filter; it is wrong if you take it to mean the tube sets the pitch.
2. **High voices bend the rule.** When F0 rises into the range of the first resonance (a few
   hundred hertz), source and filter start to interact, and singers often retune their
   resonances to follow the note [1][5]. High F0 also makes the filter much harder to
   *measure*, which is why Wren treats formant readings at high pitch with caution (see
   [Formants and resonance](formants-and-resonance.md#why-formants-get-hard-to-measure-at-high-pitch)).

## In one sentence

The folds make the buzz (pitch and weight), the tract shapes it (resonance), and the
spectrum you see is the buzz's harmonics with the tract's peaks laid over them.

## Sources

1. Wolfe, J., Garnier, M. and Smith, J. (2009, updated online). *Voice Acoustics: an
   introduction to the science of speech and singing*. UNSW Music Acoustics, free web
   essay. <https://newt.phys.unsw.edu.au/jw/voice.html>
2. Fant, G. (1960). *Acoustic Theory of Speech Production*. The Hague: Mouton. Catalogue
   record: <https://openlibrary.org/works/OL6808652W> (not free online). For a free,
   readable overview of the same model, see Story, B. H. (2002). *An overview of the
   physiology, physics and modeling of the sound source for vowels*. Acoustical Science
   and Technology 23(4), 195–206. doi:10.1250/ast.23.195.
   <https://www.jstage.jst.go.jp/article/ast/23/4/23_4_195/_pdf>
3. Boersma, P. and Weenink, D. *Praat manual: Source-filter synthesis*.
   <https://www.fon.hum.uva.nl/praat/manual/Source-filter_synthesis.html>
4. Wolfe, J. *Formant: what is a formant?* Free web page.
   <https://newt.phys.unsw.edu.au/jw/formant.html>
5. Wolfe, J., Garnier, M. and Smith, J. (2009). *Vocal tract resonances in speech, singing,
   and playing musical instruments*. HFSP Journal 3(1), 6–23. doi:10.2976/1.2998482. Free
   full text: <https://pmc.ncbi.nlm.nih.gov/articles/PMC2689615/>
