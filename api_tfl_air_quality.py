"""This script is used to get the dataset on air quailty by utilizing the AirQuality API from TfL Unified APIs.
This dataset is updated hourly.This dataset contains the air quality forecast for the next few days, 
including the following information: $id, $type, forecastType, forecastID, toDate, forecastBand, forecastSummary, 
nO2Band, o3Band, pM10Band, pM25Band, sO2Band, forecastText. Then the data is stored in a pandas dataframe and printed.
"""

#import the necessary libraries
import urllib.request, json
import pandas as pd

#
try:
    # Define the API request URL for AirQuality data from TfL (Transport for London)
    url = "https://api.tfl.gov.uk/AirQuality/"

    hdr ={
    # Request headers
    'Cache-Control': 'no-cache',
    }
    # create a request object
    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    
    # read and decode the response data
    response_data = response.read().decode('utf-8')

    # Parse the json data from the decoded response string
    data = json.loads(response_data)

    # # Extract the "currentForecast" section from the parsed JSON data
    forecast_data = data['currentForecast']

    # convert the "currentForecast" data into a pandas DataFrame 
    df = pd.DataFrame(forecast_data)

    # print the resulting DataFrame then save it to a csv file
    print(df)
    df.to_csv('air_quality_forecast.csv', index=False)


# Print any errors that occur during the process
except Exception as e:
    print(e)

