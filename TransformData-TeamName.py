import json
import csv
import io

def lambda_handler(event, context):

    """
    Transform the data by filling missing values in the 'relationship' column.
    """

    try:
        # Get the data from the previous step
        original_data = event['data']
        
        # Read the raw CSV data into a list of dictionaries and do data engineering.
        transformed_data = []
        csv_reader = csv.DictReader(io.StringIO(original_data))

        for row in csv_reader:
            # Fill missing values in all columns with 'none'
            for key in row:
                if not row[key]:  # Check if the value is missing or empty
                    row[key] = 'none'
            transformed_data.append(row)

        # Convert the processed data back to CSV format
        csv_buffer = io.StringIO()
        csv_writer = csv.DictWriter(csv_buffer, fieldnames=transformed_data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(transformed_data)
        
        transformed_data = csv_buffer.getvalue()
        
        print("Data transformed successfully")
        
        # Pass transformed data to the next step
        return {"status": "success", 
                "transformed_data": transformed_data,
                "destination_bucket": event["destination_bucket"],
                "destination_key": event["destination_key"]
                }
    
    except Exception as e:
        print(f"Error during transformation: {e}")
        raise e
