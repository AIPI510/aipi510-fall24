import json

def lambda_handler(event, context):
    try:
        # Read the event body
        body = event['body']
        
        # Calculate the sum of cashflow
        cashflow = body.get('cashflow', {})
        cashflow_sum = sum(cashflow.values())
        
        # Prepare the response
        result = {
            'date': body['date'],
            'cashflow': cashflow_sum
        }
        
        # Return the result
        return {
            'statusCode': 200,
            'body': result
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }