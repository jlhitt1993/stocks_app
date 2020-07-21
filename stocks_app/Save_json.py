# Downloads data for one or more stocks and saves it locally

import urllib.request
import json
import tkinter as tk
from tkinter import filedialog
import os
from time import sleep


def save_json(args):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    i = 1
    for arg in args:
        request = urllib.request.Request('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + arg
                                         + '&outputsize=full&interval=1min&apikey=BY1OVG40O9CEKQY4')
        response = urllib.request.urlopen(request)
        data = json.load(response)
        # prices = data['Time Series (Daily)']
        with open(os.path.join(file_path + os.path.join('/' + arg + ".json")), "w") as write_file:
            json.dump(data, write_file)
        print("Saved " + arg + " (" + str(i) + "/" + str(len(args)) + ")")
        i += 1
        sleep(0.1)
    root.destroy()

if __name__ == '__main__':
    save_json(['aapl'])
