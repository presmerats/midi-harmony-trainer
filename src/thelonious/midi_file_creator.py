from __future__ import annotations

import argparse

import yaml
from mido import Message
from mido import MidiFile
from mido import MidiTrack
from musicTheory import MusicTheory


class Song:
    # this is in fact a series of sequences, but I will transform it later

    def __init__(
        self,
        config_dict: dict,
        output: str,
        midi_rules_path: str = "midi_config.yml",
    ):
        self.config = config_dict

        self.swing = self.config["meta"].get("swing", False)

        with open(midi_rules_path, "r") as file:
            midi_rules = yaml.safe_load(file)
            # pprint(midi_rules)
            self.config.update(midi_rules)

        # # create probabilistic rythm sample
        # self.rythm_sample = []
        # for duration in self.config["durations"]:
        #     self.rythm_sample.extend(
        #         [duration] * self.config["durations_probabilities"][duration]
        #     )

        # print("rythm_sample")
        # print(self.rythm_sample)

        # self.note_sample = []
        # for pitch in self.config["pitches"]:
        #     self.note_sample.extend(
        #         [pitch] * self.config["pitch_probability"][pitch]
        #     )

        # print("note sample")
        # print(self.note_sample)

        self.mid = MidiFile()

        self.track = MidiTrack()

        self.mid.tracks.append(self.track)

        self.output = output

        self.used_time_steps = 0.0

        self.max_time_steps = (
            self.config["meta"]["measures"]
            * self.config["meta"]["measure_duration"]
            * self.config["durations_in_measure_times"][
                self.config["meta"]["measure_unit"]
            ]
        )

    def add_sequence(self, notes_sequence):
        for note in notes_sequence:
            if note["note"] == "silence":
                self.track.append(Message("note_off", time=note["ticks"]))
            else:
                self.add_note_with_ticks(note["ticks"], note["note"])

    def add_note_with_ticks(self, note_duration_ticks, new_pitch_name):
        pitch_num = self.config["pitches"][new_pitch_name]

        self.track.append(
            Message("note_on", note=pitch_num, velocity=100, time=0)
        )
        self.track.append(
            Message(
                "note_off",
                note=pitch_num,
                velocity=100,
                time=note_duration_ticks,
            )
        )

    # def add_note(self, note_duration_name, new_pitch):
    #     # print("add_note", note_duration_name, new_pitch)
    #     if new_pitch == "silenci" or new_pitch == "silence":
    #         self.add_silence(note_duration_name)
    #     else:
    #         self.add_final_note(note_duration_name, new_pitch)

    # def add_final_note(self, note_duration_name, pitch):
    #     ticks = self.config["durations_in_ticks"][note_duration_name]
    #     pitch_num = self.config["pitches"][pitch]
    #     self.track.append(
    #         Message("note_on", note=pitch_num, velocity=100, time=0)
    #     )
    #     self.track.append(
    #         Message("note_off", note=pitch_num, velocity=100, time=ticks)
    #     )

    # def add_silence(self, note_duration_name):
    #     ticks = self.config["durations_in_ticks"][note_duration_name]
    #     self.track.append(Message("note_off", time=ticks))

    def fill_measures(self, apply_swing=False):
        print(
            "Max time steps",
            self.max_time_steps,
            "current time steps",
            self.used_time_steps,
        )

        self.track.append(Message("program_change", program=29, time=0))

        max_iterations = 10
        for i in range(max_iterations):
            for passage in self.config["song"]:
                for sequence in self.config["passages"][passage]:
                    sequence_dict = self.config["sequences"][sequence]

                    used_time_steps2, final_sequence = self.parse_sequence(
                        sequence_dict, self.used_time_steps, apply_swing
                    )

                    # print("Potential new time steps", used_time_steps2)

                    # print(final_sequence)

                    if used_time_steps2 < self.max_time_steps:
                        self.used_time_steps = used_time_steps2

                        print("Used time steps:", self.used_time_steps)

                        self.add_sequence(final_sequence)

                        # print(final_sequence)
                        # print("--------SAVED!\n\n")
                    else:
                        break

                if self.used_time_steps >= self.max_time_steps:
                    break

            if self.used_time_steps >= self.max_time_steps:
                break

    def parse_sequence(self, sequence, used_time_steps, apply_swing):
        used_time_steps, rythm = self.generate_rythm(
            sequence["rythm"], used_time_steps, apply_swing
        )

        # pprint(rythm)
        # print()

        final_sequence = self.generate_melody(sequence["melody"], rythm)

        return used_time_steps, final_sequence

    def generate_rythm(
        self, rythm_instructions, used_time_steps, apply_swing=False
    ):
        rythm = []
        for rythm_type, rythm_durations in rythm_instructions.items():
            if rythm_type == "custom":
                
                for rythmic_duration in rythm_durations:
                    (
                        tick_duration,
                        measure_duration,
                        silence,
                    ) = self.parse_rythm_duration(
                        rythmic_duration, apply_swing
                    )

                    rythm.append(
                        {
                            "ticks": tick_duration,
                            "steps": measure_duration,
                            "silence": silence,
                        }
                    )

                    used_time_steps += measure_duration

        return used_time_steps, rythm

    def generate_melody(self, melody_instructions, rythm_sequence):
        # add to the note dict, the pitch, simply put

        # generate flat list of notes
        notes_list = []
        for melody_type, melody_instr in melody_instructions.items():
            if melody_type == "chords":
                for chord in melody_instr:
                    new_notes = self.generate_note_list_from_chord(chord)
                    notes_list.extend(new_notes)

        used_notes = 0
        for rythm_item in rythm_sequence:
            if rythm_item["silence"] is True:
                rythm_item["note"] = "silence"
                continue

            rythm_item["note"] = notes_list[used_notes % len(notes_list)]
            used_notes += 1

        return rythm_sequence

    def explode_note_list_to_instrument_range(self, notes_list):
        final_expanded_notes = []

        # get range
        instrument_range = self.config["meta"]["pitch range"]

        # expand each note from 1 to 7
        for i in range(1, 8):
            for note in notes_list:
                # get pitch number
                new_note = f"{note}{i}"

                new_pitch = self.config["pitches"].get(new_note, None)

                # filter by range

                if (
                    new_pitch is not None
                    and new_pitch >= instrument_range[0]
                    and new_pitch <= instrument_range[1]
                ):
                    final_expanded_notes.append((new_note, new_pitch))

        final_expanded_notes.sort(key=lambda x: x[1])

        return [n[0] for n in final_expanded_notes]

    def generate_note_list_from_chord(self, chord_name):
        # return self.config['chords'].get(melody_instr,None)

        # get chords notes
        musicEngine = MusicTheory()

        notes_list = musicEngine.build_chord_from_name(chord_name)

        print("generate_note_list_from_chord:notes list", notes_list)

        # now explode the notes into the instrument range
        notes_list_exploded = self.explode_note_list_to_instrument_range(
            notes_list
        )

        # # first test with only adding a 3
        # notes_list_exploded = [ f"{note}3" for note in notes_list]

        print(notes_list_exploded)

        return notes_list_exploded

    def parse_rythm_duration(self, rythmic_duration, apply_swing):
        duration = rythmic_duration
        silence = False

        # print("original duration", rythmic_duration)

        i = rythmic_duration.find(" ")
        if i > -1:
            duration = rythmic_duration[:i]
            silence = rythmic_duration[(i + 1):] == "silence"

        j = duration.find("_swing")
        if apply_swing is False and j > -1:
            duration = duration[:j]

        # print("processed duration", duration)

        return (
            self.config["durations_in_ticks"].get(duration, 0),
            self.config["durations_in_measure_times"].get(duration, 0),
            silence,
        )

    def write_midi_file(
        self,
    ):
        # self.mid.save(f"{self.config['meta']['title']}.mid")

        print("Write_Midi_file", self.output)
        self.mid.save(f"{self.output}")

    def generate_midi(
        self,
    ):
        self.fill_measures(apply_swing=False)
        self.write_midi_file()

        if self.swing is True:
            self.mid = MidiFile()

            self.track = MidiTrack()

            self.mid.tracks.append(self.track)

            j = self.output.find(".")
            if j > -1:
                self.output = f"{self.output[:j]}_swing{self.output[j:]}"
            else:
                self.output = f"{self.output}_swing"
            self.fill_measures(apply_swing=True)
            self.write_midi_file()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, help="config yaml file path")

    parser.add_argument("output", type=str, help="pdf output file path")

    args = parser.parse_args()

    print(
        "loading",
    )

    with open(args.config, "r") as file:
        config = yaml.safe_load(file)

        song2 = Song(config_dict=config, output=args.output)

        song2.generate_midi()
