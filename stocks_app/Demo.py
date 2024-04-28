# Demo to show all the graphs possible in stocks_app

from stock_objects import Stock
from stock_plots import correlation, percent_change, fourier, spectrum, candlestick
import matplotlib.pyplot as plt

print("Welcome to stocks_app! This is a short demo that will show you some of the things that are possible with "
      "stocks_app.")
AAPL = Stock('aapl', timescale='daily', local=True, file='Json')
AMD = Stock('amd', timescale='daily', local=True, file='Json')
MSFT = Stock('msft', timescale='daily', local=True, file='Json')
#LMT = Stock('lmt', local=True, file='Json')
#candlestick(AMD)
correlation(stocks=[AAPL, AMD, MSFT], labels=['high', 'low', 'open'])
percent_change(stocks=[AAPL, AMD, MSFT], labels=['high', 'low', 'open'])
spectrum(stocks=[AAPL, AMD, MSFT], labels=['high', 'low', 'open'])
fourier(stocks=[AAPL, AMD, MSFT], labels=['high', 'low', 'open'])
# help()
plt.show()
