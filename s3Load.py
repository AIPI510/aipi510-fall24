import boto3
import os

# Initialize S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Extract filtered data and metadata from the event
        filtered_data = event.get('filtered_data')
        if not filtered_data:
            raise ValueError("No filtered data found in the input event.")
        
        # Define the destination bucket and key
        destination_bucket = "aipi510des"  # Replace with your bucket name
        destination_key = "filtered_nc_vehicles.csv"  # Define the file name
        
        # Upload the filtered data to S3
        s3.put_object(
            Bucket=destination_bucket,
            Key=destination_key,
            Body=filtered_data,
            ContentType='text/csv'
        )
        
        return {
            "status": "success",
            "message": f"Data successfully loaded to s3://{destination_bucket}/{destination_key}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
