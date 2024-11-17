# lambda function assumes that the 'data' key in the API response always contains a list of dictionaries, each representing a stock entry.

import json
import pandas as pd



def lambda_handler(event, context):
    transform_response = lambda response: pd.DataFrame(json.loads(response)['data'])
    df = transform_response()

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function executed successfully')
    }
