import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LogisticRegression
import sklearn
import pandas_datareader.data as web
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix


def create_dataset(stock_symbol, start_date, end_date, lags=5):
    # Fetch stock data from yahoo finance
    df = web.DataReader(stock_symbol, "yahoo", start_date, end_date)

    # create a new dataframe
    # we want to use additional features: lagged returns...today's returns, yesterday's returns etc
    tslag = pd.DataFrame(index=df.index)
    tslag["Today"] = df["Adj Close"]
    tslag["Volume"] = df["Volume"]

    # Create the shifted lag series of prior trading period close values
    for i in range(0, lags):
        tslag["Lag%s" % str(i + 1)] = df["Adj Close"].shift(i + 1)

    # Create the returns dataframe
    dfret = pd.DataFrame(index=tslag.index)
    dfret["Volume"] = tslag["Volume"]
    dfret["Today"] = tslag["Today"].pct_change() * 100

    # create the lagged percentage returns columns
    for i in range(0, lags):
        dfret["Lag%s" % str(i + 1)] = tslag["Lag%s" % str(i + 1)].pct_change() * 100.0

    # "Direction" column (+1 or -1) indicating an up/down day
    dfret["Direction"] = np.sign(dfret["Today"])

    # remove NaNs
    dfret.drop(dfret.index[:5], inplace=True)

    return dfret


if __name__ == "__main__":
    # Create a lagged series of S&P index
    data = create_dataset("AAPL", datetime(2012, 1, 1), datetime(2017, 5, 31), lags=5)

    # use prior two days of returns as predictor
    X = data[["Lag1", "Lag2", "Lag3", "Lag4"]]
    y = data["Direction"]

    # split test data
    start_test = datetime(2017, 1, 1)

    # Create training and test sets
    X_train = X[X.index < start_test]
    X_test = X[X.index >= start_test]
    y_train = y[y.index < start_test]
    y_test = y[y.index >= start_test]

    # we use SVM as machine learning model
    model = SVC(C=1000000,cache_size=200,class_weight=None,coef0=0.0,degree=3,gamma=0.001,kernel="rbf",max_iter=-1,probability=False,random_state=None,shrinking=True,tol=0.001,verbose=False)

    # train the model on the training set
    model.fit(X_train, y_train)

    # make an array of predictions on the test set
    pred = model.predict(X_test)

    # output hit rate and confusion matrix
    print("Accuracy of SVM model: %0.3f" % model.score(X_test, y_test))
    print("Confusion matrix: \n%s" % confusion_matrix(pred, y_test))
