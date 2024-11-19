import csv
import io

def lambda_handler(event, context):
    # Input raw CSV data
    raw_data = event['body']

    # Create file-like objects for reading and writing
    input_csv = io.StringIO(raw_data)
    output_csv = io.StringIO()

    # Read the input CSV and write to the output, skipping rows with null 'first.donated'
    reader = csv.DictReader(input_csv)
    fieldnames = reader.fieldnames  # Get column names
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)

    writer.writeheader()  # Write header to the output CSV
    for row in reader:
        # Skip rows where 'first.donated' is empty or null
        if row['first.donated']:
            writer.writerow(row)

    # Return cleaned data
    return {
        'statusCode': 200,
        'cleaned_data': output_csv.getvalue()
    }
