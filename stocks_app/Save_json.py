import urllib.request
import json

name = 'aapl'
request = urllib.request.Request('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + name
                                 + '&outputsize=full&interval=1min&apikey=BY1OVG40O9CEKQY4')
response = urllib.request.urlopen(request)
data = json.load(response)
prices = data['Time Series (Daily)']
with open(name + ".json", "w") as write_file:
    json.dump(data, write_file)
