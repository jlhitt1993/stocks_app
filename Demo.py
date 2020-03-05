# Demo to show all the possible graphs in OO_stocks

from OO_stocks import Stock, candlestick, correlation, percent_change, \
    fourier, spectrum, help

aapl = Stock('aapl')
amd = Stock('amd')
msft = Stock('msft')
#candlestick(amd)
correlation(aapl, 'high', amd, 'low')
percent_change(aapl.high, amd.low, labels=["aapl.high", "amd.low"])
spectrum(amd, 'high')
fourier(aapl, amd)
help()
