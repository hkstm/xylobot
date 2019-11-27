import argparse
import logging
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

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


def freq_axis(fft_size, fs):
    """Returns a list of frequencies which correspond to the bins in the returned data from stft()"""
    return np.arange(fft_size) / np.float32(fft_size * 2) * fs


def time_axis(total_segments, t_max):
    """Returns a list of times which correspond to the bins in the returned data from stft()"""
    return np.arange(total_segments) / np.float32(total_segments) * t_max

#https://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/
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

def stft(fft_size, data, pad_end_size, total_segments, hop_size, ):
    window = np.hanning(fft_size)  # our half cosine window
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


def detect_pitch(magnitudes, freq_list):
    n = 1
    indices = np.argpartition(magnitudes, -n)[-n:]
    return freq_list[min(indices)]


def find_key(pitch):
    # print(f"pitch: {pitch}")
    if pitch < pitches_ranges[0][0] or pitch > pitches_ranges[-1][0]:
        return None
    else:
        for i in range(1, len(pitches_ranges)):
            if pitch < pitches_ranges[i][0]:
                return pitches_ranges[i][1]


def detect_hits(result, loudness_factor):
    averages = []
    max_magn = -1
    for i, bins in enumerate(result):
        if np.average(bins) > max_magn:
            max_magn = np.average(bins)
        print(f'max: {max_magn}')
        averages.append(np.average(bins))
    hits = []
    loudness_offset = max_magn * loudness_factor  # kinda arbitrary needs to be something to distinguish between index where no hit has taken place and beginning of hit
    print(f'loudness offset: {loudness_offset}')
    for i in range(1, len(averages)):
        if averages[i] > averages[i - 1] + loudness_offset:
            hits.append(i)
    if args.plot:
        plt.plot(averages, '.-')
        plt.show()
    return hits


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
    result = 20 * np.log10(result)  # scale to db
    result = np.clip(result, 0, 120)  # clip values
    low_index_cutoff, upper_index_cutoff = find_cutoffs(freq_list)
    results_cutoff = []
    for bin_list in result:
        results_cutoff.append(bin_list[
                              low_index_cutoff:upper_index_cutoff])  # remove some of the frequencies we dont need  freq_val < 900 or freq_val > 2300
    return results_cutoff


logging.basicConfig(level=logging.INFO)
logging.info("Starting script")
parser = argparse.ArgumentParser(description="Custom Pitch")
parser.add_argument('-n', '--name', help="Name of audio file")
parser.add_argument('-p', '--plot',  action='store_true')
args = parser.parse_args()
logging.info("Parsed arguments")

# https://kevinsprojects.wordpress.com/2014/12/13/short-time-fourier-transform-using-python-and-numpy/
fs, data = wavfile.read(f'./data/{args.name}')
fft_size = 2 ** 12
overlap_fac = 0.5
loudness_factor = 0.4  # determines senitivity off hit detection

hop_size = np.int32(np.floor(fft_size * (1 - overlap_fac)))
pad_end_size = fft_size  # the last segment can overlap the end of the data array by no more than one window size
total_segments = np.int32(np.ceil(len(data) / np.float32(hop_size)))
t_max = len(data) / np.float32(fs)

freq_list = freq_axis(fft_size, fs)
time_list = time_axis(total_segments, t_max)
low_index_cutoff, upper_index_cutoff =  find_cutoffs(freq_list)
freq_list_cutoff = freq_list[low_index_cutoff:upper_index_cutoff]

result = stft(data=data, fft_size=fft_size, pad_end_size=fft_size, total_segments=total_segments, hop_size=hop_size)

results_cutoff = process_results(result, freq_list)

hits = detect_hits(results_cutoff, loudness_factor)
key_and_times = []
for hit_idx in hits:
    pitch = detect_pitch(results_cutoff[hit_idx], freq_list_cutoff)
    print(f'pitch: {pitch}, time: {convert_idx_to_time(time_list, hit_idx)}')
    key_and_times.append((find_key(pitch), convert_idx_to_time(time_list, hit_idx)))


results_transposed = np.transpose(results_cutoff)
if args.plot:
    img = plt.imshow(results_transposed, origin='lower', cmap='jet', interpolation='nearest', aspect='auto',
                     extent=[time_list[0], time_list[-1], freq_list[low_index_cutoff], freq_list[upper_index_cutoff]])
    plt.show()

# !!! FINAL RESULT !!!

print(key_and_times)