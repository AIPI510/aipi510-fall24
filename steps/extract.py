import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({
            'data': [
                { 'name': 'Haran Nallasivan' },
                { 'name': 'Santosh Ganesan' }
            ]
        })
    }
