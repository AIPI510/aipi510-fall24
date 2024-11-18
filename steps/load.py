import json
import boto3
from datetime import datetime

BUCKET_NAME = 'aipi510-forever-loop-ta8-etl'

def get_key():
    '''
    Constructs an S3 object key using the current ISO datetime, suffixed by '.csv'.
    '''
    current_time = datetime.now()
    iso_time = current_time.isoformat()
    return iso_time + '.csv'

def lambda_handler(event, context):
    '''
    Lambda function handler to load data into S3.
    '''

    csv_text = event['body']

    # Create S3 client
    s3_client = boto3.client('s3')

    # Write buffer to S3 object
    key = get_key()
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=csv_text
    )

    # Return Lambda output with Bucket and Key
    return {
        'statusCode': 200,
        'body': json.dumps({
            'Bucket': BUCKET_NAME,
            'Key': key,
        })
    }
