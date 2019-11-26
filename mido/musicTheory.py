
class MusicTheory():

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

    notes = None


    chord_types = {
    # 'major': [4,3],
    # 'minor': [3,4],
    'M7': [4,3,4],
    # '7':[4,3,3],
    # '-7':[3,4,3],
    # '7b5':[3,3,4],
    # 'dim7':[3,3,3]
    }

    def __init__():
        self.notes = { i:self.note[i%12]  for i in range(128) }

