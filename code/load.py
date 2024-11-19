import json
import boto3

def lambda_handler(event, context):
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    # Define the bucket name and file key
    bucket_name = 'harrybucket-aipi510'
    file_key = 'output.json'
    
    try:
        # Read the event body
        body = event['body']
        
        # Parse the JSON string if necessary
        if isinstance(body, str):
            body = json.loads(body)
        
        # Convert the body to a JSON string
        json_body = json.dumps(body)
        
        # Save the JSON content to S3
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=json_body)
        
        # Return success response
        return {
            'statusCode': 200,
            'body': 'File saved successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
