import json

def lambda_handler(event, context):
    payload = json.loads(event['body'])
    return {
        'statusCode': 200,
        'body': json.dumps(payload)
    }
