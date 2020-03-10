# Demo to show all the possible graphs in OO_stocks

from OO_stocks import Stock, candlestick, correlation, percent_change, \
    fourier, spectrum, help

aapl = Stock('aapl', local='')
amd = Stock('amd', local='')
msft = Stock('msft', local='')
#candlestick(amd)
correlation(stocks=[aapl, amd, msft], labels=['high', 'low', 'open'])
percent_change(stocks=[aapl, amd, msft], labels=['high', 'low', 'open'])
spectrum(stocks=[aapl, amd, msft], labels=['high', 'low', 'open'])
fourier(stocks=[aapl, amd, msft], labels=['high', 'low', 'open'])
# help()
