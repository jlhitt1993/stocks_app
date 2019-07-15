# Program that gets data from the stock market and performs analysis on it based on the users commands

import numpy as np
import pandas as pd
import json
import urllib.request
import time
import matplotlib.pyplot as pl

url = "https://www.alphavantage.co/query"
api_key = 'BY1OVG40O9CEKQY4'


def helpme():
    print('Help is on the way')


def spectrum(*args):
    x, y = [[]]
    count = 0
    for i in args:
        count +=1
    if count % 2 != 0:


            x[i].append()

            y[i].append()

    pl.plot(x, y)
    pl.show()


def correlation(**kwargs):


    c = np.corrcoef(x, y)[0][1]
    print('Corrcoef: ', c)
    pl.scatter(xs, ys, s=1, label = )
    legend = pl.legend(loc='upper right', scatterpoints=1, prop={'size': 24}, fontsize=10)
    #legend.set_sizes([34])
    pl.show()


def percent_change(*args):
    pc = [[]]
    for h in range(len(args)):
        for i in range(len(args[h])-1):
            pc[h].append((args[h][i+1]-args[h][i])/(args[h][i]))
        pl.subplot(len(args), 1, h + 1)
        pl.scatter(args[h][:-1], pc[h], s=1, label=h)
        if h == 0:
            pl.title('Percent change', fontsize=30)
            pl.xlabel('day', fontsize=26)
        pl.legend(loc='upper right', prop={'size': 16})
        pl.ylabel('percent change', fontsize=26)
        pc.append([])
    pl.show()


def fourier():
    print()


def scaled():
    print()


class Stock:
    def __init__(self, ticker):
        self.name = ticker
        request = urllib.request.Request(url + '?function=TIME_SERIES_DAILY&symbol=' + ticker +
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
        print('Got: ' + ticker)
        time.sleep(0.5)


aapl = Stock('aapl')
amd = Stock('amd')
percent_change(aapl.high, amd.low, amd.high,aapl.volume)


