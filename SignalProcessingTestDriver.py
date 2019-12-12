import argparse
from types import SimpleNamespace

import librosa
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from scipy import signal
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.collections import PolyCollection


from signalprocessing.custompitchtracking import pitch_track_raw

spectogram3d = False


parser = argparse.ArgumentParser(description="Custom Pitch")
parser.add_argument('-n', '--name', help="Name of audio file")
args = parser.parse_args()

argsdict = {
    'name': args.name,
    'plot': False,
    'guiplot': False,
    'level': 'DEBUG',
}

def normalize_data(data, average_magnitudes):
    normalized = []
    for i in range(len(data)):
        normalized.append(data[i]/average_magnitudes[i])
    return normalized

def scale_decibel(data):
    return 10.0 * np.log10(data)

key_and_times, results_transposed, time_list, freq_list, low_index_cutoff, upper_index_cutoff, fft_size, overlap_fac, loudness_factor, fs, data, hop_size, averages = pitch_track_raw(SimpleNamespace(**argsdict))

if spectogram3d:
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
    plt.show()

flatness = librosa.feature.spectral_flatness(y=data.astype(float), n_fft=fft_size, hop_length=hop_size)
normalized = normalize_data(flatness[0], averages)
plt.plot(time_list, scale_decibel(normalized))
plt.xlabel('Time in seconds')
plt.ylabel('Noise intensity normalized by signal magnitude')
plt.show()