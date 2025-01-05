from __future__ import annotations

import random

import midiInput
import mingus.core.chords as chords
import yaml
from chordTTS import MyTTS
from midiPlayer import MyMidiPlayer
from musicTheory import MusicTheory


class MusicExercice(MusicTheory):
    thechord, chord_name, parsed_chord = None, None, None

    def __init__(
        self,
        yaml_definition,
    ):
        super(MusicExercice, self).__init__()

        # ini TTS
        self.tts = MyTTS()

        # ini midi input engine
        self.midi_input_msgs = midiInput.setup_midi_input()

        # ini midi player engine
        self.midi_player = MyMidiPlayer()

        self.process_exercice_definition(yaml_definition)

        self.pressed_notes = []

        print(self.config)

    def my_root_note_generator(self, sequence=None):
        if sequence is None:
            while True:
                yield self.root_notes[
                    random.randint(0, len(self.root_notes) - 1)
                ]

        else:
            n = 0
            while True:  # n < len(sequence):
                yield sequence[n % len(sequence)]
                n += 1

    def process_exercice_definition(self, yaml_definition):
        with open(yaml_definition, "r") as file:
            self.config = yaml.safe_load(file)

            # save the exercice type
            self.exercice_type = self.config["exercice_type"]

            # save the categoy
            self.exercice_items_categories = self.config["items_category"]
            # check items_categories are all correct first
            valid_categories = []
            for chord_type in self.exercice_items_categories:
                if chord_type in list(self.chord_types.keys()):
                    valid_categories.append(chord_type)
            self.exercice_items_categories = valid_categories

            # save the sub-category
            self.exercice_items_subcategories = self.config["items_category2"]

            # save the unrolled list of items
            if self.config["item_selector"] == "sequence":
                self.exercice_items = self.my_root_note_generator(
                    self.config["sequence"]
                )
            elif self.config["item_selector"] == "random_loop":
                self.exercice_items = self.my_root_note_generator()

    def exercice_loop(
        self,
    ):
        while True:
            # new Question
            question = self.teacher_ask_new_question()
            print(question[0])
            self.tts.teacher_say_chords(question)

            for msg in self.midi_input_msgs:
                # process midi msg
                (
                    global_note,
                    note,
                    octave,
                    play_status,
                ) = midiInput.read_midi_input(msg)

                if note is None:
                    continue

                # play sound or stop sound played
                self.midi_player.update_play(note[0], octave, play_status)

                # update exercice answer
                self.update_answer(global_note, note, octave, play_status)

                # evaluate exercice answer
                if self.evaluate():
                    print("Correct!", self.parsed_chord)
                    self.tts.teacher_say("Correct chord!")
                    # GPIOcontrol.green_light_GPIO()
                    break

            # change exercice if necessary
            # exercice = GPIOcontrol.read_GPIO(exercice)

    def teacher_ask_new_question(
        self,
    ):
        self.thechord = self.choose_next_chord()
        self.chord_name, self.parsed_chord = self.parse_chord(self.thechord)
        return self.chord_name

    def update_answer(self, global_note, note, octave, play_status):
        # print(note, octave, play_status)

        if play_status:
            self.pressed_notes.append((global_note, note))
        else:
            try:
                foundi = self.pressed_notes.index((global_note, note))
                if foundi > -1:
                    self.pressed_notes.pop(foundi)
            except Exception:
                pass

    def evaluate(
        self,
    ):
        if self.match_chord(self.pressed_notes, self.thechord):
            return True

        return False

    def choose_next_chord(
        self,
    ):
        # get next root
        root = next(self.exercice_items)

        # get next random chord type
        chord_types_keys = list(self.exercice_items_categories)
        chord_type = self.chord_types[
            chord_types_keys[random.randint(0, len(chord_types_keys) - 1)]
        ]

        return self.build_chord_from_root_and_type(root, chord_type)

    def choose_random_chord(
        self,
    ):
        root = self.root_notes[random.randint(0, len(self.root_notes) - 1)]

        chord_types_keys = list(self.chord_types.keys())
        chord_type = self.chord_types[
            chord_types_keys[random.randint(0, len(chord_types_keys) - 1)]
        ]

        final_chord = [
            root,
        ]

        # find position of root
        current_note = root
        # final_chord.append(find_real_note(current_note))
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

        # print(a_chord)

        root = a_chord[0][0]

        foundi = self.degrees.index(root[0])
        ld = len(self.degrees)
        the_degrees = [
            self.degrees[foundi],
            self.degrees[(foundi + 2) % ld],
            self.degrees[(foundi + 4) % ld],
            self.degrees[(foundi + 6) % ld],
        ]
        # print(the_degrees)

        parsed_chord = [a_chord[0]]

        for i in range(1, len(a_chord)):
            # print("match",the_degrees[i]," in",a_chord[i])
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
        if isinstance(real_note, str):
            real_note = self.find_real_note(real_note)

        return self.note.index(real_note)

    def match_chord(self, pressed_notes, thechord):
        # convert to real chord
        thechord2 = [
            thechord[i] if i > 0 else self.find_real_note(thechord[i])
            for i in range(len(thechord))
        ]

        # print('real chord', thechord2)

        # sort the pressed notes by note value ascending
        pressed_notes.sort(key=lambda x: x[0])
        pressed_notes2 = [t[1] for t in pressed_notes]
        # print('presset notes', pressed_notes2)

        match = True
        for i in range(len(thechord2)):
            if len(pressed_notes2) < i + 1:
                match = False
                break
            elif pressed_notes2[i] != thechord2[i]:
                match = False
                break

        return match
