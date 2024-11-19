import json
import urllib.request

def lambda_handler(event, context):
    try:
        # URL to fetch data
        url = "https://fingertips.phe.org.uk/api/all_data/csv/for_one_indicator?indicator_id=93505"

        # Fetch the data
        response = urllib.request.urlopen(url)
        if response.getcode() == 200:
            data = response.read().decode('utf-8')[:100000]  # Limit the payload size
            print("Successfully fetched data")
            
            # Return data for the Step Function
            return {
                'statusCode': 200,
                'body': data
            }
        else:
            print(f"Error: API request failed with code: {response.getcode()}")
            return {
                'statusCode': response.getcode(),
                'body': json.dumps({"error": "API request failed"})
            }
    except Exception as e:
        print(f"Exception occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }