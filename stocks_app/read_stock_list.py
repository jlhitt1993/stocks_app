from Save_json import save_json

with open("stock_list.txt", 'r') as read:
    stocks_list = read.read().split('\n')
print(stocks_list)
stock_objects = []
i = 0
save_json(stocks_list)
print('Stocks were saved to directory')
