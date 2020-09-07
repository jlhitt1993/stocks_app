# Script to download the stocks listed in stock_list.txt and save the data to local files

from Save_json import save_json

with open("stock_list.txt", 'r') as read:
    stocks_list = read.read().split('\n')
print(stocks_list)
save_json(stocks_list)
print('Stocks were saved to directory')
