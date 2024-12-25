# Midi-Harmony-trainer

The goal of this code is to help musicians learn chords and piano voicings, adding also very basic ear training exercices. It is based on the Mingus and mido python packages.

# To-Do List

## Refactor


- [X] ~~Modify as a python package with poetry and build required environment~~
- [X] ~~Update Mingus source package (python 3 based version)~~
- [X] ~~review fluidsynth usage in MacOS: [](https://www.youtube.com/watch?v=O8ZzgaGNLn0)~~
- [ ] Adapt TTS to each OS (pico tts for linux + install instructions, MACOS?, windows?, Android?)
- [ ] use fluidsynth to play the notes from the computer
- [ ] Finalize installation on MacOS: play, tts, midi controller receive, midi controller configure
- [ ] ----
- [ ] Separate concerns into modules
- [ ] ---- 1. Mingus extension: is it needed or not? does the chords logic already exist within Mingus?
- [ ] ---- 2. Midi controller connection & configuration
- [ ] ---- 3. TTS engine wrapper
- [ ] ---- 4. Piano Chord exercices: refactor, generalise to make extendable
- [ ] ---- 5. Ear training exercices.
- [ ] Clean unused code, keep the bare minimun needed code to work. Clean documentation also
- [ ] Create a real python package, that is run as a CLI  and distribute on PyPi
- [ ] Create a frontend for Linux, MacOS, Windows, Android, iOS, web (use a Python based frontend: reflex, kivy  ) Maybe on another repo?


## Improvements

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

## Interoperability

- [ ] Linux installation guide
- [ ] MacOS compatibility 
- [ ] Macos installation guide
- [ ] Windows compatibility and installation guide

# fluidsynth installation

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


