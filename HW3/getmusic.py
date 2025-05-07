import argparse
import numpy as np
import wave
import os

MODE = {
    "Ionian":     [2, 4, 5, 7, 9, 11],
    "Dorian":     [2, 3, 5, 7, 9, 10],
    "Phrygian":   [1, 3, 5, 7, 8, 10],
    "Lydian":     [2, 4, 6, 7, 9, 11],
    "Mixolydian": [2, 4, 5, 7, 9, 10],
    "Aeolian":    [2, 3, 5, 7, 8, 10],
    "Locrian":    [1, 3, 5, 6, 8, 10]
}

KEY = {
    "C":  0,
    "C#": 1,
    "D":  2,
    "D#": 3,
    "E":  4,
    "F":  5,
    "F#": 6,
    "G":  7,
    "G#": 8,
    "A":  9,
    "A#": 10,
    "B":  11
}

def parse_args():
    parser = argparse.ArgumentParser(
        prog="getmusic",
        description="Convert numbered musical notation to a .wav file."
    )
    parser.add_argument("--score", type=int, nargs="+", required=True, help="Note list (1-7), 0 means rest")
    parser.add_argument("--beat", type=float, nargs="+", required=True, help="Beats for each note (in quarter note units)")
    parser.add_argument("--name", type=str, default="default", help="Output filename (without .wav)")
    parser.add_argument("--bpm", type=float, default=120.0, help="Beats per minute (default: 120)")
    parser.add_argument("--key", type=str, default="C", help="Key (default: C)")
    parser.add_argument("--octave", type=int, default=4, help="Octave (default: 4)")
    parser.add_argument("--mode", type=str, default="Ionian", help="Mode (default: Ionian)")
    parser.add_argument("--volume", type=float, default=1.0, help="Volume (0.0 to 1.0)")
    parser.add_argument("--standard", type=float, default=261.63, help="Standard frequency for C4 (default: 261.63 Hz)")
    return parser.parse_args()

def getmusic(score, beat, name, bpm, key, octave, mode, volume, standard):
    fs = 44100
    spb = 60.0 / bpm

    freq = []

    diff = ((octave - 1) * 12 + KEY[key]) - 36
    freq.append(standard * (2 ** (diff / 12)))

    for i in range(1, 7):
        freq.append(freq[0] * 2 ** (MODE[mode][i - 1] / 12))

    signal = np.zeros(0, dtype=np.int16)

    for n, b in zip(score, beat):
        duration = b * spb
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)

        if n == 0:
            y = np.zeros_like(t)
        else:
            y = np.sin(2 * np.pi * freq[n - 1] * t)

        y_int16 = (y * volume * 32767).astype(np.int16)
        signal = np.concatenate((signal, y_int16))

    with wave.open(f"./results/{name}.wav", 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(signal.tobytes())

if __name__ == '__main__':
    args = parse_args()
    args.key  = args.key.upper()
    args.mode = args.mode.capitalize()

    if len(args.score) != len(args.beat):
        raise ValueError("`score` and `beat` must have the same length")
    if any(n < 0 or n > 7 for n in args.score):
        raise ValueError("`score` values must be between 1 and 7")
    if args.bpm <= 0:
        raise ValueError("`bpm` must be positive")
    if args.octave < 1 or args.octave > 7:
        raise ValueError("`octave` must be between 1 and 7")
    if args.mode not in MODE:
        raise ValueError(f"`mode` must be one of {list(MODE.keys())}")
    if args.key not in KEY:
        raise ValueError(f"`key` must be one of {list(KEY.keys())}")
    if args.standard <= 0:
        raise ValueError("`standard` must be greater than 0")
    if not (0.0 <= args.volume <= 1.0):
        raise ValueError("`volume` must be between 0.0 and 1.0")

    os.makedirs("./results", exist_ok=True)
    getmusic(args.score, args.beat, args.name, args.bpm, args.key, args.octave, args.mode, args.volume, args.standard)
    print(f"Successfully generated {args.name}.wav")
