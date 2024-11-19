import json

def lambda_handler(event, context):
    """Transforms raw data from the Coindesk API. Expects a JSON object as input."""
    try:
        raw_data = event['body']
        timestamp = raw_data['time']['updatedISO']
        prices = {
            "USD": raw_data['bpi']['USD']['rate_float'],
            "GBP": raw_data['bpi']['GBP']['rate_float'],
            "EUR": raw_data['bpi']['EUR']['rate_float']
        }
        transformed_data = {"timestamp": timestamp, "prices": prices}
        return {"statusCode": 200, "body": transformed_data}
    except KeyError as e:
        return {"statusCode": 400, "body": f"Missing key: {str(e)}"}