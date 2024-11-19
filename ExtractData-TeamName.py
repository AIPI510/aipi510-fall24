import boto3
import json

def lambda_handler(event, context):

    """
    Extract the data from the source S3 bucket.
    """
    
    # S3 bucket and object details
    s3 = boto3.client('s3')
    bucket_name = event['bucket_name']
    key = event['key']
    
    try:
        # Get the object from S3
        response = s3.get_object(Bucket=bucket_name, Key=key)
        data = response['Body'].read().decode('utf-8')
        
        print("Data extracted successfully")
        
        # Pass data to the next step
        return {"status": "success", 
                "data": data,
                "destination_bucket": event["destination_bucket"],
                "destination_key": event["destination_key"]
                }
    
    except Exception as e:
        print(f"Error during extraction: {e}")
        raise e
