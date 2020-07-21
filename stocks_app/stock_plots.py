# Defines functions that make plots

import numpy as np
import matplotlib.pyplot as pl
import plotly.graph_objects as go
from scipy.fftpack import rfft
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


def check_length(stocks, labels):
    """
    Used at the beginning of plot functions to make sure that the number of stocks and labels match
    :param stocks: list. List of stocks passed to plotting function.
    :param labels: list. List of labels passed to plotting function.
    :return: bool. False if the lengths are not equal, True otherwise.
    """
    if (len(stocks) != (len(labels))):
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
        if kwargs['labels'][i] == 'high':
            sts.append(kwargs['stocks'][i].high)
        elif kwargs['labels'][i] == 'low':
            sts.append(kwargs['stocks'][i].low)
        elif kwargs['labels'][i] == 'open':
            sts.append(kwargs['stocks'][i].open)
        elif kwargs['labels'][i] == 'close':
            sts.append(kwargs['stocks'][i].close)
        elif kwargs['labels'][i] == 'volume':
            sts.append(kwargs['stocks'][i].volume)
        else:
            print("invalid label for " + kwargs['stocks'][i].name)
            return
    fig1 = pl.figure(num='Spectrum', figsize=(18, 8), dpi=80, facecolor='w', edgecolor='k')
    for i in range(len(kwargs['stocks'])):
        pl.plot_date(kwargs['stocks'][i].dates, sts[i], xdate=True,
                     label=(kwargs['stocks'][i].name + '-' + kwargs['labels'][i]))
    pl.title("Spectrum", fontsize=28)
    pl.legend(loc='upper left', scatterpoints=1, prop={'size': 24}, fontsize=8, markerscale=3)
    #fig1.canvas.manager.window.move(0, 0)
    pl.show()


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
    sts = []
    for i in range(len(kwargs['stocks'])):
        if kwargs['labels'][i] == 'high':
            sts.append(kwargs['stocks'][i].high)
        elif kwargs['labels'][i] == 'low':
            sts.append(kwargs['stocks'][i].low)
        elif kwargs['labels'][i] == 'open':
            sts.append(kwargs['stocks'][i].open)
        elif kwargs['labels'][i] == 'close':
            sts.append(kwargs['stocks'][i].close)
        elif kwargs['labels'][i] == 'volume':
            sts.append(kwargs['stocks'][i].volume)
        else:
            print("invalid label for " + kwargs['stocks'][i].name)
            return
    fig2 = pl.figure(num='Correlation', figsize=(10, 9), dpi=80, facecolor='w', edgecolor='k')
    for i in range(len(sts)-1):
        for ii in range(i+1, len(sts)):
            c = np.corrcoef(sts[i], sts[ii])[0][1]
            pl.scatter(sts[i], sts[ii], s=1, label=kwargs['stocks'][i].name + '-' + kwargs['labels'][i] + '/' +
                       kwargs['stocks'][ii].name + '-' + kwargs['labels'][ii] + ' ' + str(c)[:6])
            pl.title("Correlation", fontsize=28)
    pl.legend(loc='upper right', scatterpoints=1, prop={'size': 17}, fontsize=7, markerscale=7)
    # legend.set_sizes([34])
    #fig2.canvas.manager.window.move(0, 0)
    pl.show()


def percent_change(**kwargs):
    check = check_length(kwargs['stocks'], kwargs['labels'])
    if not check:
        return
    pc = [[]]
    dates = []
    for h in range(len(kwargs['stocks'])):
        if kwargs["labels"][h] == "high":
            for i in range(len(kwargs['stocks'][h].high)-1):
                pc[h].append((kwargs['stocks'][h].high[i+1]-kwargs['stocks'][h].high[i]) /
                             (kwargs['stocks'][h].high[i]))
        elif kwargs["labels"][h] == "low":
            for i in range(len(kwargs['stocks'][h].low)-1):
                pc[h].append((kwargs['stocks'][h].low[i+1]-kwargs['stocks'][h].low[i]) /
                             (kwargs['stocks'][h].low[i]))
        elif kwargs["labels"][h] == "close":
            for i in range(len(kwargs['stocks'][h].high)-1):
                pc[h].append((kwargs['stocks'][h].close[i+1]-kwargs['stocks'][h].close[i]) /
                             (kwargs['stocks'][h].close[i]))
        elif kwargs["labels"][h] == "open":
            for i in range(len(kwargs['stocks'][h].high)-1):
                pc[h].append((kwargs['stocks'][h].open[i+1]-kwargs['stocks'][h].open[i]) /
                             (kwargs['stocks'][h].open[i]))
        elif kwargs["labels"][h] == "volume":
            for i in range(len(kwargs['stocks'][h].high)-1):
                pc[h].append((kwargs['stocks'][h].volume[i+1]-kwargs['stocks'][h].volume[i]) /
                             (kwargs['stocks'][h].volume[i]))
        else:
            print("Invalid label argument")
            return
        dates.append(kwargs['stocks'][h].dates)
        fig3 = pl.figure(num='Percent change', figsize=(18, 9), dpi=80, facecolor='w', edgecolor='k')
        ax = fig3.add_subplot(len(kwargs['stocks']), 1, h + 1)
        pl.plot_date(dates[h][1:], pc[h], markersize=2, label=(kwargs['stocks'][h].name + '-' + kwargs["labels"][h]))
        if h == 0:
            pl.title('Percent change', fontsize=28)
        pl.legend(loc='upper right', prop={'size': 16}, handletextpad=-0.2, handlelength=0)
        pl.ylabel('percent change (%)')
        ax.set_xlim([kwargs['stocks'][h].dates[1], kwargs['stocks'][h].dates[-1]])
        pc.append([])
    pl.xlabel('day', fontsize=26)
    #fig3.canvas.manager.window.move(0, 0)
    pl.show()


def fourier(**kwargs):
    check = check_length(kwargs['stocks'], kwargs['labels'])
    if not check:
        return
    y = []
    for h in range(len(kwargs['stocks'])):
        y.append([])
        if kwargs["labels"][h] == "high":
            y[h].append(np.abs(rfft(kwargs['stocks'][h].high)))
        elif kwargs["labels"][h] == "low":
            y[h].append(np.abs(rfft(kwargs['stocks'][h].low)))
        elif kwargs["labels"][h] == "close":
            y[h].append(np.abs(rfft(kwargs['stocks'][h].close)))
        elif kwargs["labels"][h] == "open":
            y[h].append(np.abs(rfft(kwargs['stocks'][h].open)))
        elif kwargs["labels"][h] == "volume":
            y[h].append(np.abs(rfft(kwargs['stocks'][h].volume)))
        else:
            print("Invalid label argument")
            return
    fig4 = pl.figure(num='Fourier transform', figsize=(18, 8), dpi=80, facecolor='w', edgecolor='k')
    ax = fig4.add_subplot()
    for i in range(len(kwargs['stocks'])):
        pl.plot(kwargs['stocks'][i].days, np.transpose(y[i]), label=(kwargs['stocks'][i].name +
                                                                     '-' + kwargs['labels'][i]))
    pl.xlabel('days', fontsize=26)
    pl.title('Fourier transform', fontsize=28)
    pl.ylabel('FT', fontsize=26)
    pl.legend(loc='upper right', prop={'size': 16}, markerscale=7)
    ax.set_xlim(-10, 400)
    #fig4.canvas.manager.window.move(0, 0)
    pl.show()
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
