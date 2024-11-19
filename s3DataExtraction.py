import boto3
import logging

# Logging configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    Extract data from an S3 bucket.
    :param event: {
        "bucket_name": "aipi510",
        "key": "Electric_Vehicle_Population_Data.csv"
    }
    :return: Extracted data or an error message
    """
    try:
        # Get bucket name and file key from the event
        bucket_name = event['bucket_name']  # Fix the key to match event structure
        key = event['key']  # Fix the key to match event structure
        
        logger.info(f"Extracting file from S3 bucket: {bucket_name}, key: {key}")
        
        # Fetch the object from S3
        response = s3.get_object(Bucket=bucket_name, Key=key)
        
        # Read the content of the file
        data = response['Body'].read().decode('utf-8')
        
        logger.info("Data extracted successfully from S3.")
        
        # Return the extracted data
        return {
            'status': 'success',
            'data': data
        }
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }
