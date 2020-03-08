# Program that gets data from the stock market and performs analysis on it based on the users commands
from _datetime import datetime as dt
import datetime
import numpy as np
import pandas as pd
import json
import urllib.request
import time
import matplotlib.pyplot as pl
import plotly.graph_objects as go
from scipy.fftpack import rfft
from pandas.plotting import register_matplotlib_converters
from matplotlib.pyplot import figure

register_matplotlib_converters()
url = "https://www.alphavantage.co/query"
api_key = 'BY1OVG40O9CEKQY4'
#pd.plotting.register_matplotlib_converters()


class Name:
    def __init__(self, name):
        self.name = name


class Stock(Name):
    def __init__(self, name):
        Name.__init__(self, name)
        #request = urllib.request.Request(url + '?function=TIME_SERIES_DAILY&symbol=' + name +
        #                   '&outputsize=full&interval=1min&apikey=' + api_key)
        #response = urllib.request.urlopen(request)
        #data = json.load(response)
        data = json.load(open(str(name) + '.json'))
        prices = data['Time Series (Daily)']
        count = 0
        self.days = []
        self.high = []
        self.open = []
        self.close = []
        self.volume = []
        self.low = []
        self.dates = []
        for d in prices:
            self.high.append(float(prices[d]['2. high']))   #d is date. value is the keyword for the desired data
            self.low.append(float(prices[d]['3. low']))
            self.open.append(float(prices[d]['1. open']))
            self.close.append(float(prices[d]['4. close']))
            self.volume.append(float(prices[d]['5. volume']))
            self.days.append(count)   # count is number of days for each tick
            self.dates.append(dt.strptime(d, '%Y-%m-%d'))
            count += 1
        print('Got: ' + name + '')
        time.sleep(0.5)


Stocks = {}


def stocks(*args):
    for arg in args:
        Stocks[arg] = Stock(arg)


def help():
    print('Welcome to help.\nStart by getting data about a stock ex. aapl = Stock(\'aapl\')')
    print('You can make plots by spectrum(aapl, \'high\', amd, \'high\'). Other plots are correlation(),'
          'percent_change(), candlestick and fourier()')
    print('For more help, see the documentation and examples at www.placeholder.com')


def spectrum(*args):
    sts, st, tag = [], [], []
    c = len(args)
    if c % 2 != 0:
        print('must pass a stock with the legend label after \nUse help() for more info')
        return
    counter = 0
    for arg in args:
        if counter % 2 == 0:
            st.append(arg)
        if counter % 2 == 1:
            tag.append(arg)
        counter += 1
    for i in range(len(st)):
        if tag[i] == 'high':
            sts.append(st[i].high)
        if tag[i] == 'low':
            sts.append(st[i].low)
        if tag[i] == 'open':
            sts.append(st[i].open)
        if tag[i] == 'close':
            sts.append(st[i].close)
        if tag[i] == 'volume':
            sts.append(st[i].volume)
    pl.figure(num='Spectrum', figsize=(18, 8), dpi=80, facecolor='w', edgecolor='k')
    for i in range(len(sts)):
        pl.plot_date(st[i].dates, sts[i], xdate=True, label=st[i].name + '-' + tag[i])
    pl.title("Spectrum", fontsize=28)
    pl.legend(loc='upper right', scatterpoints=1, prop={'size': 24}, fontsize=8, markerscale=3)
    mngr = pl.get_current_fig_manager()
    mngr.window.geometry("1000x700+0+0")
    pl.show()


def candlestick(arg):
    fig = go.Figure(data=[go.Candlestick(x=arg.dates, open=arg.open, high=arg.high, low=arg.low, close=arg.close)])
    fig.update_layout(title=arg.name, yaxis_title='Price ($)')
    fig.show()


def correlation(*args):
    if len(args) % 2 != 0 or len(args) < 4:
        print('Must pass at least two stocks and data labels \nUse help() for more info')
        return
    counter, tag, st, sts = 0, [], [], []
    for arg in args:
        if counter % 2 == 0:
            st.append(arg)
        if counter % 2 == 1:
            tag.append(arg)
        counter += 1
    for i in range(len(st)):
        if tag[i] == 'high':
            sts.append(st[i].high)
        if tag[i] == 'low':
            sts.append(st[i].low)
        if tag[i] == 'open':
            sts.append(st[i].open)
        if tag[i] == 'close':
            sts.append(st[i].close)
        if tag[i] == 'volume':
            sts.append(st[i].volume)
    for i in range(len(sts)-1):
        for ii in range(i+1, len(sts)):
            c = np.corrcoef(sts[i], sts[ii])[0][1]
            pl.figure(num='Correlation', figsize=(10, 9), dpi=80, facecolor='w', edgecolor='k')
            pl.scatter(sts[i], sts[ii], s=1, label=st[i].name + '-' + tag[i] + '/' + st[ii].name + '-' + tag[ii] +
                       str(c)[:6])
            pl.title("Correlation", fontsize=28)
    pl.legend(loc='upper right', scatterpoints=1, prop={'size': 17}, fontsize=7, markerscale=7)
    # legend.set_sizes([34])
    mngr = pl.get_current_fig_manager()
    mngr.window.geometry("1000x700+0+0")
    pl.show()


