import boto3
import json

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    destination_bucket = 'etl-pipeline-destination'
    destination_key = 'transformed-data.json'

    # Get transformed data from the event
    data = event['body']

    # Store transformed data in S3
    s3_client.put_object(
        Bucket=destination_bucket,
        Key=destination_key,
        Body=json.dumps(data)
    )

    return {
        'statusCode': 200,
        'body': 'Data loaded successfully'
    }

