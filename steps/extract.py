import os
import json
import requests







def lambda_handler(event, context):

    # Retrieve the environment variable
    my_env_var = os.environ.get('MARKETSTACK_API_KEY', 'default_value')

     # Use the environment variable in your code
    message = f"The value of MY_ENV_VAR is: {my_env_var}"

    url = F"https://api.marketstack.com/v1/eod?access_key={my_env_var}"

    querystring = {"symbols":"AAPL,MSFT,AMZN,TSLA,NVDA"}

    response = requests.get(url, params=querystring)

    print(response.json())


    
    return {
        'statusCode': 200,
        'body': json.dumps(response.json())
    }

