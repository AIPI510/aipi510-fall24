import boto3
import csv
import io

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'ta10'
    object_key = 'sample_data.csv'

    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    file_content = response['Body'].read().decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(file_content))

    data = [row for row in csv_reader]
    return {
        'statusCode': 200,
        'data': data  # give it to the next step
    }
