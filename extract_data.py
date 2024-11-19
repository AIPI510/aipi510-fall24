import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.client('s3')
    bucket ='sourcesavvy1'
    key = 'sample-data.json'

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        data = json.loads(content)


        return {
            'statusCode': 200,
            'body': data
        }   
    except Exception as e:
        print(f"Error extracting data: {str(e)}")
        raise e