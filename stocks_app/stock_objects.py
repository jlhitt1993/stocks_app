# Define Stock object that is used to represent stocks

from _datetime import datetime as dt
from json import dump, load
import urllib.request
from time import sleep
import tkinter as tk
from tkinter import filedialog
import numpy as np
from pandas import read_csv


url = "https://www.alphavantage.co/query"
api_key = 'BY1OVG40O9CEKQY4'


class Name:
    def __init__(self, name):
        self.name = name


class Stock(Name):
    def __init__(self, name, timescale='daily', year_month='year1month1', interval='5min', **kwargs):
        Name.__init__(self, name)
        if str(timescale) == 'daily':
            function = 'TIME_SERIES_DAILY'
        elif str(timescale) == 'intraday':
            function = 'TIME_SERIES_INTRADAY_EXTENDED'
        else:
            print("value for timescale is not not supported. Supported values are daily and intraday")
        if 'file' in kwargs.keys():
            try:
                file_path = kwargs['file']
                data = load(open(file_path + '/' + name + '.json'))
            except:
                print("There was a problem loading the data from the file. Make sure the argument file= in Stock() is "
                      "correct and that the file exists")
                exit(-1)
        elif 'local' in kwargs.keys():
            try:
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askdirectory()
                data = load(open(file_path + '/' + name + '.json'))
            except:
                print("Failed to load the file specified. Please try again.")
                exit(-1)
        else:
            if timescale == 'intraday':
                request = urllib.request.Request(url + '?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=' + name +
                                             '&interval=' + interval + '&slice=' + year_month + '&apikey=' + api_key)
                response = urllib.request.urlopen(request)
                intraday = read_csv(response)
            elif timescale == 'daily':
                request = urllib.request.Request(url + '?function=' + function + '&symbol=' + name +
                                             '&outputsize=full&interval=1min&apikey=' + api_key)
                response = urllib.request.urlopen(request)
                data = load(response)
            else:
                print("The timescale entered is not supported. Please enter either daily or intraday.")
                exit(0)
        if function == 'TIME_SERIES_DAILY':
            daily = data['Time Series (Daily)']
            #print(daily)
            self.dates = []
            self.high = np.empty(len(daily))
            self.low = np.empty(len(daily))
            self.open = np.empty(len(daily))
            self.close = np.empty(len(daily))
            self.volume = np.empty(len(daily))
            i = 0
            for d in daily:
                self.high[i] = float(daily[d]['2. high'])   #d is date. value is the keyword for the desired data
                self.low[i] = float(daily[d]['3. low'])
                self.open[i] = float(daily[d]['1. open'])
                self.close[i] = float(daily[d]['4. close'])
                self.volume[i] = float(daily[d]['5. volume'])
                self.dates.append(dt.strptime(d, '%Y-%m-%d'))
                i += 1
            self.days = np.linspace(0, len(self.dates), num=len(self.dates))
        elif function == 'TIME_SERIES_INTRADAY_EXTENDED':
            #print(intraday)
            self.dates = intraday['time']
            self.high = intraday['high']
            self.low = intraday['low']
            self.open = intraday['open']
            self.close = intraday['close']
            self.volume = intraday['volume']
        print('Got: ' + name + '')
        if ('local' not in kwargs.keys()) or ('file' not in kwargs.keys()):
            sleep(0.2)


if __name__ == '__main__':
    aapl = Stock('aapl', timescale='intraday')
#    print(aapl.name)
#    amd = Stock('amd')
#    msft = Stock('msft')
