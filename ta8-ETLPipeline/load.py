import boto3
import json

def lambda_handler(event, context):
    """
    Saves the transformed data to an S3 bucket as a JSON file.

    Args:
        event (dict): Event data passed by Step Functions (output of Transform function).
        context (object): Lambda context object.

    Returns:
        dict: Response containing status code and success/error message.
    """
    # S3 client
    s3 = boto3.client('s3')
    
    # Destination bucket details
    bucket_name = "destination-bucketeast2"  # Replace with your destination bucket name
    file_key = "transformed-user-data.json"  # Output file name for transformed data
    
    # Extract transformed data from the event
    transformed_data = event.get('transformed_data', None)
    
    # Ensure transformed_data exists in the event
    if not transformed_data:
        error_message = "Missing 'transformed_data' in the input event."
        print(error_message)
        return {
            "statusCode": 400,
            "error": error_message
        }

    try:
        # Write transformed data to the destination bucket
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=json.dumps(transformed_data))
        print(f"Data successfully loaded to {bucket_name}/{file_key}")
        
        return {
            "statusCode": 200,
            "message": f"Data successfully loaded to {bucket_name}/{file_key}"
        }
    except s3.exceptions.NoSuchBucket:
        # Handle case where the destination bucket does not exist
        error_message = f"Destination bucket '{bucket_name}' does not exist."
        print(error_message)
        return {
            "statusCode": 404,
            "error": error_message
        }
    except Exception as e:
        # Handle other exceptions
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        return {
            "statusCode": 500,
            "error": error_message
        }
