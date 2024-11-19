import json
import boto3

def lambda_handler(event, context):
    
    
   # Initialize the S3 client
    s3 = boto3.client('s3')
    
    # Specify the bucket name and file key
    bucket_name = 'ta10-510-2024'
    file_key = 'ta10-test.json'
    
    try:
        # Get the object from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        
        # Read the content of the file
        file_content = response['Body'].read().decode('utf-8')
        
        # Parse the JSON content
        json_content = json.loads(file_content)
        
        # Process the JSON data as needed
        # For example, you can return it as the Lambda response
        return {
            'statusCode': 200,
            'body': json.dumps(json_content)
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
