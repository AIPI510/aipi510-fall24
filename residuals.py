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

def calculate_leverage(X_test):
    """
    Calculate the leverage (hat matrix diagonal) for each observation.
    
    Parameters:
    X (array-like): The design matrix of the regression model.
    
    Returns:
    numpy.ndarray: Leverage values for each observation.
    """
    X = np.array(X_test)
    hat_matrix = X.dot(np.linalg.inv(X.T.dot(X))).dot(X.T)
    return np.diagonal(hat_matrix)

def cooks_distance(residuals, leverage, n_params = 1):
    """
    Calculate Cook's distance for each observation.
    
    Parameters:
    residuals (array-like): The residuals from the regression model.
    leverage (array-like): The leverage (hat matrix diagonal) for each observation.
    n_params (int): The number of parameters in the model (including intercept).
    
    Returns:
    numpy.ndarray: Cook's distance for each observation.
    """
    # Convert inputs to numpy arrays if they aren't already
    residuals = np.array(residuals)
    leverage = np.array(leverage)
    
    # Number of observations
    n_obs = len(residuals)
    
    # Calculate MSE
    mse = np.sum(residuals**2) / (n_obs - n_params)
    
    # Calculate Cook's distance
    cook_numerator = (residuals / (1 - leverage))**2
    cook_denominator = n_params * mse
    cooks_d = cook_numerator / cook_denominator
    
    return cooks_d

def visualize_cooks_distance(cooks_distances, threshold=None):
    """
    Visualize Cook's distance for each observation.
    
    Parameters:
    cooks_distances (array-like): Array of Cook's distances for each observation.
    threshold (float, optional): Threshold for influential points. If None, uses 4/n.
    
    Returns:
    None (displays the plot)
    """
    n = len(cooks_distances)
    
    # Set up the plot
    plt.figure(figsize=(12, 6))
    plt.bar(range(n), cooks_distances)
    plt.xlabel('Observation')
    plt.ylabel("Cook's Distance")
    plt.title("Cook's Distance for Influential Observations")
    
    # Add threshold line
    if threshold is None:
        threshold = 4 / n
    plt.axhline(y=threshold, color='r', linestyle='--', label=f'Threshold ({threshold:.4f})')
    
    # Highlight influential points
    influential = cooks_distances > threshold
    plt.scatter(range(n), cooks_distances, c=['r' if i else 'b' for i in influential], zorder=3)
    
    # Add labels for influential points
    for i, (d, inf) in enumerate(zip(cooks_distances, influential)):
        if inf:
            plt.annotate(f'{i}', (i, d), xytext=(0, 5), textcoords='offset points', ha='center')
    
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    # Print summary
    print(f"Number of influential observations: {sum(influential)}")
    print(f"Indices of influential observations: {np.where(influential)[0]}")


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
    leverage = calculate_leverage(X_test)
    cooks_distances = cooks_distance(residuals, leverage)
    visualize_cooks_distance(cooks_distances)
    Breusch_Pagan(residuals, X_test)
    Durbin_Watson(residuals)

if __name__ == "__main__":
    main()

