

import mido
from mido import Message
from pprint import pprint
import mingus.core.chords as chords
import random


from chordTTS import *
from chordtrainer import *
from GPIOcontrol import *





if __name__ == '__main__':


    # ini TTS
    picotts, p, input1, outport  = setup_TTS()

    with mido.open_input(input1) as inport:

        # ini exercice type
        exercice = ChordTrainer(picotts, p, inport)


        while(True):

            exercice.teacher_ask_new_question()
            
            while not exercice.evaluate():
                exercice.read_answer()
              
            # change exercice if necessary  
            exercice = read_GPIO(exercice)    


    p.terminate()