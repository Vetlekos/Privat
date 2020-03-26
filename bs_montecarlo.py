import numpy as np
import math
import time

class OptionPricing:

    def __init__(self, S,E,T,rf,sigma,iterations):
        self.S = S
        self.E = E
        self.T = T
        self.rf = rf
        self.sigma = sigma
        self.iterations = iterations

    def call_option_simulation(self):

        #we have 2 colums, one with zeros and one for payoffs
        #we need the first column of 0s, payoff function is max(0, S-E) for call
        option_data = np.zeros([self.iterations,2])

        #dimensions: 1 dimensional array with as many items as the iterations
        rand = np.random.normal(0,1,[1,self.iterations])

        #equation for stock price S(t)
        stock_price = self.S*np.exp(self.T*(self.rf - 0.5*self.sigma**2)+self.sigma*np.sqrt(self.T)*rand)

        #we need S-E to calculate max(S-E,0)
        option_data[:,1] = stock_price - self.E

        #average for the monte carlo method
        average = np.sum(np.amax(option_data,axis=1))/float(self.iterations)

        #discount using exp(-rT)
        return np.exp(-1*self.rf*self.T)*average

    def put_option_simulation(self):
        # we have 2 colums, one with zeros and one for payoffs
        # we need the first column of 0s, payoff function is max(0, E-S) for put
        option_data = np.zeros([self.iterations, 2])

        # dimensions: 1 dimensional array with as many items as the iterations
        rand = np.random.normal(0, 1, [1, self.iterations])

        # equation for stock price S(t)
        stock_price = self.S * np.exp(self.T * (self.rf - 0.5 * self.sigma ** 2) + self.sigma * np.sqrt(self.T) * rand)

        # we need S-E to calculate max(S-E,0)
        option_data[:, 1] = self.E - stock_price

        # average for the monte carlo method
        average = np.sum(np.amax(option_data, axis=1)) / float(self.iterations)

        # discount using exp(-rT)
        return np.exp(-1 * self.rf * self.T) * average

if __name__ == "__main__":
    S = 100
    E = 100
    T = 1
    rf = 0.05
    sigma = 0.2
    iterations = 10000000

    model = OptionPricing(S,E,T,rf,sigma,iterations)
    print("Call option value: ", model.call_option_simulation())
    print("Put option value: ", model.put_option_simulation())
