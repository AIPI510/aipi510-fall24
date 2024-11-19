import json
import boto3


def lambda_handler(event, context):
    # Initialize the S3 client
    s3 = boto3.client('s3')
    
    # Specify the bucket name and file key
    bucket_name = 'ta10-510-2024'
    file_key = 'output.json'
    
    # Create a sample JSON object
    # In a real scenario, this could come from the event or other sources
    data = json.loads(event['body'])
    
    try:
        # Convert the JSON object to a string
        json_data = json.dumps(data)
        
        # Put the JSON string as an object in the S3 bucket
        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json_data,
            ContentType='application/json'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully uploaded JSON to S3')
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
