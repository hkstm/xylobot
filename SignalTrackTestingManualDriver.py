import argparse
import datetime
import os
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

from signalprocessing.SignalArgParser import add_arguments
from signalprocessing.SignalTrack import pitch_track_wav

spectogram3dtest = False
flatnesstest = False
spectogramtest = False
createcsv = True

parser = argparse.ArgumentParser(description="Custom Pitch")
parser = add_arguments(parser)
args = parser.parse_args()

pitches = [
    ('c6', 1053),
    ('d6', 1182),
    ('e6', 1324),
    ('f6', 1399),
    ('g6', 1570),
    ('a6', 1764.8),
    ('b6', 1974.5),
    ('c7', 2101),
]

scale_fw_fast_filenames = [
    'scale_fw_fast_1',
    'scale_fw_fast_2',
    'scale_fw_fast_3',
    'scale_fw_fast_4',
    'scale_fw_fast_5',
]
scale_bw_fast_filenames = [
    'scale_bw_fast_1',
    'scale_bw_fast_2',
    'scale_bw_fast_3',
    'scale_bw_fast_4',
    'scale_bw_fast_5',
]
scale_fw_slow_filenames = [
    'scale_fw_slow_1',
    'scale_fw_slow_2',
    'scale_fw_slow_3',
    'scale_fw_slow_4',
    'scale_fw_slow_5',
]
scale_bw_slow_filenames = [
    'scale_bw_slow_1',
    'scale_bw_slow_2',
    'scale_bw_slow_3',
    'scale_bw_slow_4',
    'scale_bw_slow_5',
]

scale_fast_filenames = scale_fw_fast_filenames + scale_bw_fast_filenames
scale_slow_filenames = scale_fw_fast_filenames + scale_bw_fast_filenames


def normalize_data(data, average_magnitudes):
    normalized = []
    for i_data in range(len(average_magnitudes)):
        normalized.append(data[i_data] / average_magnitudes[i_data])
    return normalized


def dropandgetlowestvalue(dataframe, actual_seq_string, analyzed_seq_string):
    row_length, col_length = dataframe.shape
    min_val = dataframe.values.min()
    for idx_row in range(row_length):
        for idx_col in range(col_length):
            if min_val == dataframe.iat[idx_row, idx_col]:
                seq_actual_tobedropped = dataframe.columns[idx_col]
                seq_analyzed_tobedropped = dataframe.index[idx_row]
                dataframe = dataframe.drop(dataframe.columns[idx_col], axis=1)
                dataframe = dataframe.drop(dataframe.index[idx_row])
                return dataframe, seq_actual_tobedropped, seq_analyzed_tobedropped


def check_correct_hits(actual_seq, analyzed_seq):
    check_df = pd.DataFrame(index=analyzed_seq, columns=actual_seq)
    for idx_col in range(len(actual_seq)):
        for idx_row in range(len(analyzed_seq)):
            actual_key, actual_time = actual_seq[idx_col]
            analyzed_key, analyzed_time = analyzed_seq[idx_row]
            check_df.iat[idx_row, idx_col] = abs(actual_time - analyzed_time)

    row_length, col_length = check_df.shape
    aligned_seq_actual = []
    aligned_seq_analyzed = []
    while col_length >= 1 and row_length >= 1:
        check_df, seq_actual_dropped, seq_analyzed_dropped = dropandgetlowestvalue(check_df, actual_seq, analyzed_seq)
        aligned_seq_actual.append(seq_actual_dropped)
        aligned_seq_analyzed.append(seq_analyzed_dropped)
        row_length, col_length = check_df.shape

    actualtimes = [time for (key, time) in aligned_seq_actual]
    sorted_indices = np.argsort(actualtimes)
    timesorted_aligned_seq_actual = [aligned_seq_actual[idx] for idx in sorted_indices]
    timesorted_aligned_seq_analyzed = [aligned_seq_analyzed[idx] for idx in sorted_indices]

    time_error = 0
    key_error = row_length
    for i_timesorted_aligned in range(len(timesorted_aligned_seq_actual)):
        actual_key_timesorted_aligned, actual_time_timesorted_aligned = timesorted_aligned_seq_actual[
            i_timesorted_aligned]
        analyzed_key_timesorted_aligned, analyzed_time_timesorted_aligned = timesorted_aligned_seq_analyzed[
            i_timesorted_aligned]
        time_error += abs(actual_time_timesorted_aligned - analyzed_time_timesorted_aligned)

        if actual_key_timesorted_aligned != analyzed_key_timesorted_aligned:
            key_error += 1

    result = {
        'time_error': (time_error / len(timesorted_aligned_seq_actual)),
        'key_error': key_error,
        'seq_actual': timesorted_aligned_seq_actual,
        'seq_analyzed': timesorted_aligned_seq_analyzed,
    }
    return SimpleNamespace(**result)


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


def scale_decibel(data):
    return 10.0 * np.log10(data)


def time_resolution(time_list):
    return time_list[-1] / len(time_list)


def create_uniform_sequence(start_time, end_time, reverse=False):
    uniform_seq = []
    for idx_uni_seq, (key, _) in enumerate(pitches):
        current_time = start_time + idx_uni_seq * (end_time - start_time) / len(pitches)
        uniform_seq.append((key, current_time))

    if not reverse:
        return uniform_seq
    else:
        uniform_seq.reverse()
        return uniform_seq

