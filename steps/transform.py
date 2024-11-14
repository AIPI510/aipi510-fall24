import json

def backward(str):
    return str[::-1]

def lambda_handler(event, context):
    payload = json.loads(event['body'])
    return {
        'statusCode': 200,
        'body': json.dumps({
            'data': [backward(data['name']) for data in payload['data']]
        })
    }
