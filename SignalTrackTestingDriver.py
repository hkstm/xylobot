import argparse
import datetime
import os
import random
import threading
import time
import wave
from types import SimpleNamespace

import librosa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyaudio
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from scipy import signal

from control.ControlManager import ControlManager
from control.SongManager import Note
from signalprocessing.SignalArgParser import add_arguments
from signalprocessing.SignalTrack import pitch_track_wav

spectogram3dtest = False
flatnesstest = True
spectogramtest = False
recordaudioflag = False

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
    for i_analysed_seq in range(len(analysed_seq)):
        key, time = analysed_seq[i_analysed_seq]
        if reverse:
            key, time = analysed_seq[len(analysed_seq) - 1 - i_analysed_seq]
        scale_key, scale_time = pitches[i_analysed_seq]
        if key != scale_key:
            return False
    return True


def normalize_data(data, average_magnitudes):
    normalized = []
    for i_data in range(len(average_magnitudes)):
        normalized.append(data[i_data] / average_magnitudes[i_data])
    return normalized


def check_correct_hits(actual_seq, analyzed_seq):
    time_error = 0
    key_error = abs(len(actual_seq) - len(analyzed_seq))
    shortest_length = len(actual_seq) if len(actual_seq) <= len(analyzed_seq) else len(analyzed_seq)
    for i in range(shortest_length):
        actual_key, actual_time = actual_seq[i]
        analyzed_key, analyzed_time = analyzed_seq[i]
        time_error += abs(actual_time - analyzed_time)
        print(f'actual key: {actual_key}')
        print(f'analyzed key: {analyzed_key}')
        if actual_key != analyzed_key:
            key_error += 1
    if shortest_length == 0:
        return -1, key_error
    return (time_error / shortest_length), key_error


def generate_random_sequence(seq_length, min_delay=0.1, max_delay=1):
    random_sequence = []
    for i_seq_length in range(seq_length):
        random_sequence.append(Note(key=pitches[random.randint(0, len(pitches) - 1)][0], delay=random.uniform(min_delay, max_delay)))
    return random_sequence


def scale_decibel(data):
    return 10.0 * np.log10(data)


def time_resolution(time_list):
    return time_list[-1] / len(time_list)


def convertnote2seq(notelist):
    seqlist = []
    for i_notelist in range(len(notelist)):
        seqlist.append((notelist[i_notelist].key, notelist[i_notelist].delay))
    return seqlist

generate_random_sequence(10)

amount_of_runs_test = 10
seq_length_test = 10
record_time_test = 10
position_test = 'Center'
min_delay_test = 0.1
max_delay_test = 0.9
hit_method_test = 'Triangle 1'
if recordaudioflag:
    print('set control manager')
    filename_p = []
    run_p = []
    position_p = []
    key_error_p = []
    time_error_p = []
    length_difference_p = []
    flatness_p = []
    fftsize_p = []
    window_p = []
    topindex_p = []
    seq_length_p = []
    min_delay_p = []
    max_delay_p = []
    hit_method_p = []
    clip_length_p = []
    executiontime_p = []
    controlmanager = ControlManager()

    import control.TestControl as tc

    controlmanager.setNoteCoordinates(tc.coords)

    # audio = None
    # frames = None
    # samplewidth = None



def recordaudio():
    global audio
    global frames
    global samplewidth
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data_recaudio = stream.read(CHUNK)
        frames.append(data_recaudio)

    stream.stop_stream()
    stream.close()
    samplewidth = audio.get_sample_size(FORMAT)
    audio.terminate()


if not recordaudioflag:
    amount_of_runs_test = 1

# controlmanager = ControlManager()
#
# import control.TestControl as tc
#
# controlmanager.setNoteCoordinates(tc.coords)
# sequence_test = generate_random_sequence(seq_length_test, min_delay_test, max_delay_test)
# controlmanager.addSong('sdsf', 100, sequence_test)
# controlmanager.play()
#
for i in range(amount_of_runs_test):

    if recordaudioflag:
        print('recording audio')
        sequence_test = generate_random_sequence(seq_length_test, min_delay_test, max_delay_test)

        controlmanager.addSong('sdsf', 100, sequence_test)
        print(f'length {len(sequence_test)}')

        print(convertnote2seq(sequence_test))
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = record_time_test
        starttime = time.time()
        print('Starting thread')
        t1 = threading.Thread(target=recordaudio)
        t1.start()
        controlmanager.play()
        t1.join()
        endtime = time.time()
        print(f'time elapsed {endtime - starttime}')
        global audio
        global frames
        global samplewidth

        currentdt = datetime.datetime.now()
        WAVE_OUTPUT_FILENAME = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                            f'signalprocessing\\data\\testclip_{currentdt.strftime("%m-%d_%H-%M-%S")}.wav')
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(samplewidth)
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
    starttime = time.process_time()
    key_and_times, results_transposed, time_list, freq_list, low_index_cutoff, upper_index_cutoff, fft_size, overlap_fac, loudness_factor, fs, data, hop_size, averages, freq_and_times = pitch_track_wav(
        SimpleNamespace(**argsdict))
    endtime = time.process_time()
    print(f'data type {type(data)}')
    print(f'timeres {time_resolution(time_list)}')
    print(f'pitches{pitches}')
    print(f'{key_and_times}')
    # print(freq_and_times)
    print(f'Correct scale: {correctscale(key_and_times)}')
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
        # noise = np.random.normal(0, 10, len(data))
        # noisy_signal = data + noise
        flatness = librosa.feature.spectral_flatness(y=data.astype(float), n_fft=fft_size, hop_length=hop_size)
        # flatness = librosa.feature.spectral_flatness(y=noisy_signal.astype(float), n_fft=fft_size, hop_length=hop_size)
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
        plt.title('Spectogram')
        plt.xlabel('Time in seconds')
        plt.ylabel('Frequency in Hz')
        plt.show()

    if recordaudioflag:
        time_error_seq, key_error_seq = check_correct_hits(actual_seq=convertnote2seq(sequence_test),
                                                           analyzed_seq=key_and_times)
        filename_p.append(argsdict['name'])
        run_p.append(i)
        position_p.append(position_test)
        key_error_p.append(key_error_seq)
        time_error_p.append(time_error_seq)
        length_difference_p.append(len(key_and_times) - len(convertnote2seq(sequence_test)))
        flatness_p.append(
            np.mean(librosa.feature.spectral_flatness(y=data.astype(float), n_fft=fft_size, hop_length=hop_size)))
        fftsize_p.append(argsdict['fftsize'])
        window_p.append(argsdict['window'])
        topindex_p.append(argsdict['topindex'])
        seq_length_p.append(seq_length_test)
        min_delay_p.append(min_delay_test)
        max_delay_p.append(max_delay_test)
        hit_method_p.append(hit_method_test)
        clip_length_p.append(time_list[-1])
        executiontime_p.append(endtime - starttime)
        print(f'actual {convertnote2seq(sequence_test)}')
        print(f'analyz {key_and_times}')

if recordaudioflag:
    df = pd.DataFrame({'Filename': filename_p,
                       'Run': run_p,
                       'Position': position_p,
                       'KeyError': key_error_p,
                       'TimeError': time_error_p,
                       'LengthDiffAnalyzedActual': length_difference_p,
                       'MeanFlatness': flatness_p,
                       'FFTSize': fftsize_p,
                       'Window': window_p,
                       'TopIndex': topindex_p,
                       'SequenceLength': seq_length_p,
                       'MinDelay': min_delay_p,
                       'MaxDelay': max_delay_p,
                       'HitMethod': hit_method_p,
                       'ClipLength': clip_length_p,
                       'ExecutionTime': executiontime_p,
                       })

    currentdt = datetime.datetime.now()
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            f'signalprocessing\\data\\clip_{currentdt.strftime("%m-%d_%H-%M-%S")}.wav')
    df.to_csv(r'signalprocessing\data\csvs\test_' + currentdt.strftime("%m-%d_%H-%M-%S") + '.csv')
