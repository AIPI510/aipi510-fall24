'''
This script contains the lambda handler function that is used to load the data (i.e saving the data
into S3 as a csv file)
'''
import json
import boto3
import gzip
import base64
from io import StringIO
import pandas as pd

def lambda_handler(event, context):
    # Get compressed data from previous state
    compressed_data = event['dataframe']
    
    # uncompress the data
    json_data = gzip.decompress(base64.b64decode(compressed_data)).decode('utf-8')
    df = pd.read_json(json_data, orient='records')

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    # Upload CSV to S3
    s3 = boto3.client('s3')
    s3.put_object(
            Bucket='aipi510-ta10',
            Key='data/cocktails.csv',
            Body=csv_buffer.getvalue()
    )

    return {
    'statusCode': 200,
    'dataframe': "successfully completed"
    }