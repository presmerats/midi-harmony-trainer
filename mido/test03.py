import pyaudio
import wave
import  time
import sys
import StringIO
from picotts import PicoTTS

def  speak_for_me(msg):

    picotts = PicoTTS()
    wavs = picotts.synth_wav(msg)
    wav = wave.open(StringIO.StringIO(wavs))
    #print wav.getnchannels(), wav.getframerate(), wav.getnframes()
    f = wav
    
    p = pyaudio.PyAudio()
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
    
    p.terminate()





speak_for_me('Hooray for boobies!,  And, let\'s talk, about,  music')
