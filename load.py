# LOAD lambda function
import json
import boto3
import csv
import io

def lambda_handler(event, context):
    """
    Accepts a JSON with a body of 2D list
    Saves the file to a csv in the bucket
    Returns: 200 if succeeded, else 500
    """
    try:
        transformed_list = event['body']
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerows(transformed_list)
        s3 = boto3.client('s3')
        s3.put_object(Bucket='shaunakbucket', Key='transformed_fires.csv', Body = buffer.getvalue())
        return {
            'statusCode': 200,
            'body': 'Saved file to bucket successfully!'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }