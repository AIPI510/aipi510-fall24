import boto3
import json
import urllib.parse

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    s3_uri = 's3://ta10-aditya-and-mariam/data.csv'
    output_bucket = 'ta10-aditya-and-mariam'
    output_key = 'output_data.txt'

    # Parse the S3 URI
    parsed_url = urllib.parse.urlparse(s3_uri)
    bucket = parsed_url.netloc
    key = parsed_url.path.lstrip('/')

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read().decode('utf-8')

        # Store the data in the output S3 bucket
        s3.put_object(Bucket=output_bucket, Key=output_key, Body=data)

        # Generate the S3 URL for the stored data
        output_url = f's3://{output_bucket}/{output_key}'

        return {
            'statusCode': 200,
            'body': json.dumps({'output_url': output_url})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }