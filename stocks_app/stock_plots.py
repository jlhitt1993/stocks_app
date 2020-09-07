# Defines functions that make plots

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import plotly.graph_objects as go
from scipy.fftpack import rfft, fftfreq
from pandas.plotting import register_matplotlib_converters
from analysis import get_fourier_peaks
import matplotlib.gridspec as gridspec
import seaborn as sns

register_matplotlib_converters()


def check_length(stocks, labels):
    """
    Used at the beginning of plot functions to make sure that the number of stocks and labels match
    :param stocks: list. List of stocks passed to plotting function.
    :param labels: list. List of labels passed to plotting function.
    :return: bool. False if the lengths are not equal, True otherwise.
    """
    if len(stocks) != (len(labels)):
        print("List of stocks does not match list of labels")
        return False
    else:
        return True


def spectrum(**kwargs):
    sts = []
    check = check_length(kwargs['stocks'], kwargs['labels'])
    if not check:
        return
    for i in range(len(kwargs['stocks'])):
        sts.append(np.empty(len(kwargs['stocks'][i].dates)))
        if kwargs['labels'][i] == 'high':
            sts[i] = kwargs['stocks'][i].high
        elif kwargs['labels'][i] == 'low':
            sts[i] = kwargs['stocks'][i].low
        elif kwargs['labels'][i] == 'open':
            sts[i] = kwargs['stocks'][i].open
        elif kwargs['labels'][i] == 'close':
            sts[i] = kwargs['stocks'][i].close
        elif kwargs['labels'][i] == 'volume':
            sts[i] = kwargs['stocks'][i].volume
        else:
            print("invalid label for " + kwargs['stocks'][i].name)
            return
    fig1, axes = plt.subplots(nrows=1, ncols=1, num='Spectrum', figsize=(18, 8), dpi=80, facecolor='w', edgecolor='k')
    for i in range(len(kwargs['stocks'])):
        axes.plot_date(kwargs['stocks'][i].dates, sts[i], xdate=True,
                     label=(kwargs['stocks'][i].name + '-' + kwargs['labels'][i]), markersize=0.7)
    axes.set_title("Spectrum", fontsize=28)
    axes.set_xlabel("Date", fontsize=20)
    axes.set_ylabel("Price ($)", fontsize=20)
    axes.legend(loc='upper left', scatterpoints=1, prop={'size': 24}, fontsize=8, markerscale=7)
    #fig1.canvas.manager.window.move(0, 0)
    fig1.tight_layout()
    plt.show()


def candlestick(arg):
    fig = go.Figure(data=[go.Candlestick(x=arg.dates, open=arg.open, high=arg.high, low=arg.low, close=arg.close)])
    fig.update_layout(title=arg.name, yaxis_title='Price ($)')
    fig.show()


def correlation(**kwargs):
    check = check_length(kwargs['stocks'], kwargs['labels'])
    if not check:
        return
    if len(kwargs['stocks']) < 2:
        print('Must pass at least two stocks and data labels \nUse help() for more info')
        return
    pc = []
    for h in range(len(kwargs['stocks'])):
        pc.append(np.empty(len(kwargs['stocks'][h].dates) - 1))
        if kwargs["labels"][h] == "high":
            pc[h] = (kwargs['stocks'][h].high[1:] - kwargs['stocks'][h].high[:-1]) / kwargs['stocks'][h].high[1:]
        elif kwargs["labels"][h] == "low":
            pc[h] = (kwargs['stocks'][h].low[1:] - kwargs['stocks'][h].low[:-1]) / kwargs['stocks'][h].low[1:]
        elif kwargs["labels"][h] == "close":
            pc[h] = (kwargs['stocks'][h].close[1:] - kwargs['stocks'][h].close[:-1]) / kwargs['stocks'][h].close[1:]
        elif kwargs["labels"][h] == "open":
            pc[h] = (kwargs['stocks'][h].open[1:] - kwargs['stocks'][h].open[:-1]) / kwargs['stocks'][h].open[1:]
        elif kwargs["labels"][h] == "volume":
            pc[h] = (kwargs['stocks'][h].volume[1:] - kwargs['stocks'][h].volume[:-1]) / kwargs['stocks'][h].volume[1:]
        else:
            print("Invalid label argument")
            return
    fig2, axes = plt.subplots(num='Correlation', figsize=(10, 9), dpi=80, facecolor='w', edgecolor='k')
    for i in range(len(pc)-1):
        for ii in range(i+1, len(pc)):
            c = np.corrcoef(pc[i], pc[ii])[0][1]
            axes.scatter(pc[i], pc[ii], s=1, label=kwargs['stocks'][i].name + '-' + kwargs['labels'][i] + '/' +
                       kwargs['stocks'][ii].name + '-' + kwargs['labels'][ii] + ' ' + str(c)[:6])
    axes.set_title("Correlation of percent change", fontsize=28)
    axes.set_xlabel("First", fontsize=20)
    axes.set_ylabel("Second", fontsize=20)
    plt.legend(loc='upper right', scatterpoints=1, prop={'size': 17}, fontsize=7, markerscale=7)
    # legend.set_sizes([34])
    #fig2.canvas.manager.window.move(0, 0)
    fig2.tight_layout()
    plt.show()


def percent_change(**kwargs):
    check = check_length(kwargs['stocks'], kwargs['labels'])
    if not check:
        return
    pc = []
    axes, names, colors = [], [], sns.color_palette("Paired", len(kwargs['stocks']))
    prob = np.empty(len(kwargs['stocks']))
    fig3 = plt.figure(num='Percent change', figsize=(18, 9), dpi=80, facecolor='w',
                      edgecolor='k')
    spec3 = gridspec.GridSpec(ncols=2, nrows=len(kwargs['stocks']), width_ratios=[len(kwargs['stocks']), 1],
                              height_ratios=[1 for x in range(len(kwargs['stocks'])-1)].append(len(kwargs['stocks'])))
    for h in range(len(kwargs['stocks'])):
        names.append([])
        pc.append(np.empty(len(kwargs['stocks'][h].dates)-1))
        if kwargs["labels"][h] == "high":
            pc[h] = (kwargs['stocks'][h].high[1:] - kwargs['stocks'][h].high[:-1]) / kwargs['stocks'][h].high[1:]
        elif kwargs["labels"][h] == "low":
            pc[h] = (kwargs['stocks'][h].low[1:] - kwargs['stocks'][h].low[:-1]) / kwargs['stocks'][h].low[1:]
        elif kwargs["labels"][h] == "close":
            pc[h] = (kwargs['stocks'][h].close[1:] - kwargs['stocks'][h].close[:-1]) / kwargs['stocks'][h].close[1:]
        elif kwargs["labels"][h] == "open":
            pc[h] = (kwargs['stocks'][h].open[1:] - kwargs['stocks'][h].open[:-1]) / kwargs['stocks'][h].open[1:]
        elif kwargs["labels"][h] == "volume":
            pc[h] = (kwargs['stocks'][h].volume[1:] - kwargs['stocks'][h].volume[:-1]) / kwargs['stocks'][h].volume[1:]
        else:
            print("Invalid label argument")
            return
        prob[h] = np.sum(pc[h][pc[h] > 0])/len(pc[h])
        axes = fig3.add_subplot(spec3[h, 0])
        axes.plot_date(kwargs['stocks'][h].dates[1:], pc[h], markersize=2, label=(kwargs['stocks'][h].name + '-' +
                                            kwargs["labels"][h] + ' P: ' + "{:0.6f}".format(prob[h])), color=colors[h])
        if h == len(kwargs['stocks']):
            axes.set_title('Percent change', fontsize=28)
        axes.legend(loc='upper right', prop={'size': 16}, markerscale=0, handlelength=0, handletextpad=0, fancybox=True)
        axes.set_ylabel('percent change (%)')
        axes.set_xlim([kwargs['stocks'][h].dates[1], kwargs['stocks'][h].dates[-1]])
        names[h] = kwargs['stocks'][h].name
    axes.set_xlabel('day', fontsize=26)
    axes2 = fig3.add_subplot(spec3[0, 1])
    axes2.bar(names, prob, color=colors)
    axes2.set_ylabel('Probability of increase')
    #fig3.canvas.manager.window.move(0, 0)
    fig3.tight_layout()
    plt.show()


def fourier(**kwargs):
    check = check_length(kwargs['stocks'], kwargs['labels'])
    if not check:
        return
    y, freq = [], []
    for h in range(len(kwargs['stocks'])):
        y.append(np.empty(len(kwargs['stocks'][h].dates)))
        freq.append(np.empty(len(kwargs['stocks'][h].dates)))
        if kwargs["labels"][h] == "high":
            y[h] = np.abs(rfft(kwargs['stocks'][h].high))
            freq[h] = fftfreq(len(kwargs['stocks'][h].high), 1)
        elif kwargs["labels"][h] == "low":
            y[h] = np.abs(rfft(kwargs['stocks'][h].low))
            freq[h] = fftfreq(len(kwargs['stocks'][h].days), 1)
        elif kwargs["labels"][h] == "close":
            y[h] = np.abs(rfft(kwargs['stocks'][h].close))
            freq[h] = fftfreq(len(kwargs['stocks'][h].days), 1)
        elif kwargs["labels"][h] == "open":
            y[h] = np.abs(rfft(kwargs['stocks'][h].open))
            freq[h] = fftfreq(len(kwargs['stocks'][h].days), 1)
        elif kwargs["labels"][h] == "volume":
            y[h] = np.abs(rfft(kwargs['stocks'][h].volume))
            freq[h] = fftfreq(len(kwargs['stocks'][h].days), 1)
        else:
            print("Invalid label argument")
            return
    # rcParams.update({'font.size': 18, 'text.usetex': True})
    fig4, axes = plt.subplots(nrows=1, ncols=2, num='Fourier transform', figsize=(18, 8), dpi=80, facecolor='w', edgecolor='k')
    for i in range(len(kwargs['stocks'])):
        axes[0].plot(kwargs['stocks'][i].days, np.transpose(y[i]), label=(kwargs['stocks'][i].name +
                                                                         '-' + kwargs['labels'][i]), alpha=0.4)
    peaks, properties = [], []
    for i in range(len(kwargs['stocks'])):
        peaks.append([])
        properties.append([])
        peaks[i], properties[i] = get_fourier_peaks(y[i], axes[1], label=kwargs['stocks'][i].name +
                                                                         '-' + kwargs['labels'][i])
    axes[0].set_xlabel('1/day', fontsize=26)
    axes[0].set_title('Fourier transform', fontsize=28)
    axes[0].set_ylabel('FT', fontsize=26)
    axes[0].legend(loc='upper right', prop={'size': 16}, markerscale=7)
    axes[0].set_xlim(-10, 1500)
    axes[0].set_ylim(-200, 30000)
    #fig4.canvas.manager.window.move(0, 0)
    fig4.tight_layout()
    plt.show()
    return

if __name__ == '__main__':
    print("Start by creating stock objects like aapl = Stock('aapl') \n")
#    'For testing functions '
#    aapl = Stock('aapl')
#    amd = Stock('amd')
#    msft = Stock('msft')
#    candlestick(amd)
#    correlation(stocks=[aapl, amd], labels=['low', 'low'])
#    percent_change(stocks=[aapl], labels=["high"])
#    spectrum(stocks=[amd, aapl], labels=['high', 'high'])
#    fourier(stocks=[aapl, amd], labels=["high", "low"])
