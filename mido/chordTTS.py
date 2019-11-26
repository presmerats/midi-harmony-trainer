

import pyaudio
import wave
import  time
import sys
import StringIO
from picotts import PicoTTS


def setup_TTS():

    # TTS objects
    picotts = PicoTTS()
    p = pyaudio.PyAudio()


    outport = mido.open_output()


    input1 = mido.get_input_names()[0]
    for inp in mido.get_input_names():
        if inp.find('Keystation')>-1:
            input1 = inp

    return picotts, p, input1, outport
    

def  speak_for_me(msg, picotts, p):

    
    wavs = picotts.synth_wav(msg)
    wav = wave.open(StringIO.StringIO(wavs))
    #print wav.getnchannels(), wav.getframerate(), wav.getnframes()
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
    



