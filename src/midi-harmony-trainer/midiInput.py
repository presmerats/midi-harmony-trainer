
from os import system
import io
from mido import Message
from mido import MidiFile
import mido

from musicTheory import MusicTheory



class NoMidiInputsException(Exception):
    def __init__(self, message = "Couldn't find any MIDI inputs. Check you MIDI controller is connected.", errors = None ):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        # Now for your custom code...
        self.errors = errors

class CantReadMidiInputsException(Exception):
    def __init__(self, message = "Couldn't read the MIDI input. Check you MIDI controller is connected.", errors = None ):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        # Now for your custom code...
        self.errors = errors


music_theory = MusicTheory()

midi_notes = { i:music_theory.note[i%12]  for i in range(128) }

midi_note_heigth = { i:int(i/12 - 1)   for i in range(12,109)}

def setup_midi_input():

    outport = mido.open_output()
    
    input_names = mido.get_input_names()
    #print("mido input names", input_names)
    if len(input_names) == 0:
        raise NoMidiInputsException()
    
    input1 = input_names[0]
    for inp in input_names:
        # set a parameter for that!!
        if inp.find('Keystation')>-1:
            input1 = inp

    #print("input1", input1)
    try:
        return mido.open_input(input1)
    except:
        print(traceback.format_exc())  
        raise CantReadMidiInputsException()


def read_midi_input(msg):
    
    if 'note' not in dir(msg):
        return None, None, None
        
    if msg.is_meta:
        return None, None, None

    current_note = midi_notes[msg.note]
    current_octave = midi_note_heigth[msg.note]
    play_status = msg.velocity > 0 
    
    return msg.note, current_note, current_octave, play_status

            


    



