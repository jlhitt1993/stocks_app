from OO_stocks import Stock

with open("stock_list.txt") as read:
    stocks_list = read.read().split('\n')
print(stocks_list)
stock_objects = []
i = 0
for stock in stocks_list:
    stock_objects.append(Stock(stock))
    i += 1
