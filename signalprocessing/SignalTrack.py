import logging
import os
import numpy as np
from scipy.signal import find_peaks
from scipy.io import wavfile
from .PitchesData import pitches, pitches_ranges
import matplotlib.pyplot as plt

"""use SignalTrackDriver.py to run"""

logger = logging.getLogger(__name__)


def freq_axis(fft_size, fs):
    """Returns a list of frequencies which correspond to the bins in the returned data from stft()"""
    return np.arange(fft_size) / np.float32(fft_size * 2) * fs


def time_axis(total_segments, t_max):
    """Returns a list of times which correspond to the bins in the returned data from stft()"""
    return np.arange(total_segments) / np.float32(total_segments) * t_max


# https://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/
def fft(x):
    """A vectorized, non-recursive version of the Cooley-Tukey FFT"""
    x = np.asarray(x, dtype=float)
    N = x.shape[0]

    if np.log2(N) % 1 > 0:
        raise ValueError("size of x must be a power of 2")

    # N_min here is equivalent to the stopping condition above,
    # and should be a power of 2
    N_min = min(N, 32)

    # Perform an O[N^2] DFT on all length-N_min sub-problems at once
    n = np.arange(N_min)
    k = n[:, None]
    M = np.exp(-2j * np.pi * n * k / N_min)
    X = np.dot(M, x.reshape((N_min, -1)))

    # build-up each level of the recursive calculation all at once
    while X.shape[0] < N:
        X_even = X[:, :int(X.shape[1] / 2)]
        X_odd = X[:, int(X.shape[1] / 2):]
        factor = np.exp(-1j * np.pi * np.arange(X.shape[0])
                        / X.shape[0])[:, None]
        X = np.vstack([X_even + factor * X_odd,
                       X_even - factor * X_odd])

    return X.ravel()


def stft(fft_size, data, pad_end_size, total_segments, hop_size, args):
    if args.window == 'bartlett':
        window = np.bartlett(fft_size)
    elif args.window == 'blackman':
        window = np.blackman(fft_size)
    elif args.window == 'hamming':
        window = np.hamming(fft_size)
    elif args.window == 'hanning':
        window = np.hanning(fft_size)
    else:
        window = None

    inner_pad = np.zeros(fft_size)  # the zeros which will be used to double each segment size

    proc = np.concatenate((data, np.zeros(pad_end_size)))  # the data to process
    result = np.empty((total_segments, fft_size), dtype=np.float32)  # space to hold the result

    for i in range(total_segments):  # for each segment
        current_hop = hop_size * i  # figure out the current segment offset
        segment = proc[current_hop:current_hop + fft_size]  # get the current segment
        windowed = segment * window  # multiply by the half cosine function
        padded = np.append(windowed, inner_pad)  # add 0s to double the length of the data
        spectrum = fft(padded) / fft_size  # take the Fourier Transform and scale by the number of samples
        autopower = np.abs(spectrum * np.conj(spectrum))  # find the autopower spectrum
        result[i, :] = autopower[:fft_size]  # append to the results array
    return result


def convert_idx_to_time(time_list, idx):
    return time_list[idx]


def convert_idxlist_to_timelist(time_list, idxlist):
    return [convert_idx_to_time(time_list, x) for x in idxlist]


def detect_pitch(magnitudes, freq_list, args):
    n = args.topindex
    indices = np.argpartition(magnitudes, -n)[-n:]
    # logger.debug(f'indices {indices}')
    return freq_list[min(indices)]


def find_key(pitch):
    # print(f"pitch: {pitch}")
    if pitch < pitches_ranges[0][0] or pitch > pitches_ranges[-1][0]:
        return None
    else:
        for i in range(1, len(pitches_ranges)):
            if pitch < pitches_ranges[i][0]:
                return pitches_ranges[i][1]


def detect_hits(result_not_cutoff, loudness_factor, args, freq_list, time_list):
    result = process_results(result_not_cutoff, freq_list)
    max_magn = -1
    mean_amp = [np.average(bins) for bins in result]
    median_amp = [np.median(bins) for bins in result]
    mean_amp_notcutoff = [np.average(bins) for bins in result_not_cutoff]
    for bins in result:
        if np.average(bins) > max_magn:
            max_magn = np.average(bins)
    hits = []

    loudness_offset = max_magn * loudness_factor  # kinda arbitrary needs to be something to distinguish between index where no hit has taken place and beginning of hit
    indexes, _ = find_peaks(mean_amp, threshold=None, height=loudness_offset, prominence=loudness_offset, distance=3)
    logger.debug(f'loudnessoffset:\t{loudness_offset}')
    for i in range(1, len(mean_amp)):
        if mean_amp[i] > mean_amp[i - 1] + loudness_offset:
            hits.append(i)
    if args.plot:
        plt.plot(mean_amp, '.-')
        plt.title('Average amplitude of frequency bins in signal')
        plt.xlabel('Time in frames')
        plt.ylabel('Mean Amplitude')
        plt.show()
    # logger.debug(f'hits:\t{hits}')
    # logger.debug(f'scipy:\t{indexes.tolist()}')
    scipy_times = convert_idxlist_to_timelist(time_list, indexes.tolist())
    logger.debug(f'scipy_times:\t{[round(x, 2) for x in scipy_times]}')
    logger.debug(f'mean_amp:\t{[round(mean_amp[idx], 2) for idx in indexes]}')
    logger.debug(f'median_amp:\t{[round(median_amp[idx], 2) for idx in indexes]}')
    return indexes.tolist(), mean_amp_notcutoff


