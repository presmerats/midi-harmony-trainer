
from os import system
import pyaudio
import wave
import  time
import sys
import io
from mido import Message
from mido import MidiFile
import mido
from picotts import PicoTTS


class NoMidiInputsException(Exception):
    def __init__(self, message = "Couldn't find any MIDI inputs. Check you MIDI controller is connected.", errors = None ):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        # Now for your custom code...
        self.errors = errors


def setup_TTS():

    # TTS objects
    picotts = PicoTTS()
    p = pyaudio.PyAudio()


    outport = mido.open_output()
    

    input_names = mido.get_input_names()
    if len(input_names) == 0:
        raise NoMidiInputsException()
    
    input1 = input_names[0]
    for inp in input_names:
        # set a parameter for that!!
        if inp.find('Keystation')>-1:
            input1 = inp

    return picotts, p, input1, outport


def  speak_for_me(msg, picotts, p):
    system(f"say {msg}")

    # import subprocess
    # subprocess.call(["say",msg])

def speak_for_me_linux(msg, picotts, p): 

    
    wavs = picotts.synth_wav(msg)
    wav = wave.open(io.StringIO(wavs))
    print( wav.getnchannels(), wav.getframerate(), wav.getnframes())
    f = wav
    
    
    stream = p.open(
        format = p.get_format_from_width(wav.getsampwidth()),
        channels = wav.getnchannels(),
        rate = f.getframerate(),
        output = True
        )

    chunk = 1024
    data = f.readframes(chunk)
    
    while data:
        stream.write(data)
        data = f.readframes(chunk)
    
    stream.stop_stream()
    stream.close()
    



