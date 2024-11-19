import csv
import io

def lambda_handler(event, context):
    try:
        # Extract file content from the event
        file_content = event.get("file_content", "")

        # Parse the CSV content
        csv_reader = csv.reader(io.StringIO(file_content))
        headers = next(csv_reader)
        headers = [header.replace("\ufeff", "") for header in headers]  # Remove BOM characters if present

        # Append 'Transformed' to each header
        transformed_headers = [f"{header}_Transformed" for header in headers]

        # Read the remaining rows without changes
        transformed_data = [row for row in csv_reader]

        # Prepare transformed content as a CSV
        transformed_file_content = io.StringIO()
        csv_writer = csv.writer(transformed_file_content)
        csv_writer.writerow(transformed_headers)  # Write transformed headers
        csv_writer.writerows(transformed_data)    # Write original rows
        transformed_file_content.seek(0)

        # Return the transformed content
        return {
            "statusCode": 200,
            "transformed_file_content": transformed_file_content.getvalue()
        }

    except Exception as e:
        print("Error during transformation:", str(e))
        return {
            "statusCode": 500,
            "error": str(e)
        }