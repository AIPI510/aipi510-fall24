import json

def lambda_handler(event, context):
    """
    Lambda function to transform the extracted Arxiver dataset data.
    Args:
        event: Input data passed from the previous Lambda function.
        context: AWS Lambda context object.
    Returns:
        dict: Transformed data.
    """
    # Extract data from the event object
    if 'body' in event:
        data = json.loads(event['body'])
    else:
        data = event
    
    # Ensure data is a list of dictionaries
    if isinstance(data, str):
        data = json.loads(data)
    elif isinstance(data, dict):
        data = [data]
    
    # Perform data cleaning and formatting on the Arxiver dataset
    transformed_data = []
    for item in data:
        if isinstance(item, dict):
            transformed_item = {
                'arxiv_id': item.get('id', '').strip(),
                'title': item.get('title', '').strip(),
                'abstract': item.get('abstract', '').strip(),
                'authors': [author.strip() for author in item.get('authors', [])],
                'publication_date': item.get('publication_date', '').strip(),
                'url': item.get('url', '').strip(),
                'markdown_content': item.get('markdown_content', '').strip()
            }
            transformed_data.append(transformed_item)
    
    # Return transformed data
    return {
        'statusCode': 200,
        'body': json.dumps({'transformed_data': transformed_data})
    }
