import boto3
import json

def lambda_handler(event, context):
    
    """
    Load the transformed data into the destination S3 bucket.
    """

    # S3 bucket and object details for saving the transformed data
    s3 = boto3.client('s3')
    destination_bucket = event['destination_bucket']
    destination_key = event['destination_key']
    transformed_data = event['transformed_data']
    
    try:
        # Put the transformed data into the destination S3 bucket
        s3.put_object(Bucket=destination_bucket, Key=destination_key, Body=transformed_data)
        
        print("Data loaded successfully")
        return {"status": "success", "message": "Data loaded into destination"}
    
    except Exception as e:
        print(f"Error during loading: {e}")
        raise e
