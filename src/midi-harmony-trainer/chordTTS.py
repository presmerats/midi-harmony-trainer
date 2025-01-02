
from os import system
import pyaudio
import wave
import  time
import sys
import io
import traceback
from picotts import PicoTTS



class MyTTS:

    def __init__(self,):

        # TTS objects
        self.picotts = PicoTTS()
        self.p = pyaudio.PyAudio()
        


    def speak_for_me(self, msg):
        system(f"say {msg}")
        # import subprocess
        # subprocess.call(["say",msg])

    def speak_for_me_linux(self,msg, ): 

        wavs = self.picotts.synth_wav(msg)
        wav = wave.open(io.StringIO(wavs))
        print( wav.getnchannels(), wav.getframerate(), wav.getnframes())
        f = wav
        
        
        stream = self.p.open(
            format = self.p.get_format_from_width(wav.getsampwidth()),
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
        


    def teacher_say_chords(self, chord_list):

        schord = chord_list[0]

        schord = schord.replace('bb',' double flat ')
        schord = schord.replace('b',' flat ')
        schord = schord.replace('##',' double sharp ')
        schord = schord.replace('#',' sharp ')
        
        try:
            self.speak_for_me(schord)
        except Exception as err:
            print(traceback.format_exc())
            print(Exception, err)
            print("Error at teacher_say_chords!")


    def teacher_say(self, msg, ):
        if isinstance(msg, str):
            self.speak_for_me(msg,)
        elif isinstance(msg, list):
            self.speak_for_me(msg[0],)
    


