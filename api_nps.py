import requests
import pandas as pd

## parts of this code were modified and corrected using ChatGPT 

API_KEY = 'TjzlabAhf8XiHava2sY1ohVfxekIvM1OnWnyel8g'
BASE_URL = 'https://developer.nps.gov/api/v1/parks'
ACTIVITIES_URL = 'https://developer.nps.gov/api/v1/activities'

def fetch_parks_data(api_key, state_code=None, limit=100):
    """
    Fetch park data from the NPS API.
    Parameters: 
    - state_code (str): The state code to filter parks by (e.g., 'CA' for California).
    - limit (int): The maximum number of parks to retrieve (default is 100).
    
    """
    params = {
        'api_key': api_key,
        'limit': limit
    }
    if state_code:
        params['stateCode'] = state_code
    
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return pd.json_normalize(response.json()['data'])
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

