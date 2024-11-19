import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = event['destination_bucket_name']
    file_key = event['destination_file_key']
    cleaned_data = event['cleaned_data']
    
    # Save cleaned data to the destination S3 bucket
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=cleaned_data)
    
    return {
        'statusCode': 200,
        'message': 'Cleaned data successfully saved to S3'
    }
