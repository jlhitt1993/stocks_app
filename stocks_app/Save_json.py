import urllib.request
import json
import tkinter as tk
from tkinter import filedialog
import os


def save_json(name):
    request = urllib.request.Request('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + name
                                     + '&outputsize=full&interval=1min&apikey=BY1OVG40O9CEKQY4')
    response = urllib.request.urlopen(request)
    data = json.load(response)
    prices = data['Time Series (Daily)']
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    print(file_path)
    with open(os.path.join(file_path + os.path.join('/' + name + ".json")), "w") as write_file:
        json.dump(prices, write_file)
    root.destroy()

if __name__ == '__main__':
    save_json('aapl')
