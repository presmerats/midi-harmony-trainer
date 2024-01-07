

import pyaudio
import wave
import  time
import sys
#import StringIO
from mido import Message
from mido import MidiFile
import mido
from picotts import PicoTTS


def setup_TTS():

    # TTS objects
    #picotts = PicoTTS()
    picotts = None
    p = pyaudio.PyAudio()


    outport = mido.open_output()


    input1 = mido.get_input_names()[0]
    print("input names", mido.get_input_names())
    for inp in mido.get_input_names():
        if inp.find('USB')>-1:
            input1 = inp

    return picotts, p, input1, outport


def  speak_for_me(msg, picotts, p):

    print(msg)

    



