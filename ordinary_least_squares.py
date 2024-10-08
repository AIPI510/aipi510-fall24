import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import unittest

def perform_ols_regression(X, y):
    """
    Performs Ordinary Least Squares (OLS) regression.
    
    Parameters:
    X (pd.DataFrame): Features (independent variables) in the dataset.
    y (pd.Series): Target (dependent variable) in the dataset.
    
    Returns:
    result (RegressionResults): Contains information about the regression results.
    """
    # Add a constant to the model (intercept)
    X = sm.add_constant(X)
    
    # Create the OLS model
    model = sm.OLS(y, X)
    
    # Fit the model
    result = model.fit()
    
    return result

#create synthetic dataset
np.random.seed(0)
X = pd.DataFrame({
    'feature1': np.random.rand(100),
    'feature2': np.random.rand(100)
})
y = 3 + 2 * X['feature1'] + 1 * X['feature2'] + np.random.randn(100) * 0.5

#perform OLS Regression
ols_result = perform_ols_regression(X, y)
print(ols_result.summary())

#Scatter Plots with Regression Lines
sns.set(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for idx, feature in enumerate(X.columns):
    sns.regplot(x=X[feature], y=y, ax=axes[idx])
    axes[idx].set_title(f'Scatter Plot: {feature} vs. y')
    axes[idx].set_xlabel(feature)
    axes[idx].set_ylabel('y')

#Residual Plot
plt.figure(figsize=(8, 6))
sns.residplot(x=ols_result.fittedvalues, y=ols_result.resid, lowess=True, line_kws={'color': 'red'})
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.show()

#Coefficient Plot
coef_df = pd.DataFrame(ols_result.params, columns=["Coefficient"])
coef_df = coef_df.drop("const")
coef_df.plot(kind='bar', figsize=(8, 6))
plt.title("OLS Regression Coefficients")
plt.xlabel("Features")
plt.ylabel("Coefficient Value")
plt.xticks(rotation=0)
plt.show()

#Unit testing
class TestOLSRegression(unittest.TestCase):
    def test_ols_output(self):
        result = perform_ols_regression(X, y)
        # Test if the result has an attribute 'params' for coefficients
        self.assertTrue(hasattr(result, 'params'))
        
    def test_ols_rsquare(self):
        result = perform_ols_regression(X, y)
        # Test if R-squared value is between 0 and 1
        self.assertGreaterEqual(result.rsquared, 0)
        self.assertLessEqual(result.rsquared, 1)

if __name__ == '__main__':
    unittest.main()
