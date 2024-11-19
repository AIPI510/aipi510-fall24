import json
from urllib import request

def lambda_handler(event, context):
    """Extracts current bitcoin price from the Coindesk API. No input required."""
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    try:
        response = request.urlopen(url)
        data = json.load(response)
        return {"statusCode": 200, "body": data}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}