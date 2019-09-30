from __future__ import division
from numpy import argmax, mean, diff, nonzero
from scipy.signal import correlate
from time import time
import sys
import soundfile as sf


from signalprocessing.parabolic import parabolic


def freq_from_crossings(sig, fs):
    """
    Estimate frequency by counting zero crossings
    """
    # Find all indices right before a rising-edge zero crossing
    indices = nonzero((sig[1:] >= 0) & (sig[:-1] < 0))[0]

    # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
    # crossings = indices

    # More accurate, using linear interpolation to find intersample
    # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
    crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]

    # Some other interpolation based on neighboring points might be better.
    # Spline, cubic, whatever

    return fs / mean(diff(crossings))


def freq_from_autocorr(sig, fs):
    """
    Estimate frequency using autocorrelation
    """
    # Calculate autocorrelation and throw away the negative lags
    corr = correlate(sig, sig, mode='full')
    corr = corr[len(corr)//2:]

    # Find the first low point
    d = diff(corr)
    start = nonzero(d > 0)[0][0]

    # Find the next peak after the low point (other than 0 lag).  This bit is
    # not reliable for long signals, due to the desired peak occurring between
    # samples, and other peaks appearing higher.
    # Should use a weighting function to de-emphasize the peaks at longer lags.
    peak = argmax(corr[start:]) + start
    px, py = parabolic(corr, peak)

    return fs / px


filename = sys.argv[1]

print('Reading file "%s"\n' % filename)

signal, fs = sf.read(filename)
print('Calculating frequency from zero crossings:', end=' ')
start_time = time()
print('%f Hz' % freq_from_crossings(signal, fs))
print('Time elapsed: %.3f s\n' % (time() - start_time))

print('Calculating frequency from autocorrelation:', end=' ')
start_time = time()
print('%f Hz' % freq_from_autocorr(signal, fs))
print('Time elapsed: %.3f s\n' % (time() - start_time))