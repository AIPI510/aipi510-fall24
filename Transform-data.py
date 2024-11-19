import json

def lambda_handler(event, context):
    # TODO implement
    
    data = event['body']
    
    try:
        
        # Transform data by adding 'processed' field
        transformed_data = [
            {**item, "processed": True} if isinstance(item, dict) else {"value": item, "processed": True}
            for item in data
        ]
        
        return {
            'statusCode': 200,
            'body': transformed_data
        }
    
    except Exception as e:
        print(f"Error transforming data: {str(e)}")
        print(f"Input data: {data}")

        raise e