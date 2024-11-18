import os
import json
import requests

def lambda_handler(event, context):
    '''
    Lambda function handler to extract data from the MarketStack API.
    '''

    # Retrieve the environment variable
    api_key = os.environ.get('MARKETSTACK_API_KEY', 'default_value')

     # Use the environment variable in your code
    url = f"https://api.marketstack.com/v1/eod?access_key={api_key}"

    querystring = {"symbols":"AAPL,MSFT,AMZN,TSLA,NVDA"}

    response = requests.get(url, params=querystring)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response.json())
    }

