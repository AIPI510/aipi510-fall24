import boto3
import json

# Initialize DynamoDB resource and reference the table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('sourcesavvy_data')

def lambda_handler(event, context):
    # Extract items from the event's body
    items = event['body']
    
    # Convert items from JSON string to Python list of dictionaries, if needed
    if isinstance(items, str):
        items = json.loads(items)

    # Define the required keys for your DynamoDB table
    required_keys = ["id"]  # Adjust this list to match your table schema, e.g., ["id", "timestamp"]

    # Validate each item before insertion
    valid_items = []
    for item in items:
        if isinstance(item, dict):
            # Check if all required keys are present
            if all(key in item for key in required_keys):
                valid_items.append(item)
            else:
                missing_keys = [key for key in required_keys if key not in item]
                print(f"Skipping item due to missing keys {missing_keys}: {item}")
        else:
            print(f"Skipping non-dictionary item: {item}")

    # Load valid items into DynamoDB
    try:
        with table.batch_writer() as batch:
            for item in valid_items:
                batch.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': 'Data uploaded successfully'
        }
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise e