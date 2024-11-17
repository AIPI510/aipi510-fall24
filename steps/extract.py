import os
import json
import requests

def lambda_handler(event, context):

    # Retrieve the environment variable
    api_key = os.environ.get('MARKETSTACK_API_KEY', 'default_value')

     # Use the environment variable in your code
    url = F"https://api.marketstack.com/v1/eod?access_key={api_key}"

    querystring = {"symbols":"AAPL,MSFT,AMZN,TSLA,NVDA"}

    response = requests.get(url, params=querystring)
    
    return {
        'statusCode': 200,
        'body': json.dumps(response.json())
    }

