import numpy as np
import pandas as pd
from scipy import log,exp,sqrt,stats

def blackscholes_call(S,E,T,rf,sigma):
    #calculate d1 and d2
    d1 = (np.lib.scimath.log(S/E)+(rf + sigma*sigma/2)*T)/(sigma*np.lib.scimath.sqrt(T))
    d2 = d1 - sigma*np.lib.scimath.sqrt(T)

    #N(X) normal distribution function
    return S*stats.norm.cdf(d1)-E*np.exp(-rf*T)*stats.norm.cdf(d2)

def blackscholes_put(S,E,T,rf,sigma):
    #calculate d1 and d2
    d1 = (np.lib.scimath.log(S/E)+(rf + sigma*sigma/2)*T)/(sigma*np.lib.scimath.sqrt(T))
    d2 = d1 - sigma*np.lib.scimath.sqrt(T)

    #return n(x) put option value
    return -S*stats.norm.cdf(-d1)+E*np.exp(-rf*T)*stats.norm.cdf(-d2)

if __name__ == "__main__":
    E = 100
    S = 100
    T = 1
    rf = 0.05
    sigma = 0.2

    print("Call option value: ", blackscholes_call(S,E,T,rf,sigma))
    print("Put option value:", blackscholes_put(S,E,T,rf,sigma))
