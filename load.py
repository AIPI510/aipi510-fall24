import boto3
import json
import urllib.parse

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    destination_bucket = 'ta10-destination'
    destination_key = 'transformed_data.txt'

    try:
        # Extract the S3 URL from the event
        s3_url = json.loads(event['body'])

        # Parse the S3 URL
        parsed_url = urllib.parse.urlparse(s3_url)
        source_bucket = parsed_url.netloc
        source_key = parsed_url.path.lstrip('/')

        # Retrieve the data from the source S3 URL
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        data = response['Body'].read()

        # Upload the data to the destination S3 bucket
        s3.put_object(Bucket=destination_bucket, Key=destination_key, Body=data)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Data copied and uploaded successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }