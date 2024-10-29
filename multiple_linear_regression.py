import pytest
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error
from matplotlib import pyplot as plt

import http.server
import socketserver
import webbrowser
import threading

# HTML content for creative part as a string
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Multiple Linear Regression with 3D Plot and Fitted Plane</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script> <!-- Load Plotly for interactive plots -->
</head>
<body>
    <h1>Interactive Multiple Linear Regression with 3D Plot and Fitted Plane</h1>

    <form id="regressionForm">
        <label for="x1">X1 (Comma separated values):</label><br>
        <input type="text" id="x1" name="x1" placeholder="E.g. 2.3, 3.5, 4.7"><br><br>

        <label for="x2">X2 (Comma separated values):</label><br>
        <input type="text" id="x2" name="x2" placeholder="E.g. 1.1, 2.2, 3.3"><br><br>

        <label for="y">Y (Target, Comma separated values):</label><br>
        <input type="text" id="y" name="y" placeholder="E.g. 10, 20, 30"><br><br>

        <button type="submit">Run Regression</button>
    </form>

    <div id="output"></div> <!-- To display the regression results -->
    <div id="regressionPlot" style="width: 100%; height: 500px;"></div> <!-- For the 3D Plot -->

    <script>
        // JavaScript code for linear regression and plotting (as shown in the uploaded file)
    </script>
