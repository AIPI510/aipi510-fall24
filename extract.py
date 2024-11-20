import boto3
import json
import logging

# Initialize the S3 client
s3 = boto3.client('s3')

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        # Use the provided bucket and key or default to the specified values
        bucket_name = event.get('bucket', 'etl-aipi510-ta10')  # Updated bucket name
        key = event.get('key', 'Bird_strikes.csv')  # Updated file name

        logger.info(f"Extracting data from bucket: {bucket_name}, key: {key}")

        # Fetch the object from S3
        response = s3.get_object(Bucket=bucket_name, Key=key)
        data = response['Body'].read().decode('utf-8')

        # Parse the data (assuming CSV processing needed)
        extracted_data = data.splitlines()  # Placeholder to split CSV lines

        # Return the extracted data
        return {
            'statusCode': 200,
            'body': json.dumps({'extracted_data': extracted_data})
        }

    except Exception as e:
        logger.error(f"Error extracting data: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
