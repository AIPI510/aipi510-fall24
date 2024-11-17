import boto3
import csv
import io
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    A single Lambda function to perform the ETL process:
    - Extract: Fetch data from an S3 bucket.
    - Transform: Clean and format the data.
    - Load: Save the transformed data to another S3 bucket.
    
    Parameters:
    - event: A JSON object containing:
        - 'bucket': Source bucket name
        - 'key': File name in the source bucket
        - 'destination_bucket': Target bucket name
    
    Returns:
    - A success message with the count of transformed rows or an error message.
    """
    # Extract input details from the event
    source_bucket = event['bucket']
    source_key = event['key']
    destination_bucket = event['destination_bucket']
    transformed_key = "SDOH_2020_ZIPCODE_1_0_transformed_CA.csv"  # Default name for the transformed file

    # Initialize S3 client
    s3 = boto3.client('s3')

    try:
        # Step 1: Extract - Fetch the CSV file from the source S3 bucket
        logger.info(f"Fetching file {source_key} from bucket {source_bucket}")
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        file_content = response['Body'].read().decode('utf-8')

        # Step 2: Transform - Process the CSV content
        logger.info("Transforming data...")
        csv_reader = csv.reader(io.StringIO(file_content))
        headers = next(csv_reader)
        headers = [header.replace("\ufeff", "") for header in headers]  # Clean headers

        # Define the required columns
        required_columns = [
            "YEAR", "STATEFIPS", "ZIPCODE", "ZCTA", "STATE", "REGION", "TERRITORY", "POINT_ZIP"
        ]
        column_indices = [headers.index(col) for col in required_columns]

        transformed_data = []
        for row in csv_reader:
            transformed_row = [row[idx] for idx in column_indices]
            transformed_data.append(transformed_row)

        # Convert transformed data to CSV
        transformed_csv = io.StringIO()
        csv_writer = csv.writer(transformed_csv)
        csv_writer.writerow(required_columns)  # Write headers
        csv_writer.writerows(transformed_data)  # Write transformed rows
        transformed_csv.seek(0)

        # Step 3: Load - Save the transformed data to the target bucket
        logger.info(f"Uploading transformed file to bucket {destination_bucket}")
        s3.put_object(Bucket=destination_bucket, Key=transformed_key, Body=transformed_csv.getvalue())

        logger.info("ETL process completed successfully!")
        return {
            "statusCode": 200,
            "message": "ETL process completed successfully!",
            "transformed_rows_count": len(transformed_data)
        }

    except Exception as e:
        logger.error(f"Error during ETL process: {str(e)}")
        return {
            "statusCode": 500,
            "error": str(e)
        }
