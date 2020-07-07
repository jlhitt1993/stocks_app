# Demo to show all the possible graphs in OO_stocks

from OO_stocks import Stock, candlestick, correlation, percent_change, \
    fourier, spectrum, help

AAPL = Stock('aapl')
AMD = Stock('amd')
MSFT = Stock('msft')
candlestick(AMD)
correlation(stocks=[AAPL, AMD, MSFT], labels=['high', 'low', 'open'])
percent_change(stocks=[AAPL, AMD, MSFT], labels=['high', 'low', 'open'])
spectrum(stocks=[AAPL, AMD, MSFT], labels=['high', 'low', 'open'])
fourier(stocks=[AAPL, AMD, MSFT], labels=['high', 'low', 'open'])
# help()
