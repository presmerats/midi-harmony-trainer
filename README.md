# Midi-Harmony-trainer

The goal of this code is to help musicians learn chords and piano voicings, adding also very basic ear training exercices. It is based on the Mingus and mido python packages.

# To-Do List

## Refactor

- [ ] --------------------------------------
- [X] ~~Modify as a python package with poetry and build required environment~~
- [X] ~~Update Mingus source package (python 3 based version)~~
- [X] ~~remove unused code~~
- [ ] Separate concerns into modules
- [ ] ---- 1. Mingus extension: is it needed or not? does the chords logic already exist within Mingus?
- [ ] ---- 2. Midi controller connection & configuration
- [ ] ---- 3. TTS engine wrapper
- [ ] ---- 4. Piano Chord exercices: refactor, generalise to make extendable
- [ ] ---- 5. Ear training exercices.
- [ ]  Clean documentation also
- [ ] --------------------------------------
- [ ] --------------------------------------

## Ear & chord training


- [ ] 2) Abstract an exercice class + yaml file for each exercice
- [ ] Review Mingus harmony engine

- [ ] Training list:
    * intervals
    * single hand chords
    * root and chord
    * 2 hand same voicing
    * 2 hand chord voicings
    * 4rth voicings
    * chord progression training
    * sond chords training too (Jazz standards)
    * Bass line training loops
    * Backing tracks
    * ear training exercies (interval, chord, progression)

- [ ] Extend piano chord exercices by yaml confid files
- [ ] Adapt piano book basic exercices: II-V-Is
- [ ] Adapt piano book basic exercices: 7b5
- [ ] Adapt piano book basic exercices: dim7

- [ ] Advanced Piano voicings: bass note + right hand
- [ ] Advanced Piano voicings: 2 hand voicings
- [ ] Advanced Piano voicings: 2 hand voicings + 9th-11th-13th
- [ ] Advanced Piano voicings: 4rth voicings

- [ ] Piano comping: bass comping + right ritmic chord
- [ ] Piano comping: bass comping + right ritmic chord + right hand melody
- [ ] Piano comping: block chords melody

- [ ] Rick beato ear training adaptation?

## Midi and TTS engines
- [X] ~~review fluidsynth usage in MacOS: [](https://www.youtube.com/watch?v=O8ZzgaGNLn0)~~
- [X] ~~1) use fluidsynth to play the notes from the computer: octave? + volume?~~
- [ ] Adapt TTS to each OS (import platform; platform.system() )
    * pico tts for linux + install instructions,
    * MACOS? nothing, use say
    * windows
    * Android?) usd
- [ ] Finalize installation on MacOS: play, tts, midi controller receive, midi controller configure
- [ ] --------------------------------------
- [ ] Midi connection scripts?
- [ ] Midi controller buttons re assigning to specific tasks (like changin type of exercice or type of chords, or randomness)


## Package
- [ ] rename to wes?mmcoy?tyner?
- [ ] 3) option 2 installation as a cli tool  with a single exercice
- [ ] option 1 installation as a cli that opens a hacky console menu tools

- [ ] option 3 frontend with Kivy
- [ ] distribute on PyPi
- [ ] Create a frontend for Linux, MacOS, Windows, Android, iOS, web (use a Python based frontend: reflex, kivy  ) Maybe on another repo?



## Installation tools
- [ ] Check tts after installation
- [ ] Check fludisynt after install
- [ ] Check Sf2 after tinstall
- [ ] Check yaml config file
- [ ] --------------------------------------
- [ ] --------------------------------------
- [ ] Linux installation guide
- [ ] MacOS compatibility
- [ ] Macos installation guide
- [ ] Windows compatibility and installation guide

## Mega improvement
- [ ] use librosa to leverage FFT to detect chords in sound input from mic

# Installation instructions

## Installing on Linux

```
$ sudo apt install libfluidsynth3
```

download FluidR3_GM.sf2
```
$ sudo apt install fluid-soundfont-gm
```
On Ubuntu, the soundfont file will be located at /usr/share/sounds/sf2/FluidR3_GM.sf2 .

Install pyfluidsynth, which lets you access FluidSynth from Python:

