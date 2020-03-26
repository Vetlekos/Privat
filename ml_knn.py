import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LogisticRegression
import sklearn
import pandas_datareader.data as web
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

def create_dataset(stock_symbol, start_date, end_date, lags=7):

    #fetch the stock data from yahoo
    df = web.DataReader(stock_symbol,"yahoo",start_date,end_date)

    #create a new dataframe
    #we want to use additional features: lagged returns, yesterdays & todays returns
    tslag = pd.DataFrame(index=df.index)
    tslag["Today"] = df["Adj Close"]
    tslag["Volume"] = df["Volume"]

    #Create the shifted lag series of prior trading period close values
    for i in range(0,lags):
        tslag["Lag%s" % str(i+1)] = df["Adj Close"].shift(i+1)

    #create the returns DataFrame
    dfret = pd.DataFrame(index=tslag.index)
    dfret["Volume"] = tslag["Volume"]
    dfret["Today"] = tslag["Today"].pct_change()*100

    #create the lagged percentage returns columns
    for i in range (0,lags):
        dfret["Lag%s" % str(i+1)] = tslag["Lag%s" % str(i+1)].pct_change()*100

    #"Direction" column (-1 or +1 ) indicating down or up
    dfret["Direction"] = np.sign(dfret["Today"])

    #Remove NaNs
    dfret.drop(dfret.index[:7], inplace=True)

    return dfret

if __name__ == "__main__":

    #Create lagged series of s&p index
    data = create_dataset("AAPL", datetime(2012,1,1),datetime(2017,5,31), lags=7)

    #Use the prior two two days for prediction
    X = data[["Lag1", "Lag2", "Lag3", "Lag4","Lag5","Lag6"]]
    y = data["Direction"]

    #The test data is split into two parts, before and after 1. jan 2017
    start_test = datetime(2017,1,1)

    #Create training and test sets
    X_train = X[X.index < start_test]
    X_test = X[X.index >= start_test]
    y_train = y[y.index < start_test]
    y_test = y[y.index >= start_test]

    #we use KNeighborsClassifier as the machine learning model
    model = KNeighborsClassifier(300)

    #train the model on the training set
    model.fit(X_train,y_train)

    #make an rray of prediction on the test set
    pred = model.predict(X_test)

    #output hit rate and confusion matrix
    print("Accuracy of the kNN model: %0.3f" % model.score(X_test,y_test))
    print("Confusion matrix: \n%s" % confusion_matrix(pred,y_test))
