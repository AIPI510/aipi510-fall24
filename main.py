import json
import numpy as np
import boto3
import os

class SimpleLogisticModel:
    def __init__(self):
        self.weights = None
        self.bias = None

    def predict(self, X):
        model = np.dot(X, self.weights) + self.bias
        predictions = self._sigmoid(model)
        return [1 if i > 0.5 else 0 for i in predictions]

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

def load_model():
    s3 = boto3.client('s3')
    bucket_name = os.environ['MODEL_BUCKET']
    s3.download_file(bucket_name, 'cat_dog_model_params.json', '/tmp/model_params.json')
    with open('/tmp/model_params.json', 'r') as f:
        params = json.load(f)
    model = SimpleLogisticModel()
    model.weights = np.array(params['weights'])
    model.bias = params['bias']
    return model

def lambda_handler(event, context):
    data = json.loads(event['body'])
    model = load_model()
    prediction = model.predict(np.array(data['features']).reshape(1, -1))
    result = "Dog Lover!" if prediction[0] == 1 else "Cat Lover!"
    return {
        'statusCode': 200,
        'body': json.dumps({'prediction': result})
    }