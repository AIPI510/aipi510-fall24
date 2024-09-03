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
def list_parks_in_state(state_code):
   """
   Parameters:
   - state_code (str): The state code to list parks for (e.g., 'CA' for California).
   """
   parks_df = fetch_parks_data(API_KEY, state_code=state_code)
   if parks_df is not None:
       print(f"Parks in {state_code}:")
       # Extracting the relevant information
       if 'addresses' in parks_df.columns:
           # Extract the first address
           parks_df['address'] = parks_df['addresses'].apply(lambda x: x[0]['line1'] if x else 'No address available')
       else:
           parks_df['address'] = 'No address available'
      
       # Display full name and address
       print(parks_df[['fullName', 'address']].to_string(index=False))




def find_top_states_with_most_parks(top_n=5, activity_filters=None):
   """
   Find the top N states with the most parks, filtered by multiple activities.
   Parameters:
   - top_n (int): The number of top states to display (default is 5).
   - activity_filters (list of str): A list of activities to filter parks by (e.g., ['Hiking', 'Camping']). If None, no activity filter is applied.
   """
   parks_df = fetch_parks_data(API_KEY, limit=500)
   if parks_df is not None:
       state_counts = {}
      
       # Loop through each park
       for _, park in parks_df.iterrows():
           states = park['states'].split(',')
          
           # Check if park offers all specified activities
           if activity_filters:
               activities = [activity['name'] for activity in park['activities']]
               if not all(activity in activities for activity in activity_filters):
                   continue
          
           for state in states:
               if state in state_counts:
                   state_counts[state] += 1
               else:
                   state_counts[state] = 1
      
       # Sort states by number of parks
       sorted_states = sorted(state_counts.items(), key=lambda x: x[1], reverse=True)
      
       if activity_filters:
           print(f"Top {top_n} states with the most parks offering {', '.join(activity_filters)}:")
       else:
           print(f"Top {top_n} states with the most parks:")
      
       for state, count in sorted_states[:top_n]:
           print(f"{state}: {count} parks")


def find_parks_by_activity_and_state(activity, state_code):
   """
   Find parks in a specific state that offer a certain activity


   Parameters:
   - activity (str): The activity to search for (e.g., 'Camping').
   - state_code (str): The state code to filter parks by (e.g., 'CA' for California).
   """
   parks_df = fetch_parks_data(API_KEY, state_code=state_code, limit=100)
   if parks_df is not None:
       matching_parks = []
      
       # Loop through each park to check for the activity
       for _, park in parks_df.iterrows():
           activities = [activity['name'] for activity in park['activities']]
           if activity in activities:
               matching_parks.append(park)
      
       if matching_parks:
           print(f"Parks in {state_code} offering {activity}:")
           for park in matching_parks:
               print(park['fullName'])
       else:
           print(f"No parks found in {state_code} offering {activity}.")

  
if __name__ == "__main__":
    # Provide user guidance
    print("Welcome to the National Parks Explorer!")
    print("To use this script, refer to the following lists for valid inputs:")
    print()

    # Display the valid state codes and available activities
    state_codes = list_valid_state_codes()
    activities = fetch_activities(API_KEY)

    # Interactive User Input
    while True:
        print("\nWhat would you like to do?")
        print("1. List parks in a specific state")
        print("2. Find top states with the most parks offering certain activities")
        print("3. Find parks by activity and state")
        print("4. Exit")

        choice = input("Enter the number of your choice: ")
        
        if choice == '1':
            state_code = input("Enter the state code (e.g., 'CA' for California): ").upper()
            if state_code in state_codes:
                list_parks_in_state(state_code)
            else:
                print("Invalid state code. Please try again.")
        
        elif choice == '2':
            top_n = int(input("How many top states would you like to see? "))
            activity_filters = input("Enter a comma-separated list of activities (e.g., 'Camping,Hiking'): ").split(',')
            activity_filters = [activity.strip() for activity in activity_filters if activity.strip() in activities]
            find_top_states_with_most_parks(top_n=top_n, activity_filters=activity_filters)
        
        elif choice == '3':
            activity = input("Enter the activity (e.g., 'Camping'): ").strip()
            state_code = input("Enter the state code (e.g., 'CA' for California): ").upper()
            if state_code in state_codes and activity in activities:
                find_parks_by_activity_and_state(activity, state_code)
            else:
                print("Invalid state code or activity. Please try again.")
        
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")