```
$ pip install pyfluidsynth
````

## Installing on macOS

```
% brew install python
% brew install python-tk
```

```
% brew install fluid-synth
```

Download FluidR3_GM.sf2 from the [page](https://member.keymusician.com/Member/FluidR3_GM/index.html) The Fluid Release 3 General-MIDI Soundfont.

```
% pip install pyfluidsynth
```

## Installing on Windows

1. Go to the FluidSynth releases page and download the latest 64-bit release for Windows (e.g. fluidsynth-2.1.0-win64.zip). Extract this zip file into some directory

2. Add the fluidsynth-x64\bin subdirectory to your PATH. To do this, click in the search box on the task bar, run the command 'Edit the system environment variables', click 'Environment Variables…', select Path in the 'User variables' section, click 'Edit…', click New, then enter the path of the bin subdirectory, e.g. c:\Users\me\install\fluidsynth-x64\bin.

3. FluidSynth needs a file FluidR3_GM.sf2 that contains waveforms for various musical instruments. You can download this file from the page The Fluid Release 3 General-MIDI Soundfont. On that page, click the link 'Download FluidR3_GM Soundfont'. Save the file in some directory.

4. Install pyfluidsynth, which lets you access FluidSynth from Python:

```bash
pip install pyfluidsynth
```

**pyfluidsynth API**
Here are a few useful classes and methods. For more information, sees the pyfluidsynth GitHub page.

**fluidsynth.Synth class**

A Synth is an instance of the FluidSynth synthesizer.

Synth()
Create a Synth.
.note_off(channel, key)
Stop playing a note on the given channel. key is a MIDI note number from 0 to 127.
.note_on(channel, key, velocity)
Start playing a note on the given channel. key is a MIDI note number from 0 to 127. velocity is a value from 0 to 255.
.program_select(channel, soundfont_id, bank, preset)
Select a sound to play on the given channel (a number from 0 to 15), using the given soundfont. Usually bank will be 0. For a general MIDI soundfont such as FluidR3_GM.sf2, preset will be a General MIDI instrument number.
.sfload(filename)
Load a soundfont into memory, returning an ID that references it.
.start([device = name] [driver = name])
Start the synthesizer. On Linux, I recommend passing device = 'hw:0'. On Windows, I recommend passing driver = 'dsound'.


# Code schema and responsibilities

## Current organization

- -- miditrainer.py (
        - init
        - mian exercice loop (-> chordtrainer.py)
- -- chordtrainer.py
        - contains chord definitions
        - exercice loop functions (ask question, read answer, evaluate, choose_random_chord)
        - contains chord maniupltion: find_Note_position, match_chord, ... -> like Music Theory
- -- chordTTS
        - setup TTS
        - setup midi input & output (mido)
        - setup pyAudio (not used!)
- -- GPIOcontrol
        - exercice loop functions to control from midif controller


## Responsibilities

ok- chordTTS::TTS functions
    ok- setup TTS
    ok- setup pyAudio (it is used! maintain)

ok- MidiInput:input control
    ok- setup midi input & output (mido)
    ok- read midi input and return note, octave and status
    ok - decide what to do in the exercice loop
    - run a generator over an input

ok- midiPlayer.py::Playing pressed notes
    ok- call play/update from exercice loop

ok- musicTheory::Chord & interval definitions
    ok- understand input -> match chord

ok- miditrainer::Main Exercice loop
    ok- INIT setup all components (chordtrainer + tts + gpio)
    ok- LOAD EXERCICE PENDING
    ok- EXERCICE LOOP
        - read next question
        - TTS to ask question + print on the screen
        - read input
        - call musicTheory funcs to understand and match answer and evaluate
        - read GPIO


- musicExercice::Loading exercices PENDING
    ok- read yaml exercice definition
        - name
        - type: interval, chords, voicings, progressions, comping, piano bass, songs, improvisation
        - item_selector: random, sequential, sequential_loop, random_loop
        - items_category: (depends on type)
            - type=interval: 2m,2,3m,3,4,4a,5dim,5,6m,6,7m,7,9b,9,11,11#,13b,13, ANY, Any-Major
            - type=chord: 3Maj,3min,Maj7,Dom7,Minor7,half-dim, dim, sus4, sus2,..... ANY, or a Subset
            - type=voicing: (like chord)
            - type=progressions: 2-5-1, 6-4-5-1?, 2-1-5-4,
        - items_category2 (for voicings, tells the type of voicing)
        - item_list: for songs, a list of chords and/or voicings
        - question_print: say|console|GUI
        - answer: play|say|console|GUI
        - evaluation: nothing|say|console|GUI

    - create basic exercice class (part from chordtrainer)
        - instanciate exercice class
            - add tts, midi_input, midi_player
            - load yml file -> to dict -> to class attributes
        - pick the correct functions for
            - next item (random, sequence, loop or not)
            - next item print: teacher say? print? GUI?
            - -------
            - read answer
                - read chords
                - read intervals
                - read voicings
                - read progressions
                - read lh basses
            - play answer?
                - separate play from answer reading?
                    - what is pressed is sent to play
                    - what is pressed is later sent to answer update
                    - depending on type of item, collect note, generic chord, detailed chord voicing,
            - -------
            - evaluate answer
                - chord match
                - chord voicing match
                - interval match
                - progression match
            - teacher say or just continue?
            -----
            - play background rythm and bass? (2 threads?)

        - exercice loop implement inside the exercice class
        - Exit keys inside loop
        - Main class miditrainer: only loads exercice class, handles console menu


        - select next questions (random or in order or...)
            - teacher_ask_new_question()
            - choose_random_chord()
            - parse_chord()
        - update answer
            - update_answer()
        - evaluate
            - evaluate()
            - match_chord()
            - find_note_position()
            - find_real_notes()


    - implement yml + exercie class
        - seventh chords (random and circle of fifths)
        - intervals (selected interval or any, random or circle of fifths)
        - II-V-I progressions
        - song: Misty
        - triads
        - suspended chords
        - voicings: shell chords
        - comping? (midi player with rythm and bass)
        - piano bass? (Midi player with rythm)
        - improvisation? (midi player with rythm and bass)



- chordtrainer::Chord Understanding:
   ok - evaluate answer to question
   - Move functionality to
    - Chord parser class (musicTheory? )
    - Midi Exercice Class







- GPIOcontrol::GPIO functions
