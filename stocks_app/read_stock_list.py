from Save_json import save_json

with open("stock_list.txt", 'r') as read:
    stocks_list = read.read().split('\n')
print(stocks_list)
stock_objects = []
i = 0
for stock in stocks_list:
    save_json(stock)
    i += 1
print('Stocks were saved to directory')
