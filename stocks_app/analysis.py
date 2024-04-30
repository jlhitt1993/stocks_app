# file for performing analysis on stock data
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt


def get_fourier_peaks(x, freq, ax, label):
    peak_ind, properties = find_peaks(x, height=500, distance=2)
    ax.hist(freq[peak_ind], alpha=0.3, label=label, bins=100)
    ax.set_xlabel("Frequency (1/day)", fontsize=26)
    ax.set_ylabel("Count", fontsize=26)
    ax.set_title("Frequencies", fontsize=28)
    ax.set_xlim(-0.1, 0.2)
    ax.legend(loc='upper right', prop={'size': 16}, markerscale=7)
    return peak_ind, properties


if __name__ == '__main__':
    fig, ax = plt.subplots()
    peaks, properties = get_fourier_peaks(3)
    print(peaks)
