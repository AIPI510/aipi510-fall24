import boto3
import json
import pandas as pd 

def lambda_handler(event, context):
    # use s3 to connect to the bucket
    s3 = boto3.client('s3')
    # define the input JSON items
    bucket_name = event['bucket_name']
    key = event['csv']
    try:
        # get object from s3 and then read it, store as data
        response = s3.get_object(Bucket=bucket_name, Key=key)
        data = response['Body'].read().decode('utf-8')
        
        return {"status": "success", "data": data}

    # error handling
    except Exception as e:
        return {"status": "error", "message": str(e)}