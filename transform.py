import boto3
import json
import urllib.parse


def lambda_handler(event, context):
    s3 = boto3.client('s3')

    try:
        # Extract the S3 URL from the event
        s3_url = json.loads(event['body'])['output_url']

        # Parse the S3 URL
        parsed_url = urllib.parse.urlparse(s3_url)
        bucket = parsed_url.netloc
        key = parsed_url.path.lstrip('/')

        # Retrieve the data from the S3 URL
        response = s3.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read().decode('utf-8')

        # Convert to lowercase
        transformed_data = data.lower()

        # Remove null values
        transformed_data = ''.join([char for char in transformed_data if char is not None])

        # Remove rows with duplicate data
        lines = transformed_data.split('\n')
        unique_lines = list(set(lines))
        transformed_data = '\n'.join(unique_lines)

        # Upload the transformed data back to the S3 bucket
        s3.put_object(Bucket=bucket, Key=key, Body=transformed_data)

        return {
            'statusCode': 200,
            'body': json.dumps(s3_url)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }