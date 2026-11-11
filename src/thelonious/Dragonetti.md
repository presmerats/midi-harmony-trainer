# Dragonetti: sight reading exercice generator



## Tasks

### 2026-11-09 Initial exploration

ok- write down tasks
ok- Write down modelling hierarchy
-
ok- argparse
ok- launch midi player from Makefile?
- git commit, maybe create a new branch? maybe push to main

- correct Makefile because pdf extension is misused
  - fast approach midi2ly --duration-quant=8
  - profoudn approach generate 2 midi files, one for listening and one for lilypong
    - fix swing 8th and 16th notes (write midi to lily without swing and then midi with swing?)
-
ok- yaml examples:
  ok- find a better syntax for ti (simpler in the yaml but equivalent when parsed in the code)
    ok- implement: sequence, material with material type, sequencer
     ok - list of rythmic notes with silence with single note
        ok- use midi_config.yml
        ok- read chords from midi_config.yml
        -
    ok- swing that is not visible in the score but audible in the midi
        ok- python part -> generate the mid file with swing and without it
          ok- fill measures  -> 2 version if swing=True
          ok- FIX fill measures somehow wrong!
          ok- write_Midi  -> 2 versions
        ok- Makefile part -> parse to lilypond the one without swing

    ok- song length & start over
        ok- repeat list of notes if sequence is not completed
        ok- start again passage or sequeces if measures are not completed.

- content availability: notes
    - lister
      - list of notes
      ok- chord
        ok- use thelonious to generate chords with name/symbol
      - scale
        - use thelonious
      - interval(s) + scale
    - Random
      - list of notes
      - chord
      - scale
      - interval(s) + scale

    - Improve chord and scale definition using intervals
    - apply instrument and/or ranges
- Content: rythms
    - rythm subparts that are combined randomly
    - some subparts tend to fall in specific measure times
    - some subparts are completely random also
    - some subparts are determined completely
    -
- predetermined sequences
    - determined list of notes + 4rth note durations
    - determined rythm (list of durations that repeats) + random scale notes
    - determined rythm + determined notes (melody in order)
    ok- determined rythm + chord
    - determined rythm + scale
    - determined rythm + chord progression
  - Randomness
    - determined rythm + chord/arpeggio at random
    - determined rythm + scale at random
    - determined rythm + chord/arpeggio at random
    - determined rythm + defined interval random
    - determined rythm + multiple intervals at random
    - random rythm + chord progression
  - Weithted probabilities
    - determined rythm + chord/arpeggio -> I and 5th degrees need to have high probs in measure/2 measure teim steps
  - Combine sequences randomly
  -
- Python classes
  - find the correct subclassing
    - concept 1: by randomness, weighted randomness
    - concept 2: for determined sequences to play in order
    - concept 3: combining sequences in order but randomly?





## Modelling

First ideation of the hierarchy that models a song

- song
  - CONTAINS multiple passages
  - for example different parts of a song ABABCA, verse/chorus/bridge, modulations, different harmonic rythms, different harmonic parts

- passage
  - CONTAINS: multiple sequences
  - a part of a song, for example the verse, or the harmonic progression belongin to one group ebfore a modulation, etc

- Sequence
  - the building block of a song, can be the first 4 bars of a blues or the 12 complete bars of a blues... Flexibility first
  - this is where rythm and notes are selected or generated
  - Types of sequenches:
    - by Content: durations or note pitches
      - the silence is part of the note pitches, but it would be better to consider it as rythm
    - by generation type:
      - predetermined list to play in order
        - custom list
        - chord/arpeggio
        - scale
      - list to play randomly
        - custom list
        - chort/arpeggio
        - scale
        - intervals to play randomly
  - Sequence building blocks
    - material type
      - note_pitch vs rythmic_notes
    - materials
      - chord, scale, interval, list of notes, list of rythmic notes
    - sequencers
      - they process materials to generate the final sequence
      - list sequencer: uses the materials in order
      - generator sequencer: use the materilas by some rules (randomness, weighted randomness or others)
    - Midi config
      - config rules:
        - durations in ticks,
        - names of durations,
        - pitch to note symbol
        - chord to note symbols
        - scale to note symbols
        - interval to relative symbols
