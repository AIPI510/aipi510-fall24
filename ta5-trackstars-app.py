                    
import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time

# Streamlit  basics courtesy of https://docs.streamlit.io/get-started/fundamentals/main-concepts
#
# NB (from Streamlit docs): 
# Whenever a callback is passed to a widget via the on_change (or on_click) parameter, 
# the callback will always run before the rest of your script. For details on the Callbacks
# API, please refer to our Session State API Reference Guide.
#
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.0)

@st.cache_data
def stream(text): 
    st.write_stream(stream_data(text))

def load_rainfall(path):
    """
    Fetch and preprocess the rainfall data
    """
    df = pd.read_csv(path)

    # The data is pretty ratty earlier than 1888
    df = df[df['YEAR']>1887]
    months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'] 
    for month in months: 
        df[month] = pd.to_numeric(df[month])
    
    return df

def load_river_crests(path):
    """
    Fetch and preprocess river crests/height data
    """
    df = pd.read_csv(path) 

    flood_categories = {
        'major' : 18, 
        'moderate' : 13, 
        'minor' : 9.5, 
        'action' : 6.5
    }

    def categorize_crests(level): 
        """
        Assign flood categories based on water level
        """
        for category, height in flood_categories.items(): 
            if level >= height: 
                return category

    df['Category'] = df['Level'].apply(categorize_crests)

    return df

def plot_river_height(df): 
    """
    Generate a plot of river heights provided a dataframe that includes expected 
    columns (Level, Year)
    """
    df_major = df[df['Category'] == 'major']
    df_moderate = df[df['Category'] == 'moderate']
    df_minor = df[df['Category'] == 'minor']

    decades = range(1888, 2024, 5) 

    fig = plt.figure(figsize=[10,3])
    
    plt.bar(df_major['Year'], df_major['Level'],label='Major Flood Event', align='center', color='lightcoral')
    plt.bar(df_moderate['Year'], df_moderate['Level'], label='Moderate Flood Event', color='orange')
    plt.bar(df_minor['Year'], df_minor['Level'], label='Minor Flood Event', align='edge', color='khaki')
    plt.xlabel("Year") 
    plt.xticks(decades, rotation=90)
    plt.ylabel("River Crest (Feet)")
    plt.title("French Broad River Height, Flood Events, 1888-2023") 
    _ = plt.legend()
    
    # Critical insight on using the streamlit global pyplot instance to render pyplot-style charts
    # from https://discuss.streamlit.io/t/how-to-display-matplotlib-graphs-in-streamlit-application/35383/2
    st.pyplot(fig) 

# Buttons for *things* 
if 'button0' not in st.session_state:
    st.session_state.button0 = False
    st.session_state.button1 = False
    st.session_state.button2 = False
    st.session_state.button3 = False
    st.session_state.button4 = False

def click_button0():
    st.session_state.button0 = True

def click_button1():
    st.session_state.button1 = True

def click_button2():
    st.session_state.button2 = True

def click_button3():
    st.session_state.button3 = True

def click_button4():
    st.session_state.button4 = True

st.title('🧪 Bayes Theorem Introduction')
stream('This app provides a loose introduction to Bayes theorem by way of a real-world example.')

st.button("Continue...", on_click=click_button0)

if st.session_state.button0: 

    st.subheader("Frequentist vs Bayesian Statistics")
    stream("It might be interesting to talk for a second about frequentist vs bayesian approaches to probability estimation.") 
    stream("Bayes theorem is often illustrated with an example where our belief about rain is adjusted based on the fact it's cloudy. This example is sort of unhelpful as we usually have so much in the way of historicals, that we can go the frequentist approach and just directly estimate the probability of rain based our long history of observations. Using a bayesian update technique in this case seems impractical, and indeed throws out a lot of data that you could use.") 
    stream("However, many situations do not have rich historicals to draw estimates from, or might be deviate wildly from the historicals, and either of these cases would be inferior to a bayesian approach that is really at its heart about trying to perpetually contextualize new observations")

    df = load_rainfall('avl_rainfall.csv')
    df2 = load_river_crests('avl_crests.csv')

    plot_river_height(df2)

    stream("Probability of a major flood event (shown in red) is:")
    st.latex("p_{flood} = {\\dfrac{events}{years}}") 
    st.latex("p_{flood} = {\\dfrac{2}{2024-1888}}")
    st.latex("p_{flood} \\approx{0.014}")

    p_maj_flood = 2/(2024 - 1888)
    p_mod_flood = 6/(2025-1888) 
    p_flood = p_maj_flood + p_mod_flood 

    stream(f"The probability of a major flood event in Asheville, NC based on historical events, prior to 2024 is ~= {p_maj_flood:.2}")
    stream(f"The probability of a moderate flood event in Asheville, NC based on historical events, prior to 2024 is ~= {p_mod_flood:.2}")

# ")

# --- 
    # stream("Click below find locate the office associated with your coordinates.")
    # st.button("Fetch office...", on_click=click_button1)

    # if st.session_state.button1: 
    #     forecast = get_forecast(lat, lon)
    #     stream(f'Weather forecasts for {lat} {lon} are provided by the NWS **{forecast.office}** office, located in **{forecast.location}**.')

    #     st.subheader("🌡️ Temperature forecast")
    #     stream(f'Click the button to see temperature forecast data for your local office.')
    #     st.button("Get forecast...", on_click=click_button2)
    #     if st.session_state.button2:
    #         tempdata = get_hourly_forecast(forecast)
    #         temp_graph = display_temp_graph(tempdata)

    #         st.subheader(":satellite: Regional Weather Stations")
    #         stream(f"Forecast information for **{forecast.location}** is sourced from numerous regional weather stations, click below to retrieve the locations.")

    #         st.button("Fetch stations...", on_click=click_button3)
    #         if st.session_state.button3: 
    #             stream(f'Weather stations that contribute to the forecasts the NWS sources for **{forecast.location}** are plotted below.')
    #             stations = get_stations(forecast)
    #             station_map = display_station_map2(stations)

    #             st.subheader('🔭 Weather Stations Observations')
    #             stream("Each weather station sources its own observations, which we can poll through the API...")
    #             st.write("")
    #             stream("Click the button below to retrieve current observations from the serving weather stations.") 

    #             st.button("Retrieve observations...", on_click=click_button4)
    #             if st.session_state.button4: 
    #                 stream('**Current temperatures by reporting station**')
    #                 observations = get_observations(forecast, stations['station'])

    #                 merged = stations.merge(observations, on='station', how='inner')
    #                 temp_map = display_station_temps(merged)
            
    #                 st.subheader("Developer Notes")
    #                 stream("The NWS API is documented with an OpenAPI UI [here](https://www.weather.gov/documentation/services-web-api), however it's use is not straightforward. The most intuitive way\
    #                     to learn about the API is to visit the [Point Forecast site](https://www.weather.gov/forecastpoints/) and click around \
    #                     with your browser's developer tools turned on [and monitoring the network traffic](https://developer.chrome.com/docs/devtools/network).")