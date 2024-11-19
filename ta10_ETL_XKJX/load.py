import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')
bucket_name = "aipi510-bucket"
folder_name = "bitcoin-data"

def lambda_handler(event, context):
    """Loads transformed data to S3. Expects a JSON object as input."""
    try:
        transformed_data = event['body']
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        file_name = f"{folder_name}/{timestamp}.json"
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(transformed_data),
            ContentType="application/json"
        )
        return {"statusCode": 200, "body": "Data successfully saved to S3"}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
