"""
This script retrieves earthquake data from the USGS Earthquake Hazards Program 
API (https://earthquake.usgs.gov/fdsnws/event/1/) based on a provided zipcode 
and search parameters. Search parameters include the radius, start date, end 
date, minimum magnitude, and maximum magnitude. Earthquake data returned by the 
query is distilled into desired information and printed to the console.
"""
import argparse
import datetime

import numpy as np
import pgeocode
import requests

from dataclasses import dataclass

# dataclass to store desired earthquake information
@dataclass
class Earthquake:
    magnitude: float
    place: str  
    time: str
    latitude: float   
    longitude: float
    depth: float

def print_earthquake_data(earthquakes: list[Earthquake]) -> None:
    """
    Prints earthquake data.
    
    Args:
        earthquakes (list): A list of Earthquake objects.
    Returns:
        None
    """
    for earthquake in earthquakes:
        print(earthquake.place)
        print(f"\tMagnitude: {earthquake.magnitude}")
        print(f"\tTime: {earthquake.time} UTC")
        print(f"\tLocation: {earthquake.latitude}, {earthquake.longitude}")
        print(f"\tDepth: {earthquake.depth} km")


def distill_earthquake_data(raw_earthquake_data: dict) -> list[Earthquake]:
    """
    Extracts desired information from raw earthquake data and returns a list of Earthquake objects.
    
    Args:
        raw_earthquake_data (dict): A dictionary containing raw earthquake data. Example raw JSON data: 
            https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-02
    
    Returns:
        list[Earthquake]: A list of Earthquake objects containing the distilled information.
    """
    earthquakes = []

    # Extract desired information from the raw earthquake data
    for feature in raw_earthquake_data["features"]:
        magnitude = feature["properties"]["mag"]
        place = feature["properties"]["place"]

        # For the sake of simplicity, assume the time zone is UTC
        # None of the results observed included a timezone, which means UTC
        dt = datetime.datetime.fromtimestamp(feature["properties"]["time"] / 1000, datetime.timezone.utc)
        time = dt.strftime("%Y-%m-%d %H:%M:%S")
        
        latitude = feature["geometry"]["coordinates"][1]
        longitude = feature["geometry"]["coordinates"][0]
        depth = feature["geometry"]["coordinates"][2]
        earthquakes.append(Earthquake(magnitude, place, time, latitude, longitude, depth))
    
    return earthquakes


def is_validate_date(date_text: str) -> bool:
    """
    Validates if the given date is in the format YYYY-MM-DD.
    
    Args:
        date_text (str): The date to be validated.
    
    Returns:
        bool: True if the date is in the correct format, False otherwise.
    """
    try:
        datetime.date.fromisoformat(date_text)
    except ValueError:
        print("Incorrect date format, please use YYYY-MM-DD")
        return False
    
    return True


def get_latlong_from_zipcode(zipcode: str) -> tuple:# -> tuple[Any | Series[Any], Any | Series[Any]]:
    """
    Retrieves the latitude and longitude coordinates for a given zipcode.
    
    Args:
        zipcode (str): The zipcode for which to retrieve the coordinates.
   
     Returns:
        tuple: A tuple containing the latitude and longitude coordinates.

    Example:
        >>> get_latlong_from_zipcode("90210")
        (34.103, -118.416)
    """
    nomi = pgeocode.Nominatim("us")
    location = nomi.query_postal_code(zipcode)
    return location.latitude, location.longitude


def get_earthquake_data(args: argparse.Namespace) -> dict:
    """
    Retrieves earthquake data based on the provided arguments.
    
    Args:
        args (argparse.Namespace): The command-line arguments parsed using argparse.
    
    Returns:
        dict: A dictionary containing the earthquake data.
    """
    earthquake_data = {}

    # Convert ZIP code to latitude and longitude
    latitude, longitude = get_latlong_from_zipcode(args.zipcode)
    if np.isnan(latitude) or np.isnan(longitude):
        print("Invalid zipcode")
        return earthquake_data
    
    # URL for the USGS Earthquake Hazards Program API
    # Forcing all queries to use the GeoJSON format, which conforms to standard JSON
    api_url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
    query = f"{api_url}&latitude={latitude}&longitude={longitude}"

    if args.radius:
        # Maximum radius allowed is 20001.6 km
        if args.radius < 0 or args.radius > 20001.6:
            print("Please provide a valid radius in the range 0-20001.6 km")
            return earthquake_data
        
        query += f"&maxradiuskm={args.radius}"

    if args.startdate:
        if not is_validate_date(args.startdate):
            return earthquake_data
        
        query += f"&starttime={args.startdate}"
    
    if args.enddate:
        if not is_validate_date(args.enddate):
            return earthquake_data
        
        query += f"&endtime={args.enddate}"
    
    if args.minmagnitude:
        query += f"&minmagnitude={args.minmagnitude}"
    
    if args.maxmagnitude:
        query += f"&maxmagnitude={args.maxmagnitude}"
    
    # Retrieve earthquake data from the API
    try:
        response = requests.get(query)
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
        return earthquake_data
    
    # Convert JSON response to a dictionary
    try:
        earthquake_data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error decoding API's JSON response")
        return earthquake_data
    
    return earthquake_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("zipcode", help="Zipcode of the location to search for earthquakes")
    parser.add_argument("--radius", type=float, default=300, help="Radius in kilometers to search for earthquakes; default is 300 km")
    parser.add_argument("--startdate", help="Start date of the search in the format YYYY-MM-DD; default is 30 days ago")
    parser.add_argument("--enddate", help="End date of the search in the format YYYY-MM-DD; default is today")
    parser.add_argument("--minmagnitude", type=float, help="Minimum magnitude of the earthquake (e.g., 2.5)")
    parser.add_argument("--maxmagnitude", type=float, help="Maximum magnitude of the earthquake (e.g., 5.4)")
    args = parser.parse_args()
 
    # Retrieve the raw earthquake data from the API
    raw_earthquake_json = get_earthquake_data(args)
    if not raw_earthquake_json:
        print("Unable to retrieve earthquake data")
        return
    
    # Reduce the data to the desired information
    earthquakes = distill_earthquake_data(raw_earthquake_json)
    print(f"Found {len(earthquakes)} earthquakes\n")
    print_earthquake_data(earthquakes)


if __name__ == "__main__":
    main()