</body>
</html>
"""

# Opening the creative part in a web browser

class CustomHandler(http.server.SimpleHTTPRequestHandler):

    """ A custom request handler that serves the HTML content. """

    def do_GET(self):
        # Set the response status code
        self.send_response(200)
        
        # Set headers
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # Write the HTML content to the response
        self.wfile.write(html_content.encode("utf-8"))

def start_server():

    """ Start the server to serve the HTML content. """

    PORT = 8082
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

def open_creative_part():

    """ Open the creative part in a web browser. """

    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Open the web browser to the local server
    webbrowser.open("http://localhost:8082")



# Multiple Linear Regression
def multiple_linear_regression(X_train, y_train,X_test, y_test):
    """

    This function trains a multiple linear regression model on the training set and evaluates it on the test set.

    Parameters:
    X_train: The input features of the training set.
    y_train: The target values of the training set.
    X_test: The input features of the test set.
    y_test: The target values of the test set.

    Returns:
    model: The trained linear regression model.
    mse: The mean squared error of the model on the test set.

    """

    # Initialize the model
    model = LinearRegression()

    # Train the model
    model.fit(X_train, y_train)

    # Predict the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    mape = mean_absolute_percentage_error(y_test, y_pred)

    return model,mape

# feature and target relationship visualization
def visualize_feature_and_target_relationship(X_train, y_train):
    """
    This function visualizes the relationship between the input features and the target values.

    Parameters:

    model: The trained linear regression model.
    X_train: The input features of the training set.
    y_train: The target values of the training set.
    X_test: The input features of the test set.
    y_test: The target values of the test set.

    """
    
    # Get the feature names
    feature_names = X_train.columns

    # Create a figure and axis
    fig, axs = plt.subplots(1, len(feature_names), figsize=(20, 5))

    if len(feature_names) == 1:
        axs = [axs]

    # Plot the relationship between each feature and the target
    for i, feature_name in enumerate(feature_names):
        # Plot the training data
        axs[i].scatter(X_train[feature_name], y_train, label='Train', color='blue')
        # Plot the regression line
        axs[i].set_xlabel(feature_name)
        axs[i].set_ylabel('Target')
        axs[i].legend()
        
# Multiple Linear Regression Visualization
def visualize_residual_plot(model, X_train, y_train):
    """
    This function visualizes the residual plot of the model.

    Parameters:

    model: The trained linear regression model.
    X_train: The input features of the training set.
    y_train: The target values of the training set.
    X_test: The input features of the test set.
    y_test: The target values of the test set.

    """
    
    # Predict the test set
    y_pred = model.predict(X_train)
    
    # Calculate the residuals
    residuals = y_train - y_pred
    
    # Create a residual plot
    plt.figure(figsize=(10, 5))
    plt.scatter(y_pred, residuals, color='blue')
    plt.axhline(y=0, color='black', linestyle='--')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title('Residual Plot')
    plt.show()

# Linear Regression using data with linear relationship

def linear_regression_linear_data():
    """
    This function gives a linear regression demo using data with a linear relationship.

    """

    np.random.seed(42)

    # Random values for Feature1
    X1 = 2 * np.random.rand(100, 1)  
    # Random values for Feature2
    X2 = 3 * np.random.rand(100, 1)  
    # Random values for Feature3
    X3 = 1.5 * np.random.rand(100, 1)  

    # Linear relationship
    y_good = 5 + 2*X1 + 3*X2 + 4*X3 + np.random.randn(100, 1)

    data_good = pd.DataFrame(np.hstack([X1, X2, X3]), columns=['Feature1', 'Feature2', 'Feature3'])
    data_good['Target'] = y_good
    
    # Features and target
    X = data_good[['Feature1', 'Feature2', 'Feature3']]
    y = data_good['Target']

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a multiple linear regression model
    model,mape = multiple_linear_regression(X_train, y_train, X_test, y_test)
    
    print("Linear Regression using data with linear relationship:")

    # Display mean abosolute percentage error
    print(f"Mean Absolute Percentage Error: {mape}")

    # Display model coefficients
    print("Coefficients:", model.coef_)
    print("Intercept:", model.intercept_)
    
    # Visualize the linear regression model
    visualize_feature_and_target_relationship(X_train, y_train)
    visualize_residual_plot(model, X_train, y_train)

# Linear Regression using data with non-linear relationship

def linear_regression_non_linear_data():
    """
    This function gives a linear regression demo using data with a non-linear relationship.
    
    """

    X1 = 2 * np.random.rand(100, 1)  
    # Random values for Feature2
    X2 = 3 * np.random.rand(100, 1)  
    # Random values for Feature3
    X3 = 1.5 * np.random.rand(100, 1)  

    y_bad = 5 + 4*np.sin(X1+X2+X3)+ 0.1 * np.random.randn(100, 1)  # Non-linear relationship (sine wave)

    data_bad = pd.DataFrame(np.hstack([X1,X2,X3, y_bad]), columns=['Feature1','Feature2','Feature3', 'Target'])

    # Features and target
    X_bad = data_bad[['Feature1','Feature2','Feature3']]
    y_bad = data_bad['Target']

    # Split the data into training and test sets
    X_train_bad, X_test_bad, y_train_bad, y_test_bad = train_test_split(X_bad, y_bad, test_size=0.2, random_state=42)

    # Train a multiple linear regression model
    model_bad,mape_bad = multiple_linear_regression(X_train_bad, y_train_bad, X_test_bad, y_test_bad)

    print("Linear Regression using data with non-linear relationship:")

    # Display mean abosolute percentage error
    print(f"Mean Absolute Percentage Error: {mape_bad}")

    # Display model coefficients
    print("Coefficients:", model_bad.coef_)
    print("Intercept:", model_bad.intercept_)

    # Visualize the linear regression model
    visualize_feature_and_target_relationship(X_train_bad, y_train_bad)
    visualize_residual_plot(model_bad, X_train_bad, y_train_bad)

if __name__ == '__main__':
    
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(description="A simple example of argparse usage.")

    # Add arguments
    parser.add_argument("--creative", type=bool, default=False, help="Whether need to show creative part")  # Optional argument with a default value

    # Parse the arguments
    args = parser.parse_args()

    if args.creative==True:
        open_creative_part()
    else:
        linear_regression_linear_data()
        linear_regression_non_linear_data()


# Unit tests for the functions

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