def percent_change(*args, **kwargs):
    pc = [[]]
    dates = []
    for h in range(len(args)):
        if kwargs["labels"][h] == "high":
            for i in range(len(args[h].high)-1):
                pc[h].append((args[h].high[i+1]-args[h].high[i])/(args[h].high[i]))
        elif kwargs["labels"][h] == "low":
            for i in range(len(args[h].low)-1):
                pc[h].append((args[h].low[i+1]-args[h].low[i])/(args[h].low[i]))
        elif kwargs["labels"][h] == "close":
            for i in range(len(args[h].high)-1):
                pc[h].append((args[h].close[i+1]-args[h].close[i])/(args[h].close[i]))
        elif kwargs["labels"][h] == "open":
            for i in range(len(args[h].high)-1):
                pc[h].append((args[h].open[i+1]-args[h].open[i])/(args[h].open[i]))
        elif kwargs["labels"][h] == "volume":
            for i in range(len(args[h].high)-1):
                pc[h].append((args[h].volume[i+1]-args[h].volume[i])/(args[h].volume[i]))
        else:
            print("Invalid label argument")
            return
        dates.append(args[h].dates)
        fig = pl.figure(num='Percent change', figsize=(18, 9), dpi=80, facecolor='w', edgecolor='k')
        ax = fig.add_subplot(len(args), 1, h + 1)
        pl.plot_date(dates[h][1:], pc[h], markersize=2, label=(args[h].name + '-' + kwargs["labels"][h]))
        if h == 0:
            pl.title('Percent change', fontsize=28)
        pl.xlabel('day', fontsize=26)
        pl.legend(loc='upper right', prop={'size': 16}, markerscale=4)
        pl.ylabel('percent change', fontsize=26)
        ax.set_xlim([args[h].dates[1], args[h].dates[-1]])
        pc.append([])
    mngr = pl.get_current_fig_manager()
    mngr.window.geometry("1000x700+0+0")
    pl.show()


def fourier(*args, **kwargs):
    y = []
    for h in range(len(args)):
        y.append([])
        if kwargs["labels"][h] == "high":
            y[h].append(np.abs(rfft(args[h].high)))
        elif kwargs["labels"][h] == "low":
            y[h].append(np.abs(rfft(args[h].low)))
        elif kwargs["labels"][h] == "close":
            y[h].append(np.abs(rfft(args[h].close)))
        elif kwargs["labels"][h] == "open":
            y[h].append(np.abs(rfft(args[h].open)))
        elif kwargs["labels"][h] == "volume":
            y[h].append(np.abs(rfft(args[h].volume)))
        else:
            print("Invalid label argument")
            return
    fig = pl.figure(num='Fourier transform', figsize=(18, 8), dpi=80, facecolor='w', edgecolor='k')
    ax = fig.add_subplot()
    for i in range(len(args)):
        pl.plot(args[i].days, np.transpose(y[i]), label=(args[i].name + '-' + kwargs['labels'][i]))
    pl.xlabel('days', fontsize=26)
    pl.title('Fourier transform', fontsize=28)
    pl.ylabel('FT', fontsize=26)
    pl.legend(loc='upper right', prop={'size': 16}, markerscale=7)
    ax.set_xlim(-10, 400)
    mngr = pl.get_current_fig_manager()
    mngr.window.geometry("1000x700+0+0")
    pl.show()
    return

#def scaled():
#    print()


#aapl = Stock('aapl')
#amd = Stock('amd')
#msft = Stock('msft')
#candlestick(amd)
#correlation(aapl,'high',amd, 'low')
#percent_change(aapl, amd, labels=["high", "low"])
#spectrum(amd, 'high')
#fourier(aapl, amd, labels=["high", "low"])
#help()

# things to add
'''
1) create ability to read a script file for loading a large amount of 
stocks and performing a lot of analysis
2) Create the option to read json data from the local machine or internet
3) add Bollinger bands and candle sticks to spectrum 
4) create executable to share with others
5) add anything interesting from atom finance
6) create website and or document with detailed instructions
7) The program needs to look for trends by analyzing the relationships between a large number of stocks
8) Be able to select a date range to consider
'''