def find_cutoffs(freq_list):
    low_index_cutoff = -1
    upper_index_cutoff = -1
    for i, val in enumerate(freq_list):
        if val > 900:
            low_index_cutoff = i
            break
    for i in range(len(freq_list)):
        if freq_list[len(freq_list) - 1 - i] < 2300:
            upper_index_cutoff = len(freq_list) - 1 - i
            break
    return low_index_cutoff, upper_index_cutoff


def process_results(result, freq_list):
    result_scale = 20 * np.log10(result)  # scale to db
    result_clip = np.clip(result_scale, 0, 120)  # clip values
    low_index_cutoff, upper_index_cutoff = find_cutoffs(freq_list)
    results_cutoff = []
    for bin_list in result_clip:
        results_cutoff.append(bin_list[
                              low_index_cutoff:upper_index_cutoff])  # remove some of the frequencies we dont need  freq_val < 900 or freq_val > 2300
    return results_cutoff


def pitch_track_wrap(args_dict):
    global logger
    args = args_dict
    logger_levels = {
        'critical': 50,
        'error': 40,
        'warning': 30,
        'info': 20,
        'debug': 10,
    }
    logger.setLevel(level=logger_levels[args.level])
    if not len(logger.handlers):
        logger.addHandler(logging.StreamHandler())
    logger.info("Starting script")

    key_and_times, results_transposed, time_list, freq_list, low_index_cutoff, upper_index_cutoff, fft_size, overlap_fac, loudness_factor, fs, data, hop_size, averages, freq_and_times = pitch_track_calc(
        args, is_logging=True)
    if args.plot:
        plt.imshow(results_transposed, origin='lower', cmap='jet', interpolation='nearest', aspect='auto',
                   extent=[time_list[0], time_list[-1], freq_list[low_index_cutoff],
                           freq_list[upper_index_cutoff]])
        plt.title('results transposed')
        plt.show()

    # !!! FINAL RESULT !!!

    logger.info(f'key_and_time\t{[(key, round(times, 2)) for (key, times) in key_and_times]}')
    if args.guiplot:
        return key_and_times, plt.imshow(results_transposed, origin='lower', cmap='jet', interpolation='nearest',
                                         aspect='auto',
                                         extent=[time_list[0], time_list[-1], freq_list[low_index_cutoff],
                                                 freq_list[upper_index_cutoff]])
    return key_and_times


def find_pitch_recursively(results, freq_list, args, idx, offset, threshold=1):
    if find_key(detect_pitch(results[idx + offset], freq_list, args)) is None and idx + offset < len(
            results) and offset < threshold:
        return find_pitch_recursively(results, freq_list, args, idx, (offset + 1), threshold)
    else:
        return find_key(detect_pitch(results[idx + offset], freq_list, args))


def pitch_track_calc(args, is_logging=False):
    # https://kevinsprojects.wordpress.com/2014/12/13/short-time-fourier-transform-using-python-and-numpy/
    sound_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'data/{args.name}')
    fs, data = wavfile.read(sound_file_path)

    fft_size = int(args.fftsize)

    if is_logging:
        logger.debug(f'path:\t{sound_file_path}')
        logger.debug(f'fs:\t\t{fs}')
        logger.debug(f'fftsize:\t{fft_size}')
        logger.debug(f'fs/fft:\t\t{fs / fft_size}')

    overlap_fac = 0.5
    loudness_factor = 0.4  # determines senitivity off hit detection

    hop_size = np.int32(np.floor(fft_size * (1 - overlap_fac)))
    pad_end_size = fft_size  # the last segment can overlap the end of the data array by no more than one window size
    total_segments = np.int32(np.ceil(len(data) / np.float32(hop_size)))
    t_max = len(data) / np.float32(fs)

    freq_list = freq_axis(fft_size, fs)
    time_list = time_axis(total_segments, t_max)
    low_index_cutoff, upper_index_cutoff = find_cutoffs(freq_list)
    freq_list_cutoff = freq_list[low_index_cutoff:upper_index_cutoff]

    result = stft(data=data, fft_size=fft_size, pad_end_size=pad_end_size, total_segments=total_segments,
                  hop_size=hop_size, args=args)

    hits_cutoff, averages = detect_hits(result, loudness_factor, args, freq_list, time_list)
    results_cutoff = process_results(result, freq_list)
    key_and_times = []
    freq_and_times = []
    for hit_idx in hits_cutoff:
        pitch = find_pitch_recursively(results=results_cutoff, freq_list=freq_list_cutoff, args=args, idx=hit_idx,
                                       offset=0)

        if hit_idx == len(results_cutoff) - 1:
            pitch = detect_pitch(results_cutoff[hit_idx + 0], freq_list_cutoff, args)
        elif hit_idx < len(results_cutoff) - 1:
            pitch = detect_pitch(results_cutoff[hit_idx + 1], freq_list_cutoff, args)
            if (find_key(pitch) is None) and (hit_idx < len(results_cutoff) - 2):
                pitch = detect_pitch(results_cutoff[hit_idx + 2], freq_list_cutoff, args)
        key = find_key(pitch)
        key_and_times.append((key, convert_idx_to_time(time_list, hit_idx)))
        freq_and_times.append((pitch, convert_idx_to_time(time_list, hit_idx)))
        if is_logging:
            pass
            # logger.debug(f'pitch: {pitch}, time: {convert_idx_to_time(time_list, hit_idx)}')

    results_transposed = np.transpose(results_cutoff)
    return key_and_times, results_transposed, time_list, freq_list, low_index_cutoff, upper_index_cutoff, fft_size, overlap_fac, loudness_factor, fs, data, hop_size, averages, freq_and_times
