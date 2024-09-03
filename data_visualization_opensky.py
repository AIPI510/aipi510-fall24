import plotly.express as px
import plotly.graph_objs as go
from opensky_api import OpenSkyApi
from collections import defaultdict
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import plotly.graph_objs as go
from opensky_api import OpenSkyApi
from collections import defaultdict
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, State

api = OpenSkyApi()

def coords_to_dict():
    '''
    Gathers all of the latitudes, longitudes, and respective ICAO identifiers, counts the frequencies, 
    and records the most populated ICAO identifiers in a dictionary.

    Returns:
    dict: The frequency (value) of every unique coordinate (key) from the initial API call (coords_freqs).
    dict: The most frequent ICAO identifier (value) for every unique coordinate (key) from the initial API call (most_populated_icao).
    '''

    # The Initial API Call that gets the most up to data info on airspace information.
    states = api.get_states()

    coords_freqs = {}

    # Decided to use a defaultdict() due to the fact that non-existent keys would default to 0, in the chance a KeyError occurs.
    icao_counts = defaultdict(lambda: defaultdict(int))  

    # Loops through all of the states, checks if there is a latitude and longitude, and then computes the frequencies of the coords 
    # and ICAO identifiers.
    for state in states.states:
        if state.latitude is not None and state.longitude is not None:
            latitude_cell = int(state.latitude)
            longitude_cell = int(state.longitude)

            cell = (latitude_cell, longitude_cell)
            if cell in coords_freqs:
                coords_freqs[cell] += 1
                icao_counts[cell][state.icao24] += 1
            else:
                coords_freqs[cell] = 1
                icao_counts[cell][state.icao24] = 1

    # Finds the most frequent ICAO identifier for each cell
    # OpenAI. (2024). ChatGPT (GPT-4) [Large language model]. Retrieved [September 1st, 2024], from https://chat.openai.com/
    most_populated_icao = {cell: max(icao_counts[cell], key=icao_counts[cell].get, default="N/A") for cell in coords_freqs}
    return coords_freqs, most_populated_icao

def top10_airspaces(coords_freqs, most_populated_icao):
    '''
    Records the top 10 most populated airspaces by ICAO identifier in a dictionary.

    Params:
    coords_freqs (dict): The frequency (value) of every unique coordinate (key) from the initial API call.
    most_populated_icao (dict): The most frequent ICAO identifier (value) for every unique coordinate (key) from the initial API call.
    '''

    # Sorts and slices the top 10 coords!
    sorted_by_values = dict(sorted(coords_freqs.items(), key=lambda item: item[1], reverse=True)[:10])
    
    # Prints the top 10 crowded airspaces by getting the most populated ICAO identifier for each of the sorted values cells.
    for cell, freq in sorted_by_values.items():
        icao_id = most_populated_icao.get(cell, "N/A")
        print(f"Cell: {cell}, Frequency: {freq}, Most Populated ICAO Identifier: {icao_id}")
    print("-------------------------------------------")

    viz_top10(sorted_by_values, most_populated_icao)

def viz_top10(sorted_by_values, most_populated_icao):
    '''
    Visualizes the top 10 most populated airspaces by ICAO identifier in a dictionary on a world map (plotly).

    Params:
    sorted_by_values (dict): The top 10 most frequent coords, with frequency (value) and unique coordinate (key).
    most_populated_icao (dict): The most frequent ICAO identifier (value) for every unique coordinate (key) from the initial API call.
    '''

    # Prepares the data for plotting.
    latitudes = [lat for lat, lon in sorted_by_values.keys()]
    longitudes = [lon for lat, lon in sorted_by_values.keys()]
    frequencies = list(sorted_by_values.values())

    # Formats info that shows up when the Mouse hovers over a point on the map.
    # OpenAI. (2024). ChatGPT (GPT-4) [Large language model]. Retrieved [September 2nd, 2024], from https://chat.openai.com/
    hover_info = [f"({lat}, {lon})<br>ICAO Identifier: {most_populated_icao.get((lat, lon), 'N/A')}" for lat, lon in sorted_by_values.keys()]

    # Creates a geographical scatter plot on a world map using Plotly.
    fig = px.scatter_geo(
        lat=latitudes,
        lon=longitudes,
        size=frequencies,
        color=frequencies,
        hover_name=hover_info,
        size_max=15,
        color_continuous_scale="Viridis",
        title="Top 10 Most Crowded Airspaces (Live)",
        projection="natural earth"
    )

    # Formats certain properties of the world map.
    fig.update_geos(
        showcountries=True, countrycolor="Black",
        showcoastlines=True, coastlinecolor="Blue",
        showland=True, landcolor="LightGreen"
    )

    fig.show()

def viz_flight_density(coords_freqs):
    '''
    Visualizes the flight density of every unique airspace based on all recorded coords.

    Params:
    coords_freqs (dict): The frequency (value) of every unique coordinate (key) from the initial API call.
    '''

    # Prepares data for plotting.
    latitudes = [lat for lat, lon in coords_freqs.keys()]
    longitudes = [lon for lat, lon in coords_freqs.keys()]
    frequencies = list(coords_freqs.values())

    # Creates a heat map using Plotly.
    fig = px.density_mapbox(
        lat=latitudes,
        lon=longitudes,
        z=frequencies,
        radius=10,
        center=dict(lat=0, lon=0),
        zoom=1,
        mapbox_style="stamen-terrain", # Formats the heatmap as visually geographical
        title="Flight Density Map"
    )

    fig.show()

    
