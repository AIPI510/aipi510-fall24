import requests
import argparse
import json


def search_channel(search_query):
    
    # Replace these variables with .env information 
    client_id = "##client_id here##"
     
    client_secret = "##client_secret here##"

    # Acquire an access token to use further
    # This can be done by performing an API call with the below url
    url = 'https://id.twitch.tv/oauth2/token'

    # Use this payload as the parameters
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }

    # Make the APi call
    response = requests.post(url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    # If the response fails, print the error message
    if response.status_code != 200:
        return "Request Failed. Please check your access codes."

    # Get the access token
    parsed_response = response.json()

    access_token = parsed_response.get('access_token')

    # check if the access token exists
    if not access_token:
        return("There seems to be a problem with the access token. Please try again.")

    # Now we will call the channel query, using the user's given argument
    url = 'https://api.twitch.tv/helix/search/channels'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Client-ID': client_id
    }
    params = {
        'query': search_query
    }

    # Make the GET request
    response = requests.get(url, headers=headers, params=params)

    # if the response fails
    if response.status_code != 200:
        return "Channel Request Failed. Please try again"
    
    response_json = response.json()

    # Get only the live channels
    live_channels = [channel for channel in response_json.get('data', []) if channel.get('is_live')]

    # Return a well-formatted JSON string
    return json.dumps({'live_channels': live_channels}, indent=4)

def main():
    # Adds an argument parser to allow the user to paste their search_term directly on the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("search_query", type=str)
    args = parser.parse_args()

    # Make the user search the channel result
    result = search_channel(args.search_query)
    if result:
        print(result)

if __name__ == "__main__":
    main()

