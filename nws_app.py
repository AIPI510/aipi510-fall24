import streamlit as st
import pandas as pd 
import numpy as np
import pydeck as pdk
import time
import requests

from nws_api import Forecast, IPGeo

# Streamlit application basics courtesy of https://docs.streamlit.io/get-started/fundamentals/main-concepts
#
# NB (from Streamlit docs): 
# Whenever a callback is passed to a widget via the on_change (or on_click) parameter, 
# the callback will always run before the rest of your script. For details on the Callbacks
# API, please refer to our Session State API Reference Guide.
#
def display_chart(df, column): 
    """
    
    """
    #st.dataframe(df)
    st.bar_chart(df, y=column)

def display_station_map(df): 
    """ 
    Render the map!

    Built with help from the streamlit map quickstart: 
    https://docs.streamlit.io/develop/api-reference/charts/st.map
    """
    st.map(df, size=60, color="#0044ff")

# todo: fix this to render temperatures or something on the map with a color ramp
def display_observation_map(df): 
    """ 
    Render the map!
    """
    st.map(df, size=20, color="#0044ff")

def fetch_forecast_data(url):
    """
    get the forecast data given url
    input: url
    output: json
    """
    response = requests.get(url)
    response.raise_for_status()  
    return response.json()  

def parse_forecast_json(json_data):
    """parse the data into df suitable for plotting
    input: json
    output: pandas df"""
    periods = json_data['properties']['periods']
    data = []
    for period in periods:
        farenheight = period['temperature']
        celsius = (farenheight - 32) * (5.0/9.0)
        data.append({
            'time': pd.to_datetime(period['startTime']),
            'temperature': celsius
        })
    
    df = pd.DataFrame(data)
    df.set_index('time', inplace=True)
    return df

def temp_graph(df):
    st.line_chart(df['temperature'])

@st.cache_data
def get_location(): 
    return IPGeo()

@st.cache_data
def get_forecast(lat, lon): 
    forecast = Forecast()
    forecast.resolve_location(lat, lon)   
    return forecast

@st.cache_data
def get_stations(_forecast):
    return forecast.retrieve_serving_stations()

@st.cache_data
def get_observations(_forecast, stations):
    return forecast.retrieve_observations(stations)

def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)

@st.cache_data
def stream(text): 
    st.write_stream(stream_data(text))

st.title('☀️ National Weather Service API')
stream('This app demonstrates interactions with the more interesting endpoints of the [NWS API](https://www.weather.gov/documentation/services-web-api).')
st.divider()

geo = get_location() 

stations = None
stream(f'Your IP locates you in **{geo.city}, {geo.state}**')

col1, col2 = st.columns(2) 
lat = None
lon = None

with col1: 
    lat = st.text_input("Latitude", F"{geo.lat}")

with col2: 
    lon = st.text_input("Longitude", F"{geo.lon}")

stream(":information_source: *We'll retrieve weather information for the provided coordinates. Alternative coordinates can be obtained from [Google Maps](https://www.google.com/maps) by right-clicking on the map and selecting the coordinates to copy.*")

if 'button1' not in st.session_state:
    st.session_state.button1 = False
    st.session_state.button2 = False
    st.session_state.button3 = False
    st.session_state.button4 = False

def click_button1():
    st.session_state.button1 = True

def click_button2():
    st.session_state.button2 = True

def click_button3():
    st.session_state.button3 = True

def click_button4():
    st.session_state.button4 = True

forecast = None
st.subheader(":office: Serving NWS Office")
stream("To retrieve forecast information, we must first find the NWS office that services your location. The NWS offices each have a regional responsibility as outlined in the below image.")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/NWS_Weather_Forecast_Offices.svg/1920px-NWS_Weather_Forecast_Offices.svg.png", caption="NWS Regional Offices")       
stream("Click below find locate the office associated with your coordinates.")
st.button("Fetch office...", on_click=click_button1)

if st.session_state.button1: 
    forecast = get_forecast(lat, lon)
    stream(f'Weather forecasts for {lat} {lon} are provided by the NWS **{forecast.office}** office, located in **{forecast.location}**.')

    st.subheader(":satellite: Regional Weather Stations")
    stream("Forecast information for this area is sourced from numerous regional weather stations, click below to retrieve the locations.")

    st.button("Fetch stations...", on_click=click_button2)
    if st.session_state.button2: 
        stream(f'Weather stations that contribute to the forecasts the NWS sources for your area are plotted below.')
        stations = get_stations(forecast)
        display_station_map(stations)

        st.subheader('Serving Weather Stations')
        stream("Each weather station sources its own observations, which we can poll through the API...")
        st.write("")
        stream("Click the button below to retrieve current observations from the serving weather stations.") 

        st.button("Retrieve weather stations", on_click=click_button3)
        if st.session_state.button3: 
            st.subheader('Current observations')
            observations = get_observations(forecast, stations['station'])
            
            # @todo, this isn't right... we need to display a map 
            display_chart(observations, 'temp')

            # @todo: render some time series data from teh get_forecast method which I think is brokwn at the moment
            stream("Click the button to see temperature forecast data for your local station.")

            st.subheader("🌡️ Temperature forecast")
            st.button("Get forecast", on_click=click_button4)
            if st.session_state.button4:
                forecast_url = forecast.data['forecastHourly']  
                forecast_json = fetch_forecast_data(forecast_url)
                tempdata = parse_forecast_json(forecast_json)
                temp_graph(tempdata)
                
                st.subheader("Developer Notes")
                
                
                stream("The NWS API is documented with an OpenAPI UI [here](), however it's use is not straightforward. The most intuitive way\
                    to learn about the API is to visit the [Point Forecast site](https://www.weather.gov/forecastpoints/) and click around \
                    with your browser's developer tools turned on [and monitoring the network traffic](https://developer.chrome.com/docs/devtools/network).")
        