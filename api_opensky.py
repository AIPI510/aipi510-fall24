import sys
from opensky_api import OpenSkyApi

def coords_to_dict():
    api = OpenSkyApi()
    states = api.get_states()

    coords_freqs = {}
    for state in states.states:
        if state.latitude is not None and state.longitude is not None:
            latitude_cell = int(state.latitude)
            longitude_cell = int(state.longitude)

            cell = (latitude_cell, longitude_cell)
            if cell in coords_freqs:
                coords_freqs[cell] += 1
            else:
                coords_freqs[cell] = 1

    return coords_freqs

def top10_airspaces(coords_freqs):
    sorted_by_values = dict(sorted(coords_freqs.items(), key=lambda item: item[1], reverse=True)[:10])
    for cell, freq in sorted_by_values.items():
        print(f"Cell: {cell}, Frequency: {freq}")

def main():
    coords_freqs = coords_to_dict()
    top10_airspaces(coords_freqs)
        
if __name__ == "__main__":
    main()