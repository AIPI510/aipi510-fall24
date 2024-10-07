import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def main():
    print("Generating test data for a linear regression example...")
    
    # Generate an array of 100 random numbers between 0 and 10
    x = np.random.rand(100, 1) * 10

    # Compute `y` values based on the linear relationship `y = 2x + 1 + randn(100, 1)`
    y = 2 * x + 1 + np.random.randn(100, 1)
    
    # Split the data into training and testing sets (80/20)
    print("Splitting the data into training and testing sets...")
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    # Create a linear regression model
    model = LinearRegression()

    # Fit the model to the training data
    print("Training the linear regression model...")
    model.fit(x_train, y_train)

    # Make predictions on the test data
    print("Making predictions on the test data...")
    y_pred = model.predict(x_test)

    # Plot the test data (scatterplot)
    plt.scatter(x_test, y_test, color='blue')

    # Plot the linear regression model (line plot)
    plt.plot(x_test, y_pred, color='red', linewidth=2)

    # Add labels and title to the plot
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Linear Regression Example')

    # Create a text box that includes the linear regression equation
    plt.text(6, 4, "y = %.2f + %.2fx" % (model.intercept_, model.coef_), 
            bbox=dict(facecolor='gray', alpha=0.5))

    # Create a text box that includes the sum of squared errors (SSE) and R-squared value
    plt.text(0.5, 18, 
            "Sum of squared error (SSE): %.2f\nCoefficient of determination: %.2f" % 
            (np.sum((y_test - y_pred) ** 2), model.score(x_test, y_test)),
            bbox=dict(facecolor='gray', alpha=0.5))
    
    # Save the plot as a PNG file
    plt.savefig('linear-regression.png')

    print("Model trained and evaluated successfully!")
    print("Open linear-regression.png to view the model results.")


if __name__ == "__main__":
    main()