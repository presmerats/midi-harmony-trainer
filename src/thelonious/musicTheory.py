from __future__ import annotations


class MusicTheory(object):
    degrees = ["C", "D", "E", "F", "G", "A", "B"]

    root_notes = [
        "C",
        "B#",
        "C#",
        "Db",
        "D",
        "D#",
        "Eb",
        "E",
        "Fb",
        "F",
        "E#",
        "F#",
        "Gb",
        "G",
        "G#",
        "Ab",
        "A",
        # "Bbb",
        "A#",
        "Bb",
        "B",
        "Cb",
    ]

    note = [
        ("C", "B#", "Dbb"),
        ("C#", "B##", "Db"),
        ("D", "C##", "Ebb"),
        ("D#", "Eb", "Fbb"),
        ("E", "D##", "Fb"),
        ("F", "E#", "Gbb"),
        ("F#", "E##", "Gb"),
        ("G", "F##", "Abb"),
        (
            "G#",
            "Ab",
            "Bbbb",
        ),
        ("A", "G##", "Bbb"),
        ("A#", "Bb", "Cbb"),
        ("B", "A##", "Cb"),
    ]

    notes = None

    chord_types = {
        "major": [4, 3],
        "minor": [3, 4],
        "M7": [4, 3, 4],
        "maj7": [4, 3, 4],
        "7": [4, 3, 3],
        "-7": [3, 4, 3],
        "m7": [3, 4, 3],
        "7b5": [3, 3, 4],
        "dim7": [3, 3, 3],
    }

    interval_types = {
        "chromatic": [1],
        "tone": [2],
        "minor_third": [3],
        "major_third": [4],
        "thirds": [4],
        "perfect_fourth": [5],
        "fourths": [5],
        "augmented_fourth": [6],
        "minor_fifth": [6],
        "fifths": [7],
        "perfect_fifth": [7],
        "major_sixth": [9],
        "sixths": [9],
        "minor_sixth": [8],
        "minor_seventh": [10],
        "major_seventh": [11],
        "sevenths": [11],
    }

    interval_names = {
        "chromatic": "b2",
        "tone": "2",
        "minor_third": "b3",
        "major_third": "3",
        "thirds": "3",
        "perfect_fourth": "4",
        "fourths": "4",
        "augmented_fourth": "#4",
        "minor_fifth": "b5",
        "fifths": "5",
        "perfect_fifth": "5",
        "major_sixth": "b6",
        "sixths": "6",
        "minor_sixth": "6",
        "minor_seventh": "b7",
        "major_seventh": "7",
        "sevenths": "7",
    }

    def __init__(self):
        pass

    def build_interval(self, root, intervals):
        final_chord = [root]

        posi = self.find_note_position(root)

        for interval in intervals:
            #
            print("posi", posi, interval)
            posi = (posi + interval) % len(self.note)
            print("->", posi)

            # update curernt note
            current_note = self.note[posi][0]

            final_chord.append(current_note)

        print("return from build_interval", final_chord)

        return final_chord

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

    def build_chord_from_root_and_type(self, root, chord_type):
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

    def build_chord_from_root_and_type_simplified(self, root, chord_type):
        final_chord = self.build_chord_from_root_and_type(root, chord_type)

        final_chord = [
            note if isinstance(note, str) else note[0] for note in final_chord
        ]

        return final_chord

    def find_root_from_chord_name_substring(
        self, chord_name, substring_length
    ):
        root = None

        first_2_digits = chord_name[:substring_length]

        for note_name in self.root_notes:
            if first_2_digits == note_name:
                root = note_name

                break

        return root

    def find_root_from_chord_name(self, chord_name):
        root = None
        root = self.find_root_from_chord_name_substring(chord_name, 3)
        if root is not None:
            return root

        root = self.find_root_from_chord_name_substring(chord_name, 2)
        if root is not None:
            return root

        root = self.find_root_from_chord_name_substring(chord_name, 1)
        return root

    def build_chord_from_name(self, chord_name):
        # example A-7

        # first look for note with firs 2 digits
        root = self.find_root_from_chord_name(chord_name)

        print()
        print(f"----- found root {root}")

        if root is None:
            raise Exception(f"Can't find root note from {chord_name}")

        # then with the rest look for chord type
        j = chord_name.find(root)

        if j > -1 and len(chord_name) > j + len(root):
            j = j + len(root)

            chord_type = chord_name[j:]

            chord_type_intervals = self.chord_types[chord_type]

        else:
            chord_type_intervals = self.chord_types["major"]

        print(chord_type_intervals)

        return self.build_chord_from_root_and_type_simplified(
            root, chord_type_intervals
        )
