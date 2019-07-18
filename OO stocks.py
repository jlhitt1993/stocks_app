# Program that gets data from the stock market and performs analysis on it based on the users commands

import numpy as np
import pandas as pd
import json
import urllib.request
import time
import matplotlib.pyplot as pl
from scipy.fftpack import fft

url = "https://www.alphavantage.co/query"
api_key = 'BY1OVG40O9CEKQY4'


class Name:
    def __init__(self, name):
        self.name = name


class Stock(Name):
    def __init__(self, name):
        Name.__init__(self, name)
        request = urllib.request.Request(url + '?function=TIME_SERIES_DAILY&symbol=' + name +
                           '&outputsize=full&interval=1min&apikey=' + api_key)
        response = urllib.request.urlopen(request)
        data = json.load(response)
        prices = data['Time Series (Daily)']
        count = 0
        self.days = []
        self.high = []
        self.open = []
        self.close = []
        self.volume = []
        self.low = []
        for d in prices:
            self.high.append(float(prices[d]['2. high']))   # t is tick, d is date. value is the keyword for the desired data
            self.low.append(float(prices[d]['3. low']))
            self.open.append(float(prices[d]['1. open']))
            self.close.append(float(prices[d]['4. close']))
            self.volume.append(float(prices[d]['5. volume']))
            self.days.append(count)   # count is number of days for each tick
            count += 1
        print('Got: ' + name + '')
        time.sleep(0.5)


Stocks = {}


def stocks(*args):
    for arg in args:
        Stocks[arg] = Stock(arg)


def help():
    print('Welcome to help.\nStart by getting data about a stock ex. aapl = Stock(\'aapl\')')
    print('Afterwards, you can access data of daily high, low, open, close and volume like aapl.high')
    print('You can make plots like spectrum(aapl.high, amd.high). Other plots are correlation(),'
          'percent_change() and fourier()')
    print('For more help, see the documentation at www.placeholder.com')


def spectrum(*args):
    sts, st, tag = [], [], []
    c = len(args)
    if c % 2 != 0:
        print('must pass a stock with the legend label after \nUse help() for more info')
        return -1
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
        pl.plot(st[i].days, sts[i], label=st[i].name + '-' + tag[i])
    pl.legend(loc='upper right', scatterpoints=1, prop={'size': 24}, fontsize=8)
    pl.show()


def correlation(*args):
    print(len(args))
    for i in range(len(args)-1):
        for ii in range(i+1, len(args)):
            c = np.corrcoef(args[i], args[ii])[0][1]
            print('Corrcoef: ', c)
            pl.scatter(args[i], args[ii], s=1, label=i+ii)
            legend = pl.legend(loc='upper right', scatterpoints=1, prop={'size': 24}, fontsize=10)
    #legend.set_sizes([34])
    pl.show()


def percent_change(*args):
    pc = [[]]
    for h in range(len(args)):
        for i in range(len(args[h])-1):
            pc[h].append((args[h][i+1]-args[h][i])/(args[h][i]))
        Stock.per_ch = pc[h]
        pl.subplot(len(args), 1, h + 1)
        pl.scatter(args[h][:-1], pc[h], s=1, label=h)
        if h == 0:
            pl.title('Percent change', fontsize=30)
            pl.xlabel('day', fontsize=26)
        pl.legend(loc='upper right', prop={'size': 16})
        pl.ylabel('percent change', fontsize=26)
        pc.append([])
    pl.show()


def fourier(*args):
    x, y, c = [], [], 0
    for arg in args:
        c += 1
    if c % 2 != 0:
        print('must pass pairs of x,y data\n')
        return -1
    counter = 0
    for arg in args:
        half = len(arg) // 2
        if counter % 2 == 0:
            x.append(arg)
        if counter % 2 == 1:
            if len(arg) % 2 == 0:
                y.append(np.abs(fft(arg)[0:half]))
            if len(arg) % 2 == 1:
                y.append(np.abs(fft(arg)[0:half]))
        counter += 1
    for i in range(c//2):
        pl.plot(x[i][0:half], y[i])
    pl.xlabel('days', fontsize=26)
    pl.title('Fourier transform', fontsize=30)
    pl.ylabel('FT', fontsize=26)
    pl.show()
    return

#def scaled():
#    print()



aapl = Stock('aapl')
amd = Stock('amd')
msft = Stock('msft')
#correlation(aapl.close, aapl.high, amd.close)
#percent_change(aapl.high, amd.low)
#print(amd.per_ch)
spectrum(amd, 'high', aapl, 'high', msft, 'volume')
#helpme()

