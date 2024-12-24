import time
from mingus.containers import NoteContainer, Note
from mingus.midi import fluidsynth

fluidsynth.init("./external/FluidR3_GM.sf2")

fluidsynth.play_Note(Note("C-5"))
time.sleep(1)
fluidsynth.stop_Note(Note("C-5"), 1)