# file for performing analysis on stock data
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt


def get_fourier_peaks(x, ax, label):
    peaks, properties = find_peaks(x, height=500, distance=2)
    ax.hist(peaks, alpha=0.3, label=label, bins=25)
    ax.set_xlabel("Frequency (", fontsize=26)
    ax.set_ylabel("Count", fontsize=26)
    ax.set_title("Frequencies", fontsize=28)
    ax.set_xlim(0,)
    ax.legend(loc='upper right', prop={'size': 16}, markerscale=7)
    return peaks, properties


if __name__ == '__main__':
    fig, ax = plt.subplots()
    peaks, properties = get_fourier_peaks(3)
    print(peaks)
