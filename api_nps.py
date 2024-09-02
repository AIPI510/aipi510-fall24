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


def list_valid_state_codes():
   """   
   Returns:
   - List of state codes.
   """
   state_codes = [
       'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
       'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
       'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
       'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
       'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
   ]
   print("Valid U.S. State Codes:")
   print(", ".join(state_codes))
   return state_codes


def fetch_activities(api_key):
   """
   Returns:
   - List of activity names.
   """
   params = {
       'api_key': api_key
   }
   response = requests.get(ACTIVITIES_URL, params=params)
   if response.status_code == 200:
       activities = response.json()['data']
       activity_names = [activity['name'] for activity in activities]
       print("Available Activities:")
       print(", ".join(activity_names))
       return activity_names
   else:
       print(f"Failed to fetch activities. Status code: {response.status_code}")
       return []
