import json
import pickle
import boto3
import numpy as np
from io import BytesIO

# Define the function to load the model from S3
def load_model():
    s3 = boto3.client('s3')
    bucket_name = 'churn-challenge'
    model_key = 'xgbr_model.pkl'  
    
    # Download the model file from S3
    response = s3.get_object(Bucket=bucket_name, Key=model_key)
    model = pickle.loads(response['Body'].read())
    return model

# Define the function to load the preprocessor from S3
def load_processor():
    s3 = boto3.client('s3')
    bucket_name = 'churn-challenge'
    processor_key = 'preprocessor.pkl'  
    
    # Download the preprocessor file from S3
    response = s3.get_object(Bucket=bucket_name, Key=processor_key)
    processor = pickle.loads(response['Body'].read())
    return processor

# Define a function to transform incoming data
def data_transform(features, processor):
    """
    Transforms input features using the preloaded processor.

    Args:
        features (np.array): Input feature array.

    Returns:
        np.array: Transformed feature array.
    """
    # Assuming 'processor' is a pre-fitted transformation pipeline
    transformed_features = processor.transform(features)
    return transformed_features

# Lambda handler function
def lambda_handler(event, context):
    try:
        # Parse the incoming request JSON to extract features
        data = json.loads(event['body'])
        
        # Convert the 'features' list from the event into a 2D NumPy array for model input
        features = np.array(data['features']).reshape(1, -1)

        # Load the model and preprocessor
        model = load_model()
        processor = load_processor()

        # Apply preprocessing to features
        transformed_features = data_transform(features, processor)

        # Predict using the model and rounded output
        prediction = np.rint(model.predict(transformed_features))

        # Return prediction as JSON
        return {
            'statusCode': 200,
            'body': json.dumps({'prediction': prediction.tolist()})
        }
    
    except Exception as e:
        # Handle any exceptions, returning a JSON response with an error message
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
