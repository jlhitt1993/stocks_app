# Define Stock object that is used to represent stocks

from _datetime import datetime as dt
from json import dump, load
import urllib.request
from time import sleep
import tkinter as tk
from tkinter import filedialog


url = "https://www.alphavantage.co/query"
api_key = 'BY1OVG40O9CEKQY4'


class Name:
    def __init__(self, name):
        self.name = name


class Stock(Name):
    def __init__(self, name, **kwargs):
        Name.__init__(self, name)
        if 'local' in kwargs.keys():
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askdirectory()
            data = load(open(file_path + '/' + name + '.json'))
        else:
            request = urllib.request.Request(url + '?function=TIME_SERIES_DAILY&symbol=' + name +
                                             '&outputsize=full&interval=1min&apikey=' + api_key)
            response = urllib.request.urlopen(request)
            data = load(response)
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
        sleep(0.4)


if __name__ == '__main__':
    aapl = Stock('aapl')
    print(aapl.name)
#    amd = Stock('amd')
#    msft = Stock('msft')
