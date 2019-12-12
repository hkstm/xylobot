import argparse
import math
import os
from random import random
import random
from types import SimpleNamespace

import librosa
import numpy as np
from matplotlib import cm
from scipy import signal
import pyaudio
import wave
import matplotlib.pyplot as plt
import datetime

from Control.SongManager import Note
from signalprocessing.SignalParser import add_arguments
from signalprocessing.custompitchtracking import pitch_track_raw

spectogram3dtest = False
flatnesstest = True
spectogramtest = False
recordaudio = False

parser = argparse.ArgumentParser(description="Custom Pitch")
parser = add_arguments(parser)
args = parser.parse_args()

pitches = [
    ('c6', 1047),
    ('d6', 1175),
    ('e6', 1319),
    ('f6', 1397),
    ('g6', 1568),
    ('a6', 1760),
    ('b6', 1976),
    ('c7', 2093),
]


def correctscale(analysed_seq, reverse=False):
    if len(pitches) != len(analysed_seq):
        return False
    for i in range(len(analysed_seq)):
        key, time = analysed_seq[i]
        if reverse:
            key, time = analysed_seq[len(analysed_seq) - 1 - i]
        scale_key, scale_time = pitches[i]
        if key != scale_key:
            return False
    return True


def normalize_data(data, average_magnitudes):
    normalized = []
    for i in range(len(data)):
        normalized.append(data[i] / average_magnitudes[i])
    return normalized


def check_correct_hits(actual_seq, analyzed_seq):
    time_error = 0
    key_error = 0
    for i in range(len(actual_seq)):
        actual_key, actual_time = actual_seq[i]
        analyzed_key, analyzed_time = analyzed_seq[i]
        time_error += math.abs(actual_time - analyzed_time)
        if actual_key != analyzed_key:
            key_error += 1
    return (time_error / len(actual_seq)), key_error


def generate_random_sequence(seq_length, min_delay=0.1, max_delay=1):
    random_sequence = []
    for i in range(seq_length):
        random_sequence.append(Note(pitches[random.randint(0, len(pitches) - 1)], random.uniform(min_delay, max_delay)))
    return random_sequence


def scale_decibel(data):
    return 10.0 * np.log10(data)


def time_resolution(time_list):
    return time_list[-1] / len(time_list)


def convertnote2seq(notelist):
    seqlist = []
    for i in range(len(notelist)):
        print(notelist[i].key)
        print(notelist[i].delay)
        seqlist.append((notelist[i].key, notelist[i].delay))
    return seqlist


amount_of_runs_test = 1
seq_length_test = 10
position_test = 'Center'
min_delay_test = 0.1
max_delay_test = 0.9
hit_method_test = 'Triangle 1'
filename_p = []
run_p = []
position_p = []
key_error_p = []
time_error_p = []
flatness_p = []
fftsize_p = []
window_p = []
topindex_p = []
seq_length_p = []
min_delay_p = []
max_delay_p = []
hit_method_p = []
clip_length_p = []

for i in range(amount_of_runs_test):
    sequence_test = generate_random_sequence(seq_length_test, min_delay_test, max_delay_test)
    if recordaudio:
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 1
        currentdt = datetime.datetime.now()
        WAVE_OUTPUT_FILENAME = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                            f'signalprocessing\\data\\testclip_{currentdt.strftime("%m-%d_%H-%M-%S")}.wav')

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        argsdict = {
            'name': WAVE_OUTPUT_FILENAME.split('\\')[-1],
            'plot': args.plot,
            'guiplot': args.guiplot,
            'level': args.level,
            'window': args.window,
            'fftsize': args.fftsize,
            'topindex': args.topindex,
        }
    else:
        argsdict = {
            'name': args.name,
            'plot': args.plot,
            'guiplot': args.guiplot,
            'level': args.level,
            'window': args.window,
            'fftsize': args.fftsize,
            'topindex': args.topindex,
        }

    key_and_times, results_transposed, time_list, freq_list, low_index_cutoff, upper_index_cutoff, fft_size, overlap_fac, loudness_factor, fs, data, hop_size, averages, freq_and_times = pitch_track_raw(
        SimpleNamespace(**argsdict))

    # print(f'pitches{pitches}')
    print(f'{key_and_times}')
    # print(freq_and_times)
    # print(f'Correct scale: {correctscale(key_and_times)}')
    if spectogram3dtest:
        nperseg = 2 ** 12
        noverlap = 2 ** 11
        f, t, Sxx = signal.spectrogram(data, fs, nperseg=nperseg, noverlap=noverlap)

        myfilter = (f > 500) & (f < 3000)

        f = f[myfilter]
        Sxx = Sxx[myfilter, ...]
        Sxx_clipped = np.clip(Sxx, a_min=1, a_max=None)

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        ax.plot_surface(f[:, None], t[None, :], 10.0 * np.log10(Sxx_clipped), cmap=cm.coolwarm)
        ax.set_xlabel('Frequencies in Hz')
        ax.set_ylabel('Time in seconds')
        ax.set_zlabel('Intensity')
        plt.title('Spectogram3D')
        plt.show()

    if flatnesstest:
        # noise = np.random.normal(1, 0.9, len(data))
        # noisy_signal = np.multiply(data, noise)
        noise = np.random.normal(0, 10, len(data))
        noisy_signal = data + noise
        # flatness = librosa.feature.spectral_flatness(y=data.astype(float), n_fft=fft_size, hop_length=hop_size)
        flatness = librosa.feature.spectral_flatness(y=noisy_signal.astype(float), n_fft=fft_size, hop_length=hop_size)
        print(f' mean flatness: {np.mean(flatness)}')
        normalized = normalize_data(flatness[0], averages)
        normalized_scaled = scale_decibel(normalized)

        plt.plot(time_list, normalized_scaled)
        plt.xlabel('Time in seconds')
        plt.ylabel('Noise intensity normalized by signal magnitude')
        plt.title('Flatness')
        plt.show()

    if spectogramtest:
        img = plt.imshow(results_transposed, origin='lower', cmap='jet', interpolation='nearest', aspect='auto',
                         extent=[time_list[0], time_list[-1], freq_list[low_index_cutoff],
                                 freq_list[upper_index_cutoff]])
        plt.title('results transposed')
        plt.show()

    time_error_seq, key_error_seq = check_correct_hits()
    filename_p.append(argsdict['name'])
    run_p.append(i)
    position_p.append(position_test)
    key_error_p.append(key_error_seq)
    time_error_p.append(time_error_seq)
    flatness_p.append(librosa.feature.spectral_flatness(y=data.astype(float), n_fft=fft_size, hop_length=hop_size))
    fftsize_p.append(argsdict['fftsize'])
    window_p.append(argsdict['window'])
    topindex_p.append(argsdict['topindex'])
    seq_length_p.append(seq_length_test)
    min_delay_p.append(min_delay_test)
    max_delay_p.append(max_delay_test)
    hit_method_p.append(hit_method_test)
    clip_length_p.append(time_list[-1])

data = {'Filename': filename_p,
        'Run': run_p,
        'Position': position_p,
        'KeyError': key_error_p,
        'TimeError': time_error_p,
        'Flatness': flatness_p,
        'FFTSize': fftsize_p,
        'Window': window_p,
        'TopIndex': topindex_p,
        'SequenceLength': seq_length_p,
        'MinDelay': min_delay_p,
        'MaxDelay': max_delay_p,
        'HitMethod': hit_method_p,
        'ClipLength': clip_length_p,
        }
