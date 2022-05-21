# Stocks App

This script can easily fetch data about the stock market and create
unique graphs from the data. <br> It is intended to be used for an analysis
tool for trading. All the stock data fetched online comes <br> from 
https://www.alphavantage.co/query and is subject to their restrictions.
<br><br> Author: Jeremy Hitt (jlhitt1993@gmail.com)

### Getting started

Install stocks_app package from a repository such as https://github.com/jlhitt1993/stocks_app,
PyPI, or Anaconda Cloud.

To see examples, run `Demo.py`.

Using `help()` can also help with getting started and troubleshooting.

### Basic usage
_______________

#### Loading data

- To get data about AAPL, type `AAPL = Stock('aapl')`. This will create
a stock object called `AAPL`.
- Stock objects have eight attributes: name, high, low, open, close,
    dates, days, volume.
    - `name` is a string of the stock's ticker symbol.
    - `high`, `low`, `open`, `close`, `volume` are lists with the 
    corresponding data in a daily interval.
    - `days` is a list on integers spanning the number of days 
    since that stocks first listing.
    - `dates` is a list of the dates corresponding to the stock's data.
    It is represented in the format YYYY-MM-DD.
    
#### Making graphs

All graphs can be plotted with more than one stock at a time and
the correlation graph requires at least two stocks. <br> The arguements 
for each function must be passed as keywords as shown below.
- `specturm(stocks=[AAPL], labels=['high'])` will make a plot of AAPL's high
every day since the stock has been listed.
- `correlation(stocks=[AAPL, MSFT], labels=['high', 'low']`
- `percent_change(stocks=[AAPL], labels=['high'])`
- `candlestick(AAPL)`
- `fourier(stocks=[AAPL], labels=['high'])`

### Advanced usage

It's possible to analyze market data stored on local files.
- To load data from local files, it must be stored in the same json 
format as is used by www.alphavantage.com. <br> An example json is also 
included in this package directory.
    - To load a local file, set the keyword argument `local` to True as shown 
`AAPL = Stocks('aapl', local=True)`

### Analyzing a large set of stocks

A list of stocks can be provided in stock_list.txt to be downloaded and analyzed later.
- Fill in the list in stock_list.txt and save the file. 
- Run read_stock_list.py and choose the directory to save the json files.
- Use the `local` argument in `Stock()` to import the json data from the local files.
