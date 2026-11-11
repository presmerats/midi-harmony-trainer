from __future__ import annotations

import argparse
import random

import yaml
from mido import Message
from mido import MidiFile
from mido import MidiTrack


class Song:
    # this is in fact a series of sequences, but I will transform it later

    def __init__(self, config_dict: dict, output: str):
        self.config = config_dict

        # create probabilistic rythm sample
        self.rythm_sample = []
        for duration in self.config["durations"]:
            self.rythm_sample.extend(
                [duration] * self.config["durations_probabilities"][duration]
            )

        print("rythm_sample")
        print(self.rythm_sample)

        self.note_sample = []
        for pitch in self.config["pitches"]:
            self.note_sample.extend(
                [pitch] * self.config["pitch_probability"][pitch]
            )

        print("note sample")
        print(self.note_sample)

        self.mid = MidiFile()

        self.track = MidiTrack()

        self.mid.tracks.append(self.track)

        self.output = output

    def add_note(self, note_duration_name, new_pitch):
        # print("add_note", note_duration_name, new_pitch)
        if new_pitch == "silenci":
            self.add_silence(note_duration_name)
        else:
            self.add_final_note(note_duration_name, new_pitch)

    def add_final_note(self, note_duration_name, pitch):
        ticks = self.config["durations_in_ticks"][note_duration_name]
        pitch_num = self.config["pitches"][pitch]
        self.track.append(
            Message("note_on", note=pitch_num, velocity=100, time=0)
        )
        self.track.append(
            Message("note_off", note=pitch_num, velocity=100, time=ticks)
        )

    def add_silence(self, note_duration_name):
        ticks = self.config["durations_in_ticks"][note_duration_name]
        self.track.append(Message("note_off", time=ticks))

    def fill_measures(
        self,
    ):
        used_time_steps = 0

        max_time_steps = (
            self.config["meta"]["measures"]
            * self.config["meta"]["measure_duration"]
            * self.config["durations_in_measure_times"][
                self.config["meta"]["measure_unit"]
            ]
        )

        print("Max time steps", max_time_steps)

        self.track.append(Message("program_change", program=29, time=0))

        while used_time_steps < max_time_steps:
            new_note = random.choice(self.rythm_sample)

            note_duration = self.config["durations_in_measure_times"][new_note]

            new_pitch = random.choice(list(self.note_sample))

            print("new note", note_duration, new_pitch)

            used_time_steps += note_duration
            if used_time_steps > max_time_steps:
                used_time_steps -= note_duration
            else:
                self.add_note(new_note, new_pitch)

    def write_midi_file(
        self,
    ):
        # self.mid.save(f"{self.config['meta']['title']}.mid")

        self.mid.save(f"{self.output}")


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

        song2.fill_measures()

        song2.write_midi_file()
