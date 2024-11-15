import numpy as np
import json

# Defining a simple logistic regression model
class SimpleLogisticModel:
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None

    def train(self, X, y):
        samples, features = X.shape
        self.weights = np.zeros(features)
        self.bias = 0
        for _ in range(self.epochs):
            model = np.dot(X, self.weights) + self.bias
            predictions = self._sigmoid(model)
            dw = (1 / samples) * np.dot(X.T, (predictions - y))
            db = (1 / samples) * np.sum(predictions - y)
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X):
        model = np.dot(X, self.weights) + self.bias
        return [1 if i > 0.5 else 0 for i in self._sigmoid(model)]

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

# Fake data (because real scientists make up their own, right?)
np.random.seed(0)
data = np.random.randint(1, 10, (100, 5))
labels = (data[:, 1] > 5).astype(int)

# Training and saving model parameters as JSON
model = SimpleLogisticModel()
model.train(data, labels)

model_params = {
    "weights": model.weights.tolist(),
    "bias": model.bias
}

with open("cat_dog_model_params.json", "w") as f:
    json.dump(model_params, f)