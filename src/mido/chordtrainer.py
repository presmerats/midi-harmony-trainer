import mido
from mido import Message
from pprint import pprint
import mingus.core.chords as chords
import random

from musicTheory import *
from chordTTS import *


class ChordTrainer(MusicTheory):

    thechord, chord_name, parsed_chord = None, None, None 
    picotts, p = None, None 

    def __init__(self, picotts, p):
        super(ChordTrainer, self).__init__()
        self.picotts = picotts
        self.p = p 
        #self.inport = inport 
        self.pressed_notes = []


    def teacher_ask_new_question(self,):
        self.thechord = self.choose_random_chord()
        self.chord_name, self.parsed_chord = self.parse_chord(self.thechord)
        print(self.chord_name)
        self.teacher_say_chords(self.chord_name, self.picotts, self.p)
            


    def read_answer(self, msg):
        if 'note' not in dir(msg):
            return
            
        if msg.is_meta:
            return


        current_note = self.notes[msg.note]
        if msg.velocity > 0 :
            self.pressed_notes.append((msg.note,current_note))
        else:
            try:
                foundi = self.pressed_notes.index((msg.note,current_note))
                if foundi > -1:
                    self.pressed_notes.pop(foundi)
            except:
                pass

            
            

    def evaluate(self,):
        if self.match_chord(self.pressed_notes, self.thechord):
            print("Correct!", self.parsed_chord )
            self.teacher_say("Correct chord!", self.picotts, self.p)
            #self.green_light_GPIO()
            return True 

        #self.red_light_GPIO()
        return False 



    def choose_random_chord(self,):

        root = self.root_notes[random.randint(0,len(self.root_notes)-1)]
        
        chord_types_keys = list(self.chord_types.keys())
        chord_type = self.chord_types[chord_types_keys[random.randint(0,len(chord_types_keys)-1)]]
        

        final_chord = [root,]

        # find position of root
        current_note = root
        #final_chord.append(find_real_note(current_note))
        posi = self.find_note_position(current_note)
        
        for interval in chord_type:
            # add semitones to find next note
            posi = (posi + interval) % len(self.note)

            # update curernt note 
            current_note = self.note[posi]
            final_chord.append(current_note)

        return final_chord


    def parse_chord(self, a_chord):
        """
        PENDING:
        - compute semitones between notes of the chord
        - according to the semitones between the previous note
        and the previous note first name(ex C,D#) 
        choose the current note (ex if C -> E, if B -> D#

        establish some priority:
        1. first I,III,V,VII
        2. then II,IV,VI
        """

        #print(a_chord)

        root = a_chord[0][0]

        foundi = self.degrees.index(root[0])
        ld = len(self.degrees)
        the_degrees = [
                        self.degrees[foundi],
                        self.degrees[(foundi+2)%ld],
                        self.degrees[(foundi+4)%ld],
                        self.degrees[(foundi+6)%ld],
                        ]
        #print(the_degrees)

        parsed_chord = [a_chord[0]]


        for i in range(1,len(a_chord)):
            #print("match",the_degrees[i]," in",a_chord[i])
            for synonym in a_chord[i]:
                if synonym.lower()[0] == the_degrees[i].lower():
                    parsed_chord.append(synonym)
                    break

        return chords.determine(parsed_chord), parsed_chord



    def find_real_note(self, note_name):

        for n in self.note:
            for synonime in n:
                if synonime == note_name:
                    return n

        return None


    def find_note_position(self, real_note):

        if isinstance(real_note,str):
            real_note = self.find_real_note(real_note)

        return self.note.index(real_note)



    def match_chord(self, pressed_notes, thechord):

        # convert to real chord
        thechord2 = [ thechord[i] if i>0 else self.find_real_note(thechord[i]) for i in range(len(thechord)) ]

        #print("real chord", thechord2)

        # sort the pressed notes by note value ascending
        pressed_notes.sort(key=lambda x: x[0])
        pressed_notes2 = [t[1] for t in pressed_notes]
        #print("presset notes", pressed_notes2)

        match = True
        for i in range(len(thechord2)):
            if len(pressed_notes2)<i+1:
                match = False
                break
            elif pressed_notes2[i] != thechord2[i]:
                match = False
                break

        return match

        
    def teacher_say(self, msg, picotts, p):
        if isinstance(msg, str):
            speak_for_me(msg,picotts,p)
        elif isinstance(msg, list):
            speak_for_me(msg[0], picotts,p)
    
        # try:
        #     if isinstance(msg, str):
        #         speak_for_me(msg,picotts,p)
        #     elif isinstance(msg, list):
        #         speak_for_me(msg[0], picotts,p)
        # except:
        #     print("Error at teacher_say!")

    def teacher_say_chords(self, chord_list, picotts, p):

        schord = chord_list[0]

        schord = schord.replace('bb',' double flat ')
        schord = schord.replace('b',' flat ')
        schord = schord.replace('##',' double sharp ')
        schord = schord.replace('#',' sharp ')
        
        try:
            speak_for_me(schord, picotts,p)
        except:
            print("Error at teacher_say_chords!")