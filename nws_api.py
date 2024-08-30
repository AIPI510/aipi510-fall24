import streamlit as st
import pandas as pd 
import numpy as np

# @todo: bring this utility code into this file, the assignment seems to imply we should
# only be merging nws_api.py
import weather
import time 

geo:weather.IPGeo = None
forecast:weather.Forecast = None

# NB (from Streamlit docs): 
# Whenever a callback is passed to a widget via the on_change (or on_click) parameter, 
# the callback will always run before the rest of your script. For details on the Callbacks
# API, please refer to our Session State API Reference Guide.
#
st.write('Hello!')

def display_table(): 
    """

    Built w/ help from the Streamlit fundamentals docs: 
    https://docs.streamlit.io/get-started/fundamentals/main-concepts
    """
    dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

    st.dataframe(dataframe.style.highlight_max(axis=0))
    
    # static (non-interactive) table... 
    #st.table(dataframe)

def display_map(): 
    """ 
    Render the map!

    Built with help from the streamlit map quickstart: 
    https://docs.streamlit.io/develop/api-reference/charts/st.map
    """
    df = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=["lat", "lon"],
    )
    st.map(df, size=20, color="#0044ff")


@st.cache_data
def get_location(): 
    return weather.IPGeo()

@st.cache_data
def get_forecast(lat, lon): 
    forecast = weather.Forecast()
    forecast.resolve_location(lat, lon)     
    forecast.update_forecast()

    return forecast

display_table()

geo = get_location() 
forecast = get_forecast(geo.lat, geo.lon)

st.write(geo.lat, geo.lon)
display_map()