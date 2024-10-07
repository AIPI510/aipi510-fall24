#Portions of this code were generated using perplexity.ai
#Some portions were borrowed from other assignments in courses AIPI 520 and AIPI 590
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.stats.diagnostic import het_breuschpagan
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
import numpy as np


def preprocess():
    # Load the data
    copperdata = pd.read_csv('copper-new.txt',header=None)
    copperdata['X'] = copperdata.apply(lambda x: x.str.split()[0][1],axis=1)
    copperdata['y'] = copperdata.apply(lambda x: x.str.split()[0][0],axis=1)
    copperdata = copperdata[['X','y']].astype(float)
    print(copperdata.head())

    X = copperdata['X'].values
    y = copperdata['y'].values

    X = X.reshape(-1,1)

    X_train,X_test,y_train,y_test = train_test_split(X, y, random_state=0,test_size=0.2)

    print(y_test)

    return X_train,X_test,y_train,y_test

def linReg(X_train,X_test,y_train,y_test):
    regression = LinearRegression().fit(X_train, y_train)
    y_pred = regression.predict(X_test)
    residuals = y_pred - y_test
    return residuals, y_pred

def residual_plot(residuals, y_pred):
    plt.scatter(y_pred, residuals)
    plt.xlabel('y_pred')
    plt.ylabel('Residuals')
    plt.title('Residuals vs y_pred Values')
    plt.legend()
    plt.show()


def Breusch_Pagan(residuals, X_test):
    #test for homodescacity
    X_test_scaled_bpt = sm.add_constant(X_test)  # Add a constant term to the features

    # Perform Breusch-Pagan test

    _, p_value, _, _ = het_breuschpagan(residuals, X_test_scaled_bpt)
    print(f'Breusch-Pagan test Linear Regression p-value: {p_value}')


    print("\nSince p Value is above 0.05 (Common norm for Breusch-Pagan tes), we can say that the data displays heterodescacity")

def Durbin_Watson(residuals):
    dw_statistic = durbin_watson(residuals)
    print(f"\nDurbin-Watson statistic linear regression: {dw_statistic}")
    print("Since the value is  below 2, it indicates a strong positive autocorrelation")


def main():
    X_train,X_test,y_train,y_test = preprocess()
    residuals, y_pred = linReg(X_train,X_test,y_train,y_test)
    residual_plot(residuals, y_pred)
    Breusch_Pagan(residuals, X_test)
    Durbin_Watson(residuals)

if __name__ == "__main__":
    main()

