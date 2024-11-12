import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def generate_data():
   X = np.random.rand(100, 1) * 10  # 100 samples, 1 feature
   y = 2.5 * X + np.random.randn(100, 1) * 2  # Linear relation with some noise
   return X, y

def split_data(X, y):
   return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):
   model = LinearRegression()
   model.fit(X_train, y_train)
   return model

def evaluate_model(model, X_test, y_test):
   y_pred = model.predict(X_test)
   mse = mean_squared_error(y_test, y_pred)
   return mse, model.coef_, model.intercept_

def main():
   X, y = generate_data()
   X_train, X_test, y_train, y_test = split_data(X, y)
   model = train_model(X_train, y_train)
   mse, coef, intercept = evaluate_model(model, X_test, y_test)

   print(f"Mean Squared Error: {mse}")
   print(f"Model Coefficients: {coef}")
   print(f"Model Intercept: {intercept}")

if __name__ == "__main__":
   main()
