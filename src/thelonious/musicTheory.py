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
        "7": [4, 3, 3],
        "-7": [3, 4, 3],
        "7b5": [3, 3, 4],
        "dim7": [3, 3, 3],
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
