import boto3
import csv
import io

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'ta10'
    object_key = 'transformed_data.csv'

    data = event['transformed_data']
    if isinstance(data, list) and data:
        fieldnames = data[0].keys()
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

        s3.put_object(Bucket=bucket_name, Key=object_key, Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'message': 'Data loaded successfully as CSV'
    }
