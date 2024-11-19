import boto3
import json
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function to load the transformed data into an S3 bucket.
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Extract transformed data from the event object
        if 'body' in event:
            body = json.loads(event['body'])
            transformed_data = body.get('transformed_data', [])
        else:
            transformed_data = event.get('transformed_data', [])
        
        logger.info(f"Transformed data to load: {json.dumps(transformed_data)}")
        
        # Define the destination S3 bucket and key
        s3_bucket = 'myhuggingfacebucket002'
        s3_key = 'transformed_data.json'
        
        # Initialize S3 client
        s3 = boto3.client('s3', region_name='us-east-2')
        
        # Convert transformed data to JSON
        transformed_data_json = json.dumps(transformed_data)
        
        # Upload the transformed data to the S3 bucket
        s3.put_object(
            Bucket=s3_bucket, 
            Key=s3_key, 
            Body=transformed_data_json
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Data successfully loaded into S3 bucket.',
                'bucket': s3_bucket,
                'key': s3_key
            })
        }
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error: {error_msg}")
        return {
            'statusCode': 500,
            'error': error_msg,  # Changed to match state machine expectation
            'body': json.dumps({
                'error': error_msg,
                'stage': 'Load'
            })
        }