import boto3
import json
import logging

# Initialize the S3 client
s3 = boto3.client('s3')

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):  # Remove "Load." here
    try:
        # Use the provided bucket for transformed data
        bucket_name = 'transformeddatabucketaipi'  # Destination bucket for transformed data
        key = 'transformed/Bird_strikes_transformed.json'  # File name for the transformed data

        # Extract the aggregated data from the event body
        aggregated_data = json.loads(event['body'])['aggregated_data']

        # Log the save operation
        logger.info(f"Saving transformed data to S3 bucket: {bucket_name}, key: {key}")

        # Save the transformed data to S3
        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(aggregated_data)
        )

        # Return success response
        return {
            'statusCode': 200,
            'body': 'Data loaded successfully into the transformed data bucket!'
        }

    except KeyError as e:
        logger.error(f"Missing key in event: {str(e)}")
        return {
            'statusCode': 400,
            'body': f'Missing or incorrect input key: {str(e)}'
        }

    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error loading data: {str(e)}'
        }
