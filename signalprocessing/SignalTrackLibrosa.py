import argparse
import logging
import librosa
import numpy as np
import matplotlib.pyplot as plt
import wave
import math

pitches = dict([
    (987.8, 'b5'),
    (1047, 'c6'),
    (1175, 'd6'),
    (1319, 'e6'),
    (1397, 'f6'),
    (1568, 'g6'),
    (1760, 'a6'),
    (1976, 'b6'),
    (2093, 'c7'),
    (2349, 'd7'),
])

pitches_ranges = [
    (1017.4, 'b5'),
    (1111, 'c6'),
    (1247, 'd6'),
    (1358, 'e6'),
    (1482.5, 'f6'),
    (1664, 'g6'),
    (1868, 'a6'),
    (2034.5, 'b6'),
    (2221, 'c7'),
]


def find_key(pitch):
    # print(f"pitch: {pitch}")
    if pitch < pitches_ranges[0][0] or pitch > pitches_ranges[-1][0]:
        return None
    else:
        for i in range(1, len(pitches_ranges)):
            if pitch < pitches_ranges[i][0]:
                return pitches_ranges[i][1]


def get_timings_peak(y, sr):
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr, hop_length=None, n_fft=2048, threshold=0.0, fmin=987.8,
                                           fmax=2349)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=512)
    keys = []
    frequencies = []
    for t in range(np.size(magnitudes, 1)):
        if t in onset_frames:
            frequencies.append((detect_pitch(magnitudes, pitches, t), librosa.frames_to_time(t)))
            keys.append((find_key(detect_pitch(magnitudes, pitches, t)), librosa.frames_to_time(t)))
    return frequencies


def detect_pitch(magnitudes, pitches, t):
    n = 1
    indices = np.argpartition(magnitudes[:, t], -n)[-n:]
    return pitches[min(indices), t]


logging.basicConfig(level=logging.INFO)
logging.info("Starting script")

parser = argparse.ArgumentParser(description="Librosa")
parser.add_argument('-n', "--name", help="Name of audio file")
args = parser.parse_args()
logging.info("Parsed arguments")

file_name = args.name
y, sr = librosa.load(file_name)

spf = wave.open(file_name, 'r')
signal = spf.readframes(-1)
signal = np.frombuffer(signal, 'Int16')

freq_timings = get_timings_peak(y, sr)
freq, time = zip(*freq_timings)
for freq, time in freq_timings:
    print(find_key(freq), time)
