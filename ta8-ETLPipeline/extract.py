import requests
import json

def lambda_handler(event, context):
    """
    Extracts user data from an external API and returns it in JSON format.

    Args:
        event (dict): Event data passed by Step Functions.
        context (object): Lambda context object.

    Returns:
        dict: Response containing status code and fetched user data or an error.
    """
    # API endpoint for fetching user data
    api_url = "https://jsonplaceholder.typicode.com/users"
    
    try:
        # Fetch data from the API
        print(f"Fetching data from API: {api_url}")
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the JSON response
        data = response.json()
        print("Successfully fetched data:", data)
        
        # Return the fetched data
        return {
            "statusCode": 200,
            "body": data
        }
    
    except requests.exceptions.RequestException as e:
        # Handle any errors during the API call
        print(f"Error fetching data from API: {e}")
        return {
            "statusCode": 500,
            "error": str(e)
        }
