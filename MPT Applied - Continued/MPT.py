# import needed modules
import quandl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cs50
from datetime import datetime
import sys

# get adjusted closing prices of selected companies with Quandl
quandl.ApiConfig.api_key = 'E9ihtBbFesQ7_2po-Vss'

# Create empty list for selected stocks
selected = []

#check if stocks.txt exists and if it does: take its lines as selected stocks and skip manual inputs
if len(sys.argv) > 1:
    selected = [line.rstrip('\n') for line in open(sys.argv[1])]
else:
    #Get number of stocks to put in portfolio and to promt user for x amount of tickers. Also validate that x>=2
    while True:
    	try:
    		n_stocks = cs50.get_int("Input number of stocks: ")
    		assert(n_stocks > 1)
    		break
    	except:
    		print("Number of stocks must be greater than or equal to 2")

    while n_stocks > len(selected):
        stock = input("Enter stock ticker: ")
        selected.append(stock)

#promt for time interval. If no end date, todays date is used
date_start = cs50.get_string("Input starting date (YYYY-MM-DD): ")
date_end = cs50.get_string("Input ending date (YYYY-MM-DD): ")
if not date_end or date_end > datetime.today().strftime('%Y-%m-%d'):
    date_end = datetime.today().strftime('%Y-%m-%d')

data = quandl.get_table('WIKI/PRICES', ticker = selected,
                        qopts = { 'columns': ['date', 'ticker', 'adj_close'] },
                        date = { 'gte': date_start, 'lte': date_end }, paginate=True)

# reorganise data pulled by setting date as index with columns of tickers and their corresponding adjusted prices
clean = data.set_index('date')
table = clean.pivot(columns='ticker')

# calculate daily and annual returns of the stocks
returns_daily = table.pct_change()
returns_annual = returns_daily.mean() * 250

# get daily and covariance of returns of the stock
cov_daily = returns_daily.cov()
cov_annual = cov_daily * 250

# empty lists to store returns, volatility and weights of imiginary portfolios
port_returns = []
port_volatility = []
sharpe_ratio = []
stock_weights = []

# set the number of combinations for imaginary portfolios and check if over 0
num_assets = len(selected)

while True:
	try:
		num_portfolios = cs50.get_int("Input number of combinations: ")
		assert(num_portfolios > 0)
		break
	except:
		print("Number of portfolios must be greater than 0")

#set random seed for reproduction's sake
np.random.seed(101)

# populate the empty lists with each portfolios returns,risk and weights
for single_portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = np.dot(weights, returns_annual)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
    sharpe = returns / volatility
    sharpe_ratio.append(sharpe)
    port_returns.append(returns)
    port_volatility.append(volatility)
    stock_weights.append(weights)

# a dictionary for Returns and Risk values of each portfolio
portfolio = {'Returns': port_returns,
             'Volatility': port_volatility,
             'Sharpe Ratio': sharpe_ratio}

# extend original dictionary to accomodate each ticker and weight in the portfolio
for counter,symbol in enumerate(selected):
    portfolio[symbol+' Weight'] = [Weight[counter] for Weight in stock_weights]

# make a nice dataframe of the extended dictionary
df = pd.DataFrame(portfolio)

# get better labels for desired arrangement of columns
column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' Weight' for stock in selected]

# reorder dataframe columns
df = df[column_order]

# find min Volatility & max sharpe values in the dataframe (df)
min_volatility = df['Volatility'].min()
max_sharpe = df['Sharpe Ratio'].max()

# use the min, max values to locate and create the two special portfolios
sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
min_variance_port = df.loc[df['Volatility'] == min_volatility]

# plot frontier, max sharpe & min Volatility values with a scatterplot
plt.style.use('seaborn-dark')
df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', marker='D', s=200)
plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='blue', marker='D', s=200 )
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
plt.savefig("Efficient_Frontier.svg")

#Print portfolios + date in terminal
print("")
print(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
print("Analysis on %s stocks from %s to %s" % (len(selected), date_start, date_end))
print("Minimum Variance Portfolio:")
print(min_variance_port.T)
print("")
print("Maximum Sharpe Ratio Portfolio:")
print(sharpe_portfolio.T)

#Write portfolios + date to file
sys.stdout=open("Portfolio_Analysis.txt","w")
print(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
print("Analysis on %s stocks from %s to %s" % (len(selected), date_start, date_end))
print("Minimum Variance Portfolio:")
print(min_variance_port.T)
print("")
print("Maximum Sharpe Ratio Portfolio:")
print(sharpe_portfolio.T)
sys.stdout.close()

