import json
import boto3
from uuid import uuid4
from decimal import Decimal

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Set the table name
TABLE_NAME = 'LifeExpData'

def convert_to_decimal(obj):
    """
    Recursively converts float values in a dictionary or list to Decimal for DynamoDB.
    """
    if isinstance(obj, list):
        return [convert_to_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, float):
        return Decimal(str(obj))  # Convert float to Decimal
    return obj

def lambda_handler(event, context):
    try:
        data = event.get("body")
        if not data:
            raise ValueError("No data received.")

        data_items = json.loads(data)

        table = dynamodb.Table(TABLE_NAME)

        for item in data_items:
            
            item['id'] = str(uuid4())

            item = convert_to_decimal(item)
            
            item['AreaName'] = item.get('Area Name', 'Unknown')
            
            table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps(data_items)
        }

    except Exception as e:
        print(f"Exception occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }