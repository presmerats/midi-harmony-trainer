from mingus.containers import NoteContainer, Note
from mingus.midi import fluidsynth



class MyMidiPlayer:

    def __init__(self, ):
        fluidsynth.init("./external/FluidR3_GM.sf2")



    def update_play(self, note, octave, play_status):
        if play_status:
            fluidsynth.play_Note(Note(f"{note}-{octave}"))
        else:
            fluidsynth.stop_Note(Note(f"{note}-{octave}"))