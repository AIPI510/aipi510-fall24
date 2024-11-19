import boto3

def lambda_handler(event, context):
    try:
        # Extract parameters from the event
        transformed_file_content = event.get("transformed_file_content", "")
        target_bucket = event.get("destination_bucket", "510-demo-bucket-output")
        transformed_file_key = "demo_510_transformed.csv"

        # Initialize the S3 client
        s3 = boto3.client('s3')

        # Upload the transformed file to the target bucket
        s3.put_object(Bucket=target_bucket, Key=transformed_file_key, Body=transformed_file_content)

        return {
            "statusCode": 200,
            "message": "Transformed file uploaded successfully!",
            "destination": {
                "bucket": target_bucket,
                "key": transformed_file_key
            }
        }

    except Exception as e:
        print("Error during loading:", str(e))
        return {
            "statusCode": 500,
            "error": str(e)
        }