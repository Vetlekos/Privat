import numpy as np
import pandas as pd
from scipy.stats import norm
import pandas_datareader.data as web
import datetime

#calulate var for tomorrow
def value_at_risk_tmrw(position,c,mu,sigma):
    alpha = norm.ppf(1-c)
    var = position*(mu-sigma*alpha)
    return var

#if we want to calculate VaR for n days into the future
#we must consider that the mu and sigma will change so we use: mu = mu*n and sigma = sigma*sqrt(n)
def value_at_risk(S,c,mu,sigma,n):
    alpha = norm.ppf(1-c)
    var = S*(mu*n-sigma*alpha*np.sqrt(n))
    return var

if __name__ == "__main__":
    #start and ending date
    start_date = datetime.datetime(2014,1,1)
    end_date = datetime.datetime(2017,10,15)

    # download stock related data from Yahoo Finance
    citi = web.DataReader('C', data_source='yahoo', start=start_date, end=end_date)

    #use pct_change to calc daily returns
    citi["Returns"] = citi["Adj Close"].pct_change()

    #investment
    S = 1e6
    #confidence level
    c = 0.99

    #we assume normally distributed daily returns
    mu = np.mean(citi["Returns"])
    sigma = np.std(citi["Returns"])

    print("Value at risk is: $%0.2f" % value_at_risk_tmrw(S,c,mu,sigma))

