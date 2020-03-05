# Program that gets data from the stock market and performs analysis on it based on the users commands
from _datetime import datetime as dt
import numpy as np
import pandas as pd
import json
import urllib.request
import time
import matplotlib.pyplot as pl
import plotly.graph_objects as go
from scipy.fftpack import rfft
from pandas.plotting import register_matplotlib_converters

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
            self.high.append(float(prices[d]['2. high']))   # t is tick, d is date. value is the keyword for the desired data
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
    for i in range(len(sts)):
        pl.plot_date(st[i].dates, sts[i], xdate=True, label=st[i].name + '-' + tag[i])
    pl.legend(loc='upper right', scatterpoints=1, prop={'size': 24}, fontsize=8, markerscale=6)
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
            print('Corrcoef: ', c)
            pl.scatter(sts[i], sts[ii], s=1, label=st[i].name + '-' + tag[i] + '/' + st[ii].name + '-' + tag[ii] +
                       str(c)[:6])
    pl.legend(loc='upper right', scatterpoints=1, prop={'size': 24}, fontsize=10, markerscale=7)
    # legend.set_sizes([34])
    pl.show()


def percent_change(*args, **kwargs):
    pc = [[]]
    for h in range(len(args)):
        for i in range(len(args[h])-1):
            pc[h].append((args[h][i+1]-args[h][i])/(args[h][i]))
        Stock.per_ch = pc[h]
        pl.subplot(len(args), 1, h + 1)
        pl.scatter(args[h][:-1], pc[h], s=1, label=kwargs["labels"][h])
        if h == 0:
            pl.title('Percent change', fontsize=30)
            pl.xlabel('day', fontsize=26)
        pl.legend(loc='upper right', prop={'size': 16}, markerscale=7)
        pl.ylabel('percent change', fontsize=26)
        pc.append([])
    pl.show()


def fourier(*args):
    x, y, c = [], [], 0
    '''for arg in args:
        c += 1
    if c % 2 != 0:
        print('must pass stock and data label \nUse help() for more info')
        return'''
    counter = 0
    for arg in args:
        half = len(arg.days) // 2
        #if counter % 2 == 0:
        x.append(arg.days)
        if len(arg.days) % 2 == 0:
            y.append(np.abs(rfft(arg.high)))
        if len(arg.days) % 2 == 1:
            y.append(np.abs(rfft(arg.high)))
        counter += 1
    for i in range(len(args)):
        pl.plot(x[i], y[i])
    pl.xlabel('days', fontsize=26)
    pl.title('Fourier transform', fontsize=30)
    pl.ylabel('FT', fontsize=26)
    #pl.legend(loc='upper right', prop={'size': 16}, markerscale=7)
    pl.show()
    return

#def scaled():
#    print()



#aapl = Stock('aapl')
#amd = Stock('amd')
#msft = Stock('msft')
#candlestick(amd)
#correlation(aapl,'high',amd, 'low')
#percent_change(aapl.high, amd.low, labels=["aapl.high", "amd.low"])
#spectrum(amd, 'high')
#fourier(aapl, amd)
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
'''