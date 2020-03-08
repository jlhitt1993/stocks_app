# Demo to show all the possible graphs in OO_stocks

from OO_stocks import Stock, candlestick, correlation, percent_change, \
    fourier, spectrum, help

aapl = Stock('aapl')
amd = Stock('amd')
msft = Stock('msft')
# candlestick(amd)
correlation(aapl, 'high', amd, 'low')
percent_change(aapl, amd, labels=["high", "low"])
spectrum(amd, 'high', aapl, 'high')
fourier(aapl, amd, labels=["high", "low"])
# help()
