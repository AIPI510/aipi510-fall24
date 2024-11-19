import json
import boto3
import io
import csv

def lambda_handler(event, context):
    """
    Extract function
    Processes a csv file from a bucket and returns the data as a 2D list.
    """

    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket='shaunakbucket', Key='forestfires.csv')
        file_content = response['Body'].read().decode('utf-8')
        file = io.StringIO(file_content)
        reader = csv.reader(file)
        data = list(reader)
        return {
            'statusCode': 200,
            'body': data
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
