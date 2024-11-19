import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = event['bucket_name']
    file_key = event['file_key']
    
    # Fetch the file from S3
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    data = obj['Body'].read().decode('ISO-8859-1')
    
    # Return raw CSV data
    return {
        'statusCode': 200,
        'body': data
    }
