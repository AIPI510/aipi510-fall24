import boto3
import csv
import io

def lambda_handler(event, context):
    try:
        # Get bucket and key details from the event input
        source_bucket = event.get("bucket", "ta8-etl-source")  # Default to "ta8-etl-source" if not provided
        source_key = event.get("key", "SDOH_2020_ZIPCODE_1_0_upload_CA.csv")  # Default to file name
        target_bucket = event.get("destination_bucket", "ta8-etl-target")  # Default to "ta8-etl-target"

        transformed_file_key = "SDOH_2020_ZIPCODE_1_0_transformed_CA.csv"  # Transformed file name

        # Initialize the S3 client
        s3 = boto3.client('s3')

        # Step 1: Fetch the CSV file from the S3 bucket
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        file_content = response['Body'].read().decode('utf-8')

        # Step 2: Parse and transform the CSV content
        csv_reader = csv.reader(io.StringIO(file_content))
        headers = next(csv_reader)
        headers = [header.replace("\ufeff", "") for header in headers]

        required_columns = [
            "YEAR", "STATEFIPS", "ZIPCODE", "ZCTA", "STATE", "REGION", "TERRITORY", "POINT_ZIP",
            "ACS_TOT_POP_WT_ZC", "ACS_TOT_POP_US_ABOVE1_ZC", "ACS_TOT_POP_ABOVE5_ZC",
            "ACS_TOT_POP_ABOVE15_ZC", "ACS_TOT_POP_ABOVE16_ZC", "ACS_TOT_POP_16_19_ZC",
            "ACS_TOT_POP_ABOVE25_ZC", "ACS_TOT_CIVIL_POP_ABOVE18_ZC", "ACS_TOT_CIVIL_VET_POP_ABOVE25_ZC",
            "ACS_TOT_OWN_CHILD_BELOW17_ZC", "ACS_TOT_WORKER_NWFH_ZC", "ACS_TOT_WORKER_HH_ZC"
        ]

        column_indices = [headers.index(col) for col in required_columns]

        transformed_data = []
        for row in csv_reader:
            transformed_row = [row[idx] for idx in column_indices]
            transformed_data.append(transformed_row)

        # Step 3: Save the transformed data back to S3
        transformed_file_content = io.StringIO()
        csv_writer = csv.writer(transformed_file_content)
        csv_writer.writerow(required_columns)
        csv_writer.writerows(transformed_data)
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
