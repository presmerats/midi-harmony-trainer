
from pprint import pprint

# import mido
# from mido import Message
# import mingus.core.chords as chords
# from mingus.containers import NoteContainer, Note
# from mingus.midi import fluidsynth

# import random

from chordTTS import MyTTS

import midiInput 

from midiPlayer import MyMidiPlayer

from chordtrainer import *

#from GPIOcontrol import *





if __name__ == '__main__':


    # ini TTS
    my_tts  = MyTTS()

    # ini midi input engine
    midi_input_msgs = midiInput.setup_midi_input()
    
    # ini midi player engine
    midi_player = MyMidiPlayer()
    
    # ini exercice type
    exercice = ChordTrainer()


    while(True):

        # new Question
        question = exercice.teacher_ask_new_question()
        print(question)
        my_tts.teacher_say_chords(question)

        
        for msg in midi_input_msgs:

            # process midi msg
            global_note, note, octave, play_status = midiInput.read_midi_input(msg)
            
            if note is None:
                continue

            # play sound or stop sound played
            midi_player.update_play(note[0], octave, play_status)
            
            # update exercice answer
            exercice.update_answer(global_note, note, octave, play_status)
            
            # evaluate exercice answer
            if exercice.evaluate():
                print("Correct!", exercice.parsed_chord )
                my_tts.teacher_say("Correct chord!")
                #GPIOcontrol.green_light_GPIO()
                break

        # change exercice if necessary  
        # exercice = GPIOcontrol.read_GPIO(exercice)    


    p.terminate()