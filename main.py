import sys
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", type=int, default=100, help="Duration of a single beat in milliseconds")
    parser.add_argument("-o", type=str, help="octave shift (e.g. +1, -2)", default="0")
    parser.add_argument("path", type=str, help="Path to the text file containing notes", nargs="?")
    return parser.parse_args()


def note_to_tone(note: str, duration=200, octave_shift="0") -> str:
    """
    Convert a note string like 'D2' or 'G#4' to the format '[:t <freq> 200]'.
    Frequencies are rounded to whole numbers.
    """
    if "_" in note:
        return f"_<{duration}>"
    # Frequencies by octave
    freq_table = {
        0: {"C": 16, "C#": 17, "Db": 17, "D": 18, "D#": 19, "Eb": 19, "E": 21, "F": 22, "F#": 23, "Gb": 23,
            "G": 24, "G#": 26, "Ab": 26, "A": 28, "A#": 29, "Bb": 29, "B": 31},
        1: {"C": 33, "C#": 35, "Db": 35, "D": 37, "D#": 39, "Eb": 39, "E": 41, "F": 44, "F#": 46, "Gb": 46,
            "G": 49, "G#": 52, "Ab": 52, "A": 55, "A#": 58, "Bb": 58, "B": 62},
        2: {"C": 65, "C#": 69, "Db": 69, "D": 73, "D#": 78, "Eb": 78, "E": 82, "F": 87, "F#": 92, "Gb": 92,
            "G": 98, "G#": 104, "Ab": 104, "A": 110, "A#": 117, "Bb": 117, "B": 123},
        3: {"C": 131, "C#": 139, "Db": 139, "D": 147, "D#": 156, "Eb": 156, "E": 165, "F": 175, "F#": 185, "Gb": 185,
            "G": 196, "G#": 208, "Ab": 208, "A": 220, "A#": 233, "Bb": 233, "B": 247},
        4: {"C": 262, "C#": 277, "Db": 277, "D": 294, "D#": 311, "Eb": 311, "E": 330, "F": 349, "F#": 370, "Gb": 370,
            "G": 392, "G#": 415, "Ab": 415, "A": 440, "A#": 466, "Bb": 466, "B": 494},
        5: {"C": 523, "C#": 554, "Db": 554, "D": 587, "D#": 622, "Eb": 622, "E": 659, "F": 698, "F#": 740, "Gb": 740,
            "G": 784, "G#": 831, "Ab": 831, "A": 880, "A#": 932, "Bb": 932, "B": 988},
        6: {"C": 1047, "C#": 1109, "Db": 1109, "D": 1175, "D#": 1245, "Eb": 1245, "E": 1319, "F": 1397, "F#": 1480, "Gb": 1480,
            "G": 1568, "G#": 1661, "Ab": 1661, "A": 1760, "A#": 1865, "Bb": 1865, "B": 1976},
        7: {"C": 2093, "C#": 2217, "Db": 2217, "D": 2349, "D#": 2489, "Eb": 2489, "E": 2637, "F": 2794, "F#": 2960, "Gb": 2960,
            "G": 3136, "G#": 3322, "Ab": 3322, "A": 3520, "A#": 3729, "Bb": 3729, "B": 3951},
        8: {"C": 4186, "C#": 4435, "Db": 4435, "D": 4699, "D#": 4978, "Eb": 4978, "E": 5274, "F": 5588, "F#": 5920, "Gb": 5920,
            "G": 6272, "G#": 6645, "Ab": 6645, "A": 7040, "A#": 7459, "Bb": 7459, "B": 7902},
    }

    # Extract note name and octave
    if len(note) == 2:
        name, octave = note[0], int(note[1])
        accidental = ""
    else:
        name, accidental, octave = note[0], note[1], int(note[2])

    full_name = name + accidental

    if octave_shift != "0":
        octave += int(octave_shift)

    # Lookup
    freq = freq_table[octave][full_name]

    return f":t {freq} {duration}"


def text_to_code(file_path: str, beat_duration=100, octave_shift=0) -> str:
    codes = []
    with open(file_path, "r") as f:
        for note_line in f.readlines():
            note, n_beats = note_line.split(' ')
            codes.append(note_to_tone(note, int(n_beats) * beat_duration, octave_shift))
    return " ".join(codes)


if __name__ == "__main__":
    args = parse_arguments()
    filepath = sys.argv[1]
    code = text_to_code(args.path, args.b, args.o)
    with open("output.txt", "w") as f:
        f.write(f"[{code}]")


