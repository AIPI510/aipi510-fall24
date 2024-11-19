import boto3
import json

def lambda_handler(event, context):
    # Example: Loading data to S3
    s3 = boto3.client('s3')
    # We decided to hard-code the bucket_name and the key(file name) to avoid errors.
    bucket_name = "daves-data-collector-bucket" # aka. event['bucket_name']
    key = "nicu_transformed.csv" # aks. event['csv']
    
    try:
        # Get the CSV data from the event
        csv_data = event['data']
        
        # Save to S3 destination bucket 
        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=csv_data,
            ContentType="text/csv"  # Ensure the file is recognized as a CSV
        )
        return {"status": "success"}
    # error handling
    except Exception as e:
        return {"status": "error", "message": str(e)}
