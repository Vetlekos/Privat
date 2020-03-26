import pandas_datareader as pdr
from pandas_datareader import data, wb
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

risk_free_rate = 0.05


def capm(start_date, end_date, ticker1, ticker2):
    # get data from yahoo finance
    stock1 = pdr.get_data_yahoo(ticker1, start_date, end_date)
    stock2 = pdr.get_data_yahoo(ticker2, start_date, end_date)

    # transform daily returns to monthly
    return_stock1 = stock1.resample("M").last()
    return_stock2 = stock2.resample("M").last()

    # creating a dataframe from data using adj close
    data = pd.DataFrame({"s_adjclose": return_stock1["Adj Close"], "m_adjclose": return_stock2["Adj Close"]},
                        index=return_stock1.index)
    # ln returns
    data[['s_returns', 'm_returns']] = np.log(
        data[['s_adjclose', 'm_adjclose']] / data[['s_adjclose', 'm_adjclose']].shift(1))
    # drop missing data
    data = data.dropna()

    # Covariance matrix
    covmat = np.cov(data["s_returns"], data["m_returns"])
    print(covmat)

    # Calculate beta
    beta = covmat[0, 1] / covmat[1, 1]
    print("Beta: ", beta)

    # using linear regression to fit line to stock and market returns
    beta, alpha = np.polyfit(data["m_returns"], data["s_returns"], deg=1)
    print("Beta from regresiion: ", beta)

    # plot
    fig, axis = plt.subplots(1, figsize=(20, 10))
    axis.scatter(data["m_returns"], data['s_returns'], label="Data points")
    axis.plot(data["m_returns"], beta * data["m_returns"] + alpha, color='red', label="CAPM Line")
    plt.title('Capital Asset Pricing Model, finding alphas and betas')
    plt.xlabel('Market return $R_m$', fontsize=18)
    plt.ylabel('Stock return $R_a$')
    plt.text(0.08, 0.05, r'$R_a = \beta * R_m + \alpha$', fontsize=18)
    plt.legend()
    plt.grid(True)
    plt.show()

    # calculate capm expected return
    expected_return = risk_free_rate + beta * (data["m_returns"].mean() * 12 - risk_free_rate)
    print("Expected return: ", expected_return)


capm("2010-01-01", "2019-12-12", "IBM", "^GSPC")

