import numpy as np
import pandas as pd
from scipy.stats import norm
import pandas_datareader.data as web
import datetime
import math

class ValueAtRiskMonteCarlo:

    def __init__(self, S, mu, sigma, c, n, iterations):
        self.S = S
        self.mu = mu
        self.sigma = sigma
        self.c = c
        self.n = n
        self.iterations = iterations

    def simulation(self):

        stock_data = np.zeros([self.iterations, 1])
        rand = np.random.normal(0,1,[1,self.iterations])

        #equation for the stock price S(t)
        stock_price = self.S*np.exp(self.n*(self.mu - 0.5*self.sigma**2)+self.sigma*np.sqrt(self.n)*rand)

        #sort stock prices to determine percentile
        stock_price = np.sort(stock_price)

        percentile = np.percentile(stock_price,(1-self.c)*100)

        return self.S-percentile

if __name__ == "__main__":

    S = 1000000
    c = 0.99
    n = 1
    iterations = 100000

    #historical data
    start_date = datetime.datetime(2014,1,1)
    end_date = datetime.datetime(2017,10,15)

    citi = web.DataReader('C', data_source='yahoo', start=start_date, end=end_date)

    citi["Returns"] = citi["Adj Close"].pct_change()

    #assume normal distribution
    mu = np.mean(citi["Returns"])
    sigma = np.std(citi["Returns"])

    model = ValueAtRiskMonteCarlo(S,mu,sigma,c,n,iterations)

    print("Value at risk with monte-carlo simulation: $%0.2f" % model.simulation())