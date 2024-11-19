import json

def reverse (name):
    return name[::-1]
def lambda_handler(event, context):
    # Parse out the names by loading everything in the body field as a python dictionary and access the names from there
    payload = json.loads(event['body'])
    names = payload['names'] # should give back ['Aryan','Yash','Ashley']

    return {
        'statusCode': 200,
        'body': json.dumps({
            'names':[reverse(name) for name in names]
        })
    }
