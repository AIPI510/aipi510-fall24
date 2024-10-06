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


regression = LinearRegression().fit(X_train, y_train)
y_pred = regression.predict(X_test)

residuals = y_pred - y_test

residuals_list = list(residuals)

# Remove ellipsis if present
residuals_cleaned = [x for x in residuals_list if x is not Ellipsis]

# Convert to numpy array
residuals_array = np.array(residuals_cleaned, dtype=float)

print("Cleaned residuals:")
print(residuals_array)

print(residuals)
residuals = np.array(residuals, dtype=float)

residuals = np.array([...])  # Your residuals here

# Calculate approximate Pearson Residuals
approx_pearson_residuals = residuals / np.std(residuals)

# Calculate standardized residuals (similar to studentized, but not the same)
standardized_residuals = (residuals - np.mean(residuals)) / np.std(residuals)

# Print the first few values of each
print("Approximate Pearson Residuals:")
print(approx_pearson_residuals[:5])
print("\nStandardized Residuals:")
print(standardized_residuals[:5])

# Some summary statistics
print("\nSummary Statistics:")
print(f"Mean of Approx. Pearson Residuals: {np.mean(approx_pearson_residuals):.4f}")
print(f"Std Dev of Approx. Pearson Residuals: {np.std(approx_pearson_residuals):.4f}")
print(f"Mean of Standardized Residuals: {np.mean(standardized_residuals):.4f}")
print(f"Std Dev of Standardized Residuals: {np.std(standardized_residuals):.4f}")

plt.scatter(y_pred, residuals)
plt.xlabel('y_pred')
plt.ylabel('Residuals')
plt.title('Residuals vs y_pred Values - Residual Plot')
plt.legend()
plt.show()



#test for homodescacity
X_test_scaled_bpt = sm.add_constant(X_test)  # Add a constant term to the features

# Perform Breusch-Pagan test

_, p_value, _, _ = het_breuschpagan(residuals, X_test_scaled_bpt)
print(f'Breusch-Pagan test Linear Regression p-value: {p_value}')


print("\nSince p Value is above 0.05 (Common norm for Breusch-Pagan tes), we can say that the data displays heterodescacity")


dw_statistic = durbin_watson(residuals)
print(f"\nDurbin-Watson statistic linear regression: {dw_statistic}")
print("Since the value is slightly below 2, it indicates a very slight positive autocorrelation, but it's so close to 2 that it's generally not a cause for concern")

