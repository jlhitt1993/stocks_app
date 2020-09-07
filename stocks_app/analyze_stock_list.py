from stock_objects import Stock
from stock_plots import correlation, percent_change, spectrum, fourier

with open("stock_list.txt", 'r') as read:
    stocks_list = read.read().split()
stocks_names, labels, stocks_objects = [], [], []
c = 0
for i in range(len(stocks_list)//2):
    stocks_names.append(stocks_list[c])
    labels.append(stocks_list[c+1])
    c += 2
print(stocks_list)
for i in stocks_names:
    stocks_objects.append(Stock(i))
print(labels)
correlation(stocks=stocks_objects, labels=labels)
percent_change(stocks=stocks_objects, labels=labels)
spectrum(stocks=stocks_objects, labels=labels)
fourier(stocks=stocks_objects, labels=labels)
