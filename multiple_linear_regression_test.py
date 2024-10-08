import pytest
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt

# Import the functions from your module
from multiple_linear_regression import (
    multiple_linear_regression,
    visualize_feature_and_target_relationship,
    visualize_residual_plot,
    linear_regression_linear_data,
    linear_regression_non_linear_data
)

# Fixtures to create datasets for the tests
@pytest.fixture
def linear_data():
    np.random.seed(42)
    X1 = 2 * np.random.rand(100, 1)
    X2 = 3 * np.random.rand(100, 1)
    X3 = 1.5 * np.random.rand(100, 1)
    y_good = 5 + 2 * X1 + 3 * X2 + 4 * X3 + np.random.randn(100, 1)
    
    data_good = pd.DataFrame(np.hstack([X1, X2, X3]), columns=['Feature1', 'Feature2', 'Feature3'])
    data_good['Target'] = y_good
    
    X_good = data_good[['Feature1', 'Feature2', 'Feature3']]
    y_good = data_good['Target']
    
    return X_good, y_good

@pytest.fixture
def non_linear_data():
    np.random.seed(42)
    X1 = 2 * np.random.rand(100, 1)
    X2 = 3 * np.random.rand(100, 1)
    X3 = 1.5 * np.random.rand(100, 1)
    y_bad = 5 + 4 * np.sin(X1 + X2 + X3) + 0.1 * np.random.randn(100, 1)
    
    data_bad = pd.DataFrame(np.hstack([X1, X2, X3]), columns=['Feature1', 'Feature2', 'Feature3'])
    data_bad['Target'] = y_bad
    
    X_bad = data_bad[['Feature1', 'Feature2', 'Feature3']]
    y_bad = data_bad['Target']
    
    return X_bad, y_bad

# Test for multiple linear regression model training and MAPE calculation
def test_multiple_linear_regression(linear_data):
    X, y = linear_data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model, mape = multiple_linear_regression(X_train, y_train, X_test, y_test)
    
    # Assert that model is a trained LinearRegression model
    assert isinstance(model, LinearRegression)
    
    # Check if the MAPE is below a certain threshold for linear data
    assert mape < 0.1, f"Expected MAPE to be < 0.1, but got {mape}"

# Test for multiple linear regression with non-linear data
def test_multiple_linear_regression_non_linear(non_linear_data):
    X, y = non_linear_data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model, mape = multiple_linear_regression(X_train, y_train, X_test, y_test)
    
    # Assert that model is a trained LinearRegression model
    assert isinstance(model, LinearRegression)
    
    # Since the data is non-linear, the MAPE should be higher
    assert mape > 0.2, f"Expected MAPE to be > 0.2 for non-linear data, but got {mape}"

# Test for visualization functions without throwing errors
def test_visualize_feature_and_target_relationship(linear_data):
    X, y = linear_data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    try:
        visualize_feature_and_target_relationship(X_train, y_train)
    except Exception as e:
        pytest.fail(f"visualize_feature_and_target_relationship raised an exception: {e}")

# Test for visualization functions without throwing errors
def test_visualize_residual_plot(linear_data):
    X, y = linear_data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model, _ = multiple_linear_regression(X_train, y_train, X_test, y_test)
    
    try:
        visualize_residual_plot(model, X_train, y_train)
    except Exception as e:
        pytest.fail(f"visualize_residual_plot raised an exception: {e}")

# Test for full flow of linear regression on linear data
def test_linear_regression_linear_data():
    try:
        linear_regression_linear_data()
    except Exception as e:
        pytest.fail(f"linear_regression_linear_data raised an exception: {e}")

# Test for full flow of linear regression on non-linear data
def test_linear_regression_non_linear_data():
    try:
        linear_regression_non_linear_data()
    except Exception as e:
        pytest.fail(f"linear_regression_non_linear_data raised an exception: {e}")
