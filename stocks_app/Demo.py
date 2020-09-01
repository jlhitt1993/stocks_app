# Demo to show all the graphs possible in stocks_app

from stock_objects import Stock
from stock_plots import correlation, percent_change, fourier, spectrum, candlestick

AAPL = Stock('aapl', local=True, file='Json')
AMD = Stock('amd', local=True, file='Json')
MSFT = Stock('msft', local=True, file='Json')
LMT = Stock('lmt', local=True, file='Json')
#candlestick(AMD)
#correlation(stocks=[AAPL, AMD, MSFT, LMT], labels=['high', 'low', 'open', 'open'])
#percent_change(stocks=[AAPL, AMD, MSFT, LMT], labels=['high', 'low', 'open', 'open'])
#spectrum(stocks=[AAPL, AMD, MSFT, LMT], labels=['high', 'low', 'open', 'open'])
fourier(stocks=[AAPL, AMD, MSFT, LMT], labels=['high', 'low', 'open', 'open'])
# help()
