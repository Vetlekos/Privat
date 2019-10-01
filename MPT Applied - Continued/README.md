# MPT Applied - Continued 

MPT Applied is a Python application for optimizing portfolios using Modern Portfolio Theory (MPT) developed by Harry Markowitz.
The application is based on Quandl for providing pricing info and is currently set to US Equity markets but can be modified to fit other markets, indexes and financial instruments. This also assumes a 0% risk free rate.
This is not financial advice and is just for development purposes.

#THIS IS A CONT OF MY FINAL PROJECT FOR CS50X 

## Usage

```bash
    python MPT.py <filename.txt>
```
This will start the application. A .txt-file can optionally be provided as argument. The text must include stock tickers seperated by a newline. If no textfile is provided the user will be prompted to manually type stock tickers.

The user will then be prompted to give start and end date for analysis. If no end date is provided, todays date will be used. The user is then prompted for how many imaginary portfolios to plot. The more portfolios the more accurate the analysis but it also increases computing time

The application will plot and create a .svg file containing a chart displaying the efficient frontier, as well as the minimum variance portfolio and maximum sharpe ratio portfolio. Information for the two portfolios will also be printed and written to a textfile.

Example of what will be printed and written to textfile:

```
2019-08-08-21:10:23
Analysis on 3 stocks from 2017-1-1 to 2019-08-08
Minimum Variance Portfolio:
                  4671
Returns       0.002802
Volatility    0.163385
Sharpe Ratio  0.017148
TSLA Weight   0.459510
AMZN Weight   0.448920
GE Weight     0.091570

Maximum Sharpe Ratio Portfolio:
                  9018
Returns       0.575329
Volatility    0.225108
Sharpe Ratio  2.555797
TSLA Weight   0.979621
AMZN Weight   0.001459
GE Weight     0.018920
```

## Author
This application was developed as part of my final project for CS50x.
The project was further developed during fall 2019 after completion of CS50.
I want to thank Professor David Malan and the rest of the CS50 team for all their effort and contribution.

👤 **Vetle Skeime Kostøl**
* Email: vetle@skeime.no
* Github: [@Vetlekos](https://github.com/Vetlekos)
