from datetime import datetime

def lambda_handler(event, context):
    data = event.get('data', [])

    transformed_data = []
    for item in data:
        # Transform and clean other fields
        item['Name'] = item.get('Name', '').strip()
        item['Country'] = item.get('Country', '').capitalize()

        # Process `Purchase_Amount` to keep only integer part
        try:
            item['Purchase_Amount'] = int(float(item.get('Purchase_Amount', 0)))
        except (ValueError, TypeError):
            item['Purchase_Amount'] = 'Invalid Amount'

        transformed_data.append(item)
    
    return {
        'statusCode': 200,
        'transformed_data': transformed_data
    }
