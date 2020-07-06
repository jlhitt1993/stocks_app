# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 14:47:00 2017

@author: Jeremy Hitt
"""

import urllib.request
import numpy as np
from scipy.fftpack import fft
import time
import json
#import pprint
import matplotlib.pyplot as pl
# import sys
url = "https://www.alphavantage.co/query"
api_key = 'BY1OVG40O9CEKQY4'
another = 'yes'
while (another == 'yes'):
    ticker = input('Enter the three ticker symbols in all caps separated by a space: ')
    tick_list = ticker.split()
    amount = len(tick_list)
    request = []
    response = []
    data = []
    prices = []
    c = 0
    for t in range(len(tick_list)):
        request.append(urllib.request.Request(url+'?function=TIME_SERIES_DAILY&symbol='+tick_list[t] +
            '&outputsize=full&interval=1min&apikey='+api_key))
        response.append(urllib.request.urlopen(request[t]))
        # print(json.load(response[c]))
        data.append(json.load(response[c]))
        # data is dictionary where 'Time Series (Daily)' is the keyword for all the data
        prices.append(data[c]['Time Series (Daily)'])
        # prices has form 'yyyy-mm-dd': {'1. open': 'value', '2. high': 'value', etc...}
        c += 1
        time.sleep(1.5)
        print('Got: ',tick_list[t],'('+str(c)+'/'+str(len(tick_list))+')')
    # pprint.pprint(data)
    # print(data)
    # print(data)
    # newest = data['Meta Data']['3. Last Refreshed']
    # print(newest[11:16])
    # dat= input("Enter the date and time you want.(2017-13-12 16:00:00) ")
    # pprint.pprint(prices[newest])
    # print('\n')
    value1 = input('Enter the quantity you want. (high,low,open,close,volume) ')
    while (value1 != 'high' or value1 != 'low' or value1 != 'open' or value1 != 'close' or value1 != 'volume'):
        if (value1 == 'high' or value1 == 'h'):
            value = '2. high'
            break
        elif (value1 == 'low' or value1 == 'l'):
            value = '3. low'
            break
        elif (value1 == 'open' or value1 == 'o'):
            value = '1. open'
            break
        elif (value1 == 'close' or value1 == 'c'):
            value = '4. close'
            break
        elif (value1 == 'volume' or value1 == 'v'):
            value = '5. volume'
            break
        else:
            print('Invalid input\n')
            value1 = input('Enter the quantity you want. (high,low,open,close,volume) ')
    # print(value)
    x = []
    # will be how many days ago the value is from
    y1 = []
    y2 = []
    y3 = []
    for t in range(len(tick_list)):
        count = 0
        x.append([])
        y1.append([])
        for d in prices[t]:
            y1[t].append(prices[t][d][value])   # t is tick, d is date. value is the keyword for the desired data
            count += 1
            x[t].append(count)   # count is number of days for each tick
    s =[]
    for t in range(len(tick_list)):
        s.append(len(x[t]))
    m = min(s)                   # find the smallest data set out of the collection
    x2 = []
    for t in range(len(tick_list)):
        y2.append([])
        x2.append([])
        count = 0
        for d in range(m):
            y2[t].append(float(y1[t][d]))  # y2 is to adjust the data sets so they all have the same length
            x2[t].append(float(x[t][d]))
            count += 1
        # print(y2[t])
        # x2 = (x[t][:m]) # adjust the number of days to match the minimum number from the data
        # y2[t].append(0)
    p = input('Which type of plot would you like? (correlation, spectrum, scaled, percent change, fourier transform): ')
    if ((p == 'percent change' or p == 'pc' or p == 'correlation' or p == 'c') and amount == 1):
        print('More than one stock is needed for that analysis')
        continue
    pl.figure(figsize=(12,12))
    cnt = 0 # used in correlation calculation
    a = []  # used in correlation calculation
    if (p == 'percent change' or p == 'pc'):  # calucaltes the change of stock value between each day
        diff = []
        vec = []
        for t in range(len(tick_list)):
            for g in range(len(y2[t])-1):
                vec.append((y2[t][g+1] - y2[t][g])/y2[t][g]) # calulate percent change each day
            diff.append(vec)
            vec = []
        for h in range(len(tick_list)):
            pl.subplot(amount, 1, h+1)
            pl.plot(x2[0][1:], diff[h], label='percent change '+tick_list[h])
            legnd = pl.legend(loc='upper right', prop={'size': 16})
            pl.title('percent change', fontsize=30)
            pl.ylabel('percent change', fontsize=26)
        pl.show()
        '''for t in range(len(tick_list)):
            #diff.append([])
            #pl.subplot(2,1,2)
            pl.plot(x2[t],y2[t], label=tick_list[t])
        legnd = pl.legend(loc='upper right',prop={'size' : 16})
        for handle in legnd.legendHandles:
            handle.set_linewidth(4.5)
        pl.xlabel('days',fontsize = 26)
        pl.title('price',fontsize=30)
        pl.ylabel(value,fontsize=26)
        #print(diff)
        pl.show()'''
    elif (p == 'correlation' or p == 'c'): # calculates the correlation value for each pair of /
            # stocks and plots the correlations
        for t in range(len(tick_list)-1):
            for e in range(t, len(tick_list)):
                if not(t == e):
                    a.append([])
                    a[cnt] = np.corrcoef(y2[t],y2[e])
                    b = "%.3f" % a[cnt][0][1]
                    cnt = cnt + 1
                    print('corrcoef ', tick_list[t], '-', tick_list[e], ': ', b)
                    pl.scatter(y2[t], y2[e], s=1, label=(tick_list[t]+'-' + tick_list[e]+' ' + str(b)))
        lgnd = pl.legend(loc='upper right', scatterpoints=1, prop={'size': 24}, fontsize=10)
        for handle in lgnd.legendHandles:
            handle.set_sizes([34])
        pl.title('Correlation scatter', fontsize=30)
        pl.xlabel('percent change', fontsize=26)
        pl.ylabel('percent change', fontsize=26)
        pl.show()
    elif (p == 'spectrum' or p == 'sp'):  # plots all the stock prices on one graph
        for t in range(len(tick_list)):
            pl.plot(x2[t], y2[t], label=tick_list[t])
        legnd = pl.legend(loc='upper right', prop={'size': 26})
        for handle in legnd.legendHandles:
            handle.set_linewidth(4.5)
        pl.xlabel('days', fontsize = 26)
        pl.title('spectrum', fontsize=30)
        pl.ylabel(value+' price ($)', fontsize=26)
        pl.show()
    elif (p == 'scaled' or p == 'sc'): # will plot the spectra normalized to the most recent stock price
        for t in range(len(tick_list)):
            y3.append([])
            first = float(y2[t][0])
            print(first)
            for i in range(len(y2[t])):
                y3[t].append(float(y2[t][i])/first)
        for t in range(len(tick_list)):
            pl.plot(x2[t], y3[t], label=tick_list[t])
        legnd = pl.legend(loc='upper right', prop={'size': 26})
        for handle in legnd.legendHandles:
            handle.set_linewidth(4.5)
        pl.xlabel('days', fontsize = 26)
        pl.title('Normalized plot', fontsize=30)
        pl.ylabel('Normalized '+value+' price ($)', fontsize=26)
        pl.show()
    elif (p == 'fourier' or p == 'fft'):
        yf = []
        if m % 2 == 0:       # even length
            half = len(y2[0])//2
            for t in range(len(tick_list)):
                yf.append(np.abs(fft(y2[t])[0:half]))
            for t in range(len(tick_list)):
                pl.plot(x2[t][0:half], yf[t], label=tick_list[t])
        if m % 2 == 1:             # odd length
            half = len(y2[0])//2
            for t in range(len(tick_list)):
                yf.append(np.abs(fft(y2[t])[0:half]))
            for t in range(len(tick_list)):
                pl.plot(x2[t][0:half], yf[t], label=tick_list[t])
        legnd = pl.legend(loc='upper right', prop={'size': 26})
        for handle in legnd.legendHandles:
            handle.set_linewidth(4.5)
        pl.xlabel('days', fontsize = 26)
        pl.title('Fourier transform', fontsize=30)
        pl.ylabel('FT', fontsize=26)
        pl.show()

    else:
        p = input('Which type of plot would you like? (correlation, spectrum, scaled, percent change, '
                  'fourier transform): ')
    print('\n')
    another = input('Look up another stock? (yes/no): ')
    print('\n')
