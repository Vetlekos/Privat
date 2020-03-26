import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import fix_yahoo_finance as yf
stock = ['AAPL']
yf.pdr_override(stock)
start = pd.to_datetime('2013-12-12')
end = pd.to_datetime('2018-03-29')
data = pdr.get_data_yahoo(stock, start=start, end=end)['Adj Close']
daily_returns = (data/data.shift(1))-1
daily_returns.hist(bins=100)
plt.show()

from math import exp
##Define functions for FV, PV and cont FV and cont PV
def discrete_future_value(x,r,n):
    return x*(1+r)**n

def discrete_present_value(x,r,n):
    return x*(1+r)**-n

def cont_future_value(x,r,t):
    return x*exp(r*t)

def cont_present_value(x,r,t):
    return x*exp(-r*t)

x=100
r=0.05
n=5

print(discrete_future_value(x, r, n))
print(cont_future_value(x, r, n))