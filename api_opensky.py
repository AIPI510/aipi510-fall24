import plotly.express as px
from opensky_api import OpenSkyApi
from collections import defaultdict


def coords_to_dict():
    '''
    Gathers all of the latitudes, longitudes, and respective ICAO identifiers, counts the frequencies, 
    and records the most populated ICAO identifiers in a dictionary.

    Returns:
    dict: The frequency (value) of every unique coordinate (key) from the initial API call (coords_freqs).
    dict: The most frequent ICAO identifier (value) for every unique coordinate (key) from the initial API call (most_populated_icao).
    '''

    # The Initial API Call that gets the most up to data info on airspace information.
    api = OpenSkyApi()
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

def main():
    '''
    The main() func that contains menu functionality.
    '''
    while True:
        print("\nMenu Options:")
        print("1. Display Top 10 Most Crowded Airspaces")
        print("2. (Reserved for Future Functionality)")
        print("q. Quit")

        command = input("Enter option (1, 2, or q): ").strip().lower()
        
        if command == '1':
            print("Querying airspace data...")
            coords_freqs, most_populated_icao = coords_to_dict()
            top10_airspaces(coords_freqs, most_populated_icao)
        elif command == '2':
            print("Querying airspace data...")
            coords_freqs, most_populated_icao = coords_to_dict()
            viz_flight_density(coords_freqs)
        elif command == 'q':
            print("Quitting...")
            break
        else:
            print("Invalid input. Please enter 1, 2, or q.")

if __name__ == "__main__":
    main()