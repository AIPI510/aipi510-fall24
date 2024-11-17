import json
import boto3
import csv
import io

def lambda_handler(event, context):

    try:
        
        source_bucket = event.get("bucket", "510-demo-bucket")
        source_key = event.get("key", "demo_510.csv")
        target_bucket = event.get("destination_bucket", "510-demo-bucket-output")

        transformed_file_key = "demo_510_transformed.csv"  # Transformed file name

        # Initialize the S3 client
        s3 = boto3.client('s3')

        # Step 1: Fetch the CSV file from the S3 bucket
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        file_content = response['Body'].read().decode('utf-8')

        # Step 2: Parse and transform the CSV content
        csv_reader = csv.reader(io.StringIO(file_content))
        headers = next(csv_reader)
        headers = [header.replace("\ufeff", "") for header in headers]  # Remove BOM characters if present

        # Append 'Transformed' to each header
        transformed_headers = [f"{header}_Transformed" for header in headers]

        # Read the remaining rows without further transformations
        transformed_data = [row for row in csv_reader]

        # Step 3: Save the transformed data back to S3
        transformed_file_content = io.StringIO()
        csv_writer = csv.writer(transformed_file_content)
        csv_writer.writerow(transformed_headers)  # Write transformed headers
        csv_writer.writerows(transformed_data)    # Write original rows
        transformed_file_content.seek(0)

        s3.put_object(Bucket=target_bucket, Key=transformed_file_key, Body=transformed_file_content.getvalue())

        return {
            "statusCode": 200,
            "message": "CSV file transformed and saved successfully!",
            "transformed_rows_count": len(transformed_data)
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "error": str(e)
        }