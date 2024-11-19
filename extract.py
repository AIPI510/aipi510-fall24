import boto3

def lambda_handler(event, context):
    try:
        # Extract parameters from the event
        source_bucket = event.get("bucket", "510-demo-bucket")
        source_key = event.get("key", "demo_510.csv")

        # Initialize the S3 client
        s3 = boto3.client('s3')

        # Fetch the CSV file from the S3 bucket
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        file_content = response['Body'].read().decode('utf-8')

        # Return the file content
        return {
            "statusCode": 200,
            "file_content": file_content,
            "headers": {
                "bucket": source_bucket,
                "key": source_key
            }
        }

    except Exception as e:
        print("Error during extraction:", str(e))
        return {
            "statusCode": 500,
            "error": str(e)
        }