# Define inputs and outputs for the application using component IDs as well as State to keep track of zoom and/or pan state of the plot for each update
@callback(
    Output('graph', 'figure'),
    Input('interval', 'n_intervals'),
    State('graph', 'relayoutData')
)

# Define the graph update function
def update_graph(n, relayoutData):
    '''
    This function calls the OpenSky API to retrieve the latest plane positions in the US.
    Every 10 seconds, this callback method is executed as the input defined above triggers the callback.

    In addition, the relayoutData parameter is used to retain the zoom and pan of the plot upon each update,
    therefore that is also passed into this function

    Args:
        n (int): number of 10 second intervals since inception
        relayoutData: current zoom and/or pan settings of user

    Returns:
        plotly.graph_objects.Figure: plot of all live flights in the US

    '''        
    # API call
    state_vectors = api.get_states(bbox=(20, 50, -126, -65))

    # Organize and store pertinent data
    times, icao_codes, callsigns, latitudes, longitudes = [], [], [], [], []
    for state in state_vectors.states:
        icao_codes.append(state.icao24)
        times.append(state.time_position)
        callsigns.append(state.callsign)
        latitudes.append(state.latitude)
        longitudes.append(state.longitude)

    temp_dict = {
        'time' : times,
        'icao24' : icao_codes,
        'callsign' : callsigns,
        'latitude' : latitudes,
        'longitude' : longitudes
    }

    # Convert collected data to dataframe
    flights_df = pd.DataFrame.from_dict(temp_dict)

    # Create a scatter plot of the US map using the dataframe
    fig = px.scatter_geo(flights_df,
                    lat='latitude',
                    lon='longitude',
                    hover_data=['callsign', 'icao24'],
                    scope='usa')
    
    fig.update(layout_coloraxis_showscale=False)

    # Check if zoom and/or pan data was provided and update the layout accordingly
    if relayoutData:
        fig.update_layout(relayoutData)

    return fig

# This callback method is used to handle click events where the clickData stores what details the user has clicked on
@callback(
    Input('graph', 'clickData')
)
def handle_click(clickData):
    '''
    This function handles click events and generates a plot showing the flight path of the flight that was clicked on and its current location

    Args:
        clickData (dict): stores information regarding the data point that was clicked by the user

    Returns:
        plotly.graph_objects.Figure: plot of flight path for selected flight
    
    '''
    # Extract ICAO24 code from the clicked data supplied to the function
    clicked_flight_icao24 = clickData['points'][0]['customdata'][1]

    # API call to retrieve flight path data
    flight_tracker = api.get_track_by_aircraft(clicked_flight_icao24)

    # Convert to dataframe
    flight_path_df = pd.DataFrame(flight_tracker.path, columns=["time", "latitude", "longitude", "baro_altitude", "true_track", "on_ground"])

    # Create a geographical line plot
    fig = px.line_geo(flight_path_df, 
                    lat='latitude',
                    lon='longitude',
                    scope='usa')

    # Display current position as a red dot
    fig.add_trace(go.Scattergeo(
        lat=[flight_path_df['latitude'].to_list()[-1]],
        lon=[flight_path_df['longitude'].to_list()[-1]],
        mode = 'markers',
        marker = {'color':'red', 'size':14},
        showlegend = False,
    ))
    
    fig.update(layout_coloraxis_showscale=False)
    fig.show()

def main():
    '''
    The main() func that contains menu functionality.
    ''' 

    # Initialize Dash application
    app = Dash()

    # Setup User Interface layout of Dash application
    app.layout = html.Div([
        html.H1(children="Flight Tracker", style={'textAlign':'center'}),
        dcc.Graph(id='graph', style={'width' : '100vw', 'height' : '100vh'}),
        dcc.Interval(
            id='interval',
            interval=15*1000,
            n_intervals=0
        ),
    ])

    while True:
        print("\nMenu Options:")
        print("1. Display Top 10 Most Crowded Airspaces")
        print("2. Display Heatmap of Flight Density")
        print("3. Run Live Flight Tracker Web Application")
        print("q. Quit")

        command = input("Enter option (1, 2, 3, or q): ").strip().lower()
        
        if command == '1':
            print("Querying airspace data...")
            coords_freqs, most_populated_icao = coords_to_dict()
            top10_airspaces(coords_freqs, most_populated_icao)
        elif command == '2':
            print("Querying airspace data...")
            coords_freqs, most_populated_icao = coords_to_dict()
            viz_flight_density(coords_freqs)
        elif command == '3':
            print("Running Live Flight Tracker...")
            print("Click on planes to display their flight path\n")
            print("Use Ctrl+C to stop the live tracker")
            break  
        elif command == 'q':
            print("Quitting...")
            exit(0)
        else:
            print("Invalid input. Please enter 1, 2, or q.")

    app.run_server(debug=True, use_reloader=False)

if __name__ == "__main__":
    main()
