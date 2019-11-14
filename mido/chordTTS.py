

import pyaudio
import wave
import  time
import sys
import StringIO
from picotts import PicoTTS

def  speak_for_me(msg, picotts, p):

    
    wavs = picotts.synth_wav(msg)
    wav = wave.open(StringIO.StringIO(wavs))
    #print wav.getnchannels(), wav.getframerate(), wav.getnframes()
    f = wav
    
    
    stream = p.open(format = p.get_format_from_width(wav.getsampwidth()),
                                                 channels = wav.getnchannels(),
                                                 rate = f.getframerate(),
                                                 output = True)

    chunk = 1024
    data = f.readframes(chunk)
    
    while data:
        stream.write(data)
        data = f.readframes(chunk)
    
    stream.stop_stream()
    stream.close()
    
    
def teacher_say(msg, picotts, p):
    if isinstance(msg, str):
        speak_for_me(msg,picotts,p)
    elif isinstance(msg, list):
        speak_for_me(msg[0], picotts,p)

def teacher_say_chords(chord_list, picotts, p):

    schord = chord_list[0]

    schord = schord.replace('bb',' double flat ')
    schord = schord.replace('b',' flat ')
    schord = schord.replace('##',' double sharp ')
    schord = schord.replace('#',' sharp ')
    

    speak_for_me(schord, picotts,p)


