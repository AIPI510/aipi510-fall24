import json

def lambda_handler(event, context):
    # Receive data from the previous step
    data = event['body']

    # Perform data transformation
    transformed_data = []
    for record in data:
        transformed_record = {
            'id': record['id'],
            'name': record['name'].upper(),  # Example transformation
            'value': record['value'] * 2     # Example aggregation
        }
        transformed_data.append(transformed_record)

    # Pass transformed data to the next step
    return {
        'statusCode': 200,
        'body': transformed_data
    }

