# import mido
# from mido import Message
# import mingus.core.chords as chords
# from mingus.containers import NoteContainer, Note
# from mingus.midi import fluidsynth
# import random
from __future__ import annotations

import click
from exercice import MusicExercice


@click.command()
@click.option(
    '--exercice',
    prompt='The exercice definition yaml file',
    help='The exercice definition yaml file',
)
def run(exercice):
    ex = MusicExercice(yaml_definition=exercice)
    ex.exercice_loop()


if __name__ == '__main__':
    run()
