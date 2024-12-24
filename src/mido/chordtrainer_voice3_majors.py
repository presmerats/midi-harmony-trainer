import mido
from mido import Message
from pprint import pprint
import mingus.core.chords as chords
import random


from chordTTS import *




# TTS objects
picotts = PicoTTS()
p = pyaudio.PyAudio()


outport = mido.open_output()


input1 = mido.get_input_names()[0]
for inp in mido.get_input_names():
    if inp.find('Keystation')>-1:
        input1 = inp


"""
Application:

1. random generate chord and type(ex C, dominant)
2. translate with mingus
3. show on screen
4. wait until correctly pressed(or just one chance and show succes/failure)

"""

degrees = ['C','D','E','F','G','A','B']

root_notes = [
    'C','B#',
    'C#','Db',
    'D',
    'D#','Eb',
    'E','Fb',
    'F','E#',
    'F#','Gb',
    'G',
    'G#','Ab',
    'A','Bbb',
    'A#','Bb',
    'B','Cb']

note = [
    ('C','B#','Dbb'),
    ('C#','B##','Db'),
    ('D','C##','Ebb'),
    ('D#','Eb'),
    ('E','D##','Fb'),
    ('F','E#','Gbb'),
    ('F#','E##','Gb'),
    ('G','F##','Abb'),
    ('G#','Ab'),
    ('A','G##','Bbb'),
    ('A#','Bb'),
    ('B','A##','Cb')]

notes = { i:note[i%12]  for i in range(128) }


chord_types = {
#'major': [4,3],
# 'minor': [3,4],
'': [4,3,4],
# '7':[4,3,3],
# 'm7':[3,4,3],
# '7b5':[3,3,4],
# 'dim7':[3,3,3]
}


def find_real_note(note_name):

    for n in note:
        for synonime in n:
            if synonime == note_name:
                return n

    return None

def find_note_position(real_note):

    if isinstance(real_note,str):
        real_note = find_real_note(real_note)

    return note.index(real_note)


def choose_random_chord():

    root = root_notes[random.randint(0,len(root_notes)-1)]
    
    chord_types_keys = list(chord_types.keys())
    chord_type = chord_types[chord_types_keys[random.randint(0,len(chord_types_keys)-1)]]
    

    final_chord = [root,]

    # find position of root
    current_note = root
    #final_chord.append(find_real_note(current_note))
    posi = find_note_position(current_note)
    
    for interval in chord_type:
        # add semitones to find next note
        posi = (posi + interval) % len(note)

        # update curernt note 
        current_note = note[posi]
        final_chord.append(current_note)

    return final_chord


def parse_chord(a_chord):
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

    foundi = degrees.index(root[0])
    ld = len(degrees)
    the_degrees = [
                    degrees[foundi],
                    degrees[(foundi+2)%ld],
                    degrees[(foundi+4)%ld],
                    degrees[(foundi+6)%ld],
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


def match_chord(pressed_notes, thechord):

    # convert to real chord
    thechord2 = [ thechord[i] if i>0 else find_real_note(thechord[i]) for i in range(len(thechord)) ]

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


pressed_notes = []
with mido.open_input(input1) as inport:
    while(True):

        thechord = choose_random_chord()
        
        chord_name, parsed_chord = parse_chord(thechord)


        print(chord_name)
        teacher_say_chords(chord_name, picotts, p)

        

        for msg in inport:
            if 'note' not in dir(msg):
                continue
                
            if msg.is_meta:
                continue


            current_note = notes[msg.note]
            if msg.velocity > 0 :
                pressed_notes.append((msg.note,current_note))
            else:
                try:
                    foundi = pressed_notes.index((msg.note,current_note))
                    if foundi > -1:
                        pressed_notes.pop(foundi)
                except:
                    pass

            if match_chord(pressed_notes, thechord):
                print("Correct!", parsed_chord )
                teacher_say("Correct chord!", picotts, p)
                break
            
            
            


p.terminate()