amount_of_runs_test = 10
position_test = 'Center'
hit_method_test = 'Manual'
playingstyle = 'Slow'

if createcsv:
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
    effective_duration = []
    max_delay_p = []
    hit_method_p = []
    clip_length_p = []
    executiontime_p = []

if not createcsv:
    amount_of_runs_test = 1

for i in range(amount_of_runs_test):
    argsdict = {
        'name': scale_slow_filenames[i],
        'plot': args.plot,
        'guiplot': args.guiplot,
        'level': args.level,
        'window': args.window,
        'fftsize': args.fftsize,
        'topindex': args.topindex,
    }

    starttime = time.process_time()
    pitchtrack_resNS = pitch_track_wav(SimpleNamespace(**argsdict))
    endtime = time.process_time()

    if spectogram3dtest:
        nperseg = 2 ** 12
        noverlap = 2 ** 11
        f, t, Sxx = signal.spectrogram(pitchtrack_resNS.data, pitchtrack_resNS.fs, nperseg=nperseg, noverlap=noverlap)

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
        flatness = librosa.feature.spectral_flatness(y=pitchtrack_resNS.data.astype(float),
                                                     n_fft=pitchtrack_resNS.fft_size,
                                                     hop_length=pitchtrack_resNS.hop_size)
        # flatness = librosa.feature.spectral_flatness(y=noisy_signal.astype(float), n_fft=fft_size, hop_length=hop_size)
        print(f' mean flatness: {np.mean(flatness)}')
        normalized = normalize_data(flatness[0], pitchtrack_resNS.averages)
        normalized_scaled = scale_decibel(normalized)

        plt.plot(pitchtrack_resNS.time_list, normalized_scaled)
        plt.xlabel('Time in seconds')
        plt.ylabel('Noise intensity normalized by signal magnitude')
        plt.title('Flatness')
        plt.show()

    if spectogramtest:
        img = plt.imshow(pitchtrack_resNS.results_transposed, origin='lower', cmap='jet', interpolation='nearest',
                         aspect='auto',
                         extent=[pitchtrack_resNS.time_list[0], pitchtrack_resNS.time_list[-1],
                                 pitchtrack_resNS.freq_list[pitchtrack_resNS.low_index_cutoff],
                                 pitchtrack_resNS.freq_list[pitchtrack_resNS.upper_index_cutoff]])
        plt.title('Spectogram')
        plt.xlabel('Time in seconds')
        plt.ylabel('Frequency in Hz')
        plt.show()

    if createcsv:
        start_key_res, start_time_res = pitchtrack_resNS.key_and_times[0]
        end_key_res, end_time_res = pitchtrack_resNS.key_and_times[-1]
        actual_seq = create_uniform_sequence(start_time_res, end_time_res, True if i % 10 >= 5 else False)
        analyzed_seq = pitchtrack_resNS.key_and_times
        print(f'file name: \t {scale_slow_filenames[i]}')
        print(pitchtrack_resNS.key_and_times)
        print(f'unallgined actual: {actual_seq}')
        print(f'unallgined analyzed: {analyzed_seq}')

        res_correct_check = check_correct_hits(actual_seq=actual_seq,
                                               analyzed_seq=analyzed_seq)
        actual_seq = res_correct_check.seq_actual
        analyzed_seq = res_correct_check.seq_analyzed

        filename_p.append(argsdict['name'])
        run_p.append(i)
        position_p.append(position_test)
        key_error_p.append(res_correct_check.key_error)
        time_error_p.append(res_correct_check.time_error)
        length_difference_p.append(len(pitchtrack_resNS.key_and_times) - len(actual_seq))
        flatness_p.append(
            np.mean(librosa.feature.spectral_flatness(y=pitchtrack_resNS.data.astype(float),
                                                      n_fft=pitchtrack_resNS.fft_size,
                                                      hop_length=pitchtrack_resNS.hop_size)))
        fftsize_p.append(argsdict['fftsize'])
        window_p.append(argsdict['window'])
        topindex_p.append(argsdict['topindex'])
        seq_length_p.append(len(actual_seq))
        effective_duration.append(end_time_res - start_time_res)
        max_delay_p.append(playingstyle)
        hit_method_p.append(hit_method_test)
        clip_length_p.append(pitchtrack_resNS.time_list[-1])
        executiontime_p.append(endtime - starttime)
        print(f'actual {actual_seq}')
        print(f'analyz {analyzed_seq}')

if createcsv:
    df = pd.DataFrame({'Filename': filename_p,
                       'Run': run_p,
                       'Position': position_p,
                       'KeyError': key_error_p,
                       'TimeError': time_error_p,
                       'LengthDiffSeq': length_difference_p,
                       'MeanFlatness': flatness_p,
                       'FFTSize': fftsize_p,
                       'Window': window_p,
                       'TopIndex': topindex_p,
                       'SequenceLength': seq_length_p,
                       'EffDuration': effective_duration,
                       'PlayingStyle': max_delay_p,
                       'HitMethod': hit_method_p,
                       'ClipLength': clip_length_p,
                       'ExecutionTime': executiontime_p,
                       })

    currentdt = datetime.datetime.now()
    df.to_csv(r'signalprocessing\data\csvs\test_' + currentdt.strftime("%m-%d_%H-%M-%S") + '.csv')
