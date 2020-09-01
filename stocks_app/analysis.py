# file for performing analysis on stock data
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt


def get_fourier_peaks(x):
    peaks, properties = find_peaks(x, height=500, distance=2)
    fig = plt.figure(num='Fourier transform', figsize=(18, 8), dpi=80, facecolor='w', edgecolor='k')
    ax = fig.add_subplot(1, 2, 2)
    _ = plt.hist(peaks)
    return peaks, properties, _, ax


if __name__ == '__main__':
    peaks, properties = get_fourier_peaks(3)
    print(peaks)
