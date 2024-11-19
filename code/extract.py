import json
import boto3

def lambda_handler(event, context):
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    # Define the bucket name and file key
    bucket_name = 'harrybucket-aipi510'
    file_key = 'sample_input.json'
    
    # Get the file content from S3
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        content = response['Body'].read().decode('utf-8')
        json_content = json.loads(content) # return type: dict
        
        # Return the JSON content
        return {
            'statusCode': 200,
            'body': json_content
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }