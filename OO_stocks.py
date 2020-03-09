# Program that gets data from the stock market and performs analysis on it based on the users commands
from _datetime import datetime as dt
import numpy as np
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


def help():
    print('Welcome to help.\nStart by getting data about a stock ex. aapl = Stock(\'aapl\')')
    print('You can make plots by spectrum(aapl, \'high\', amd, \'high\'). Other plots are correlation(),'
          'percent_change(), candlestick and fourier()')
    print('For more help, see the documentation and examples at www.placeholder.com')


def check_length(stocks, labels):
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
    pl.figure(num='Spectrum', figsize=(18, 8), dpi=80, facecolor='w', edgecolor='k')
    for i in range(len(kwargs['stocks'])):
        pl.plot_date(kwargs['stocks'][i].dates, sts[i], xdate=True,
                     label=(kwargs['stocks'][i].name + '-' + kwargs['labels'][i]))
    pl.title("Spectrum", fontsize=28)
    pl.legend(loc='upper left', scatterpoints=1, prop={'size': 24}, fontsize=8, markerscale=3)
    mngr = pl.get_current_fig_manager()
    mngr.window.geometry("1000x700+0+0")
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
    for i in range(len(sts)-1):
        for ii in range(i+1, len(sts)):
            c = np.corrcoef(sts[i], sts[ii])[0][1]
            pl.figure(num='Correlation', figsize=(10, 9), dpi=80, facecolor='w', edgecolor='k')
            pl.scatter(sts[i], sts[ii], s=1, label=kwargs['stocks'][i].name + '-' + kwargs['labels'][i] + '/' +
                       kwargs['stocks'][ii].name + '-' + kwargs['labels'][ii] + ' ' + str(c)[:6])
            pl.title("Correlation", fontsize=28)
    pl.legend(loc='upper right', scatterpoints=1, prop={'size': 17}, fontsize=7, markerscale=7)
    # legend.set_sizes([34])
    mngr = pl.get_current_fig_manager()
    mngr.window.geometry("1000x700+0+0")
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
        fig = pl.figure(num='Percent change', figsize=(18, 9), dpi=80, facecolor='w', edgecolor='k')
        ax = fig.add_subplot(len(kwargs['stocks']), 1, h + 1)
        pl.plot_date(dates[h][1:], pc[h], markersize=2, label=(kwargs['stocks'][h].name + '-' + kwargs["labels"][h]))
        if h == 0:
            pl.title('Percent change', fontsize=28)
        pl.legend(loc='upper right', prop={'size': 16}, handletextpad=-0.2, handlelength=0)
        pl.ylabel('percent change (%)')
        ax.set_xlim([kwargs['stocks'][h].dates[1], kwargs['stocks'][h].dates[-1]])
        pc.append([])
    pl.xlabel('day', fontsize=26)
    mngr = pl.get_current_fig_manager()
    mngr.window.geometry("1000x700+0+0")
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
    fig = pl.figure(num='Fourier transform', figsize=(18, 8), dpi=80, facecolor='w', edgecolor='k')
    ax = fig.add_subplot()
    for i in range(len(kwargs['stocks'])):
        pl.plot(kwargs['stocks'][i].days, np.transpose(y[i]), label=(kwargs['stocks'][i].name +
                                                                     '-' + kwargs['labels'][i]))
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


' For testing functions '
#aapl = Stock('aapl')
#amd = Stock('amd')
#msft = Stock('msft')
#candlestick(amd)
#correlation(stocks=[aapl, amd], labels=['low', 'low'])
#percent_change(stocks=[aapl, amd], labels=["high", "low"])
#spectrum(stocks=[amd, aapl], labels=['high', 'high'])
#fourier(stocks=[aapl, amd], labels=["high", "low"])
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