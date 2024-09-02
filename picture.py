import json
import webbrowser
import re
from datetime import datetime
import os
import requests

# Get the API key from the environment variable
API_KEY = os.getenv("NASA_API_KEY")
if not API_KEY:
    raise ValueError("No API key found. Please set the NASA_API_KEY environment variable.")

cutoff_date = datetime(1995, 6, 16) #No data exists before 6/16/1995
todays_date = datetime.now()


def get_date():
    '''
    Function to receive date input from the user. If date is not in specified format, raise an error and reprompt the user
    '''
    while True:
        date = input('Please enter in a date in the format YYYY-MM-DD. Date must be before 1995-06-16: ')
        if not re.match(r'\d{4}-\d{2}-\d{2}', date): #use regex to check date format
            print("Date is not in the correct format. Please try again.")
            continue

        try:
            input_date = datetime.strptime(date, '%Y-%m-%d') #converting string to datetime object

            if input_date < cutoff_date:
                print("Date is before June 16, 1995. Please try again.")
                continue
            if input_date > todays_date:
                print("Date is in the future. Please try again.")
                continue

            return input_date
        except ValueError:
            print("Date is not valid. Please try again.")


def fetch_apod(date):
    '''
    Function to fetch the Astronomy Picture of the Day (APOD) from the NASA API
    '''
    response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={date.strftime('%Y-%m-%d')}") 
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4)) #optional
        webbrowser.open(data['url']) #open apod image in user's default browser
    else:
        print("Failed to fetch data from NASA API")

if __name__ == "__main__":
    date = get_date()
    fetch_apod(date)