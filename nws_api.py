       
import requests
import pandas as pd

class IPGeo: 
    """
    Wrapper for a free IP geo API. Assumed to be called from within the US only.     

    Note: this class was repurposed from auto-d's premodule assignment repo 
    """

    data = None
    lat = None
    lon = None
    zip = None
    city = None
    state = None

    def __init__(self): 
        self.geo()

    def geo(self): 
        """
        Poke the Internet and geolocate the source (first routable) IP 
        """
        # Techniknews.net free IP geolocation API, this URI maps your routable Internet address to the 
        # lat/long of its owner
        ip_geo_url='https://api.techniknews.net/ipgeo'

        response = requests.get(ip_geo_url)
        if response.ok: 
            try: 
                self.data = response.json()
                self.lat = self.data['lat']
                self.lon = self.data['lon']
                self.zip = self.data['zip']
                self.city = self.data['city']
                self.state = self.data['regionName']
            except KeyError as k:
                print('Failed to unpack IP geolocation response')

class Forecast: 
    """
    Wrapper for a US National Weather Service forecast API

    """
    data = None    
    forecast_url = None
    office = None
    location = None
    forecast = None

    def __init__(self): 
        pass

    def resolve_location(self, lat, lon): 
        """
        retrieve a US forecast given a lat/lon pair

        Note: this function was repurposed from auto-d's premodule assignment
        """
        
        # Resolve our location ... e.g. https://api.weather.gov/points/39.7456,-97.0892
        points_base_url = "https://api.weather.gov/points/"
        points_url = points_base_url + str(lat) + ',' + str(lon)  #obtain correct url

        response = requests.get(points_url)
        if response.status_code == 200: 
            self.data = response.json()['properties']  
            
            self.forecast_url = self.data['forecast']  #store for later use
            self.office = self.data['cwa']

            loc = self.data['relativeLocation']['properties']  
            self.location = loc['city'] + ', ' + loc['state']

    def update_forecast(self):
        """
        grab the forecast for the cached location, requires location resolution be updated prior
        """
        if self.forecast_url: 
            
            response = requests.get(self.forecast_url) 
            if response.status_code == 200: 
                
                self.forecast = []
                
                for period in response.json()['properties']['periods']: 
                    if period['number'] <= 7:  #limit collection to next 7 days
                        self.forecast.append(
                            "Day " 
                            + str(period['number']) 
                            + ": " 
                            + period['detailedForecast']
                        )
            else: 
                raise Exception("Forecast URL (" + self.forecast_url + ") returned unexpected code: " + str(response.status_code))

        else: 
            raise Exception("No forecast URL found!")
    
    def retrieve_hourly_forecast(self):
        """
        get the hourly temperature forecast data

        Returns: 
            pandas.DataFrame: the hourly forecast for temperature
        """
        response = requests.get(self.data['forecastHourly'])
        response.raise_for_status()  
        data = response.json()
        periods = data['properties']['periods']
        data = []
        for period in periods:
            farenheight = period['temperature']
            celsius = (farenheight - 32) * (5.0/9.0)  #convert to celsius for prefence
            data.append({
                'time': pd.to_datetime(period['startTime']),
                'temperature': celsius
            })
        
        df = pd.DataFrame(data)  #store in pandas dataframe
        df.set_index('time', inplace=True)
        return df 

    def validate_grid(self, station, x, y):
        """
        test the validity of a grid/station combo, this function has no prerequisites

        returns a bool indiciating wehether or not the NWS reports this as a valid grid
        """
        gridpoint_url = f"{self.gridpoint_base_url}{station}/{x},{y}"  #obtain correct url
        response = requests.get(gridpoint_url) 
        return True if response.status_code == 200 else False
 

    def retrieve_serving_stations(self): 
        """
        get a list of the stations that service this grid point
        """ 
        gridpoint_base_url = 'https://api.weather.gov/gridpoints/'
        station_url = f"{gridpoint_base_url}{self.office}/{self.data['gridX']},{self.data['gridY']}/stations"  #obtain correct url
        response = requests.get(station_url)
        response.raise_for_status()
        
        stations = []
        try: 
            for f in response.json()['features']:
                station = f['properties']['stationIdentifier']
                name = f['properties']['name']
                lat = f['geometry']['coordinates'][1]
                lon = f['geometry']['coordinates'][0]
                stations.append({ 'station': station, 'name': name, 'lat': lat, 'lon': lon})
        
        except KeyError as ke: 
            raise KeyError('Server response missing expected key: ' + str(ke))

        return pd.DataFrame(stations,columns=['station','name','lat','lon'])

    def retrieve_observations(self, stations): 
        """
        given a NWS station, retrieve the latest observations

        returns a dict with current temp and a weather string, e.g. {'temperature': 22.1, 'weather': 'rain'}
        failures in retrieval may result in empty values
        """ 
        stations_base_url = 'https://api.weather.gov/stations/'

        obs = [] 
        for station in stations: 
            observation_url = f"{stations_base_url}{station}/observations/latest"   #obtain correct url
            response = requests.get(observation_url)
            response.raise_for_status()
        
            ob = {} 
            try:             
                properties = response.json()['properties']
                weather_valid = True if len(properties['presentWeather']) > 0 else False
                ob = { 
                    'station': station, 
                    'temp': properties['temperature']['value'], 
                    'humidity': properties['relativeHumidity']['value'],
                    'weather': properties['presentWeather'][0]['weather'] if weather_valid else 'n/a'
                }
                
            except KeyError as ke: 
                print('Server response missing expected key: ' + str(ke))
            except IndexError as ie: 
                print('Failed to locate weather forecast: ' + str(ie))

            obs.append(ob) 

        return pd.DataFrame(obs,columns=['station','temp','humidity', 'weather'])
    

# Demonstrate if invoked from the command line, not if imported... 
if __name__ == '__main__': 

    geo = IPGeo()

    stations = None
    print(f'\nYour IP locates you in {geo.city}, {geo.state} at {geo.lat} {geo.lon}')
    print("Press enter to retrieve weather information for these coordinates.")
    input()
    print("Retrieving office associated with your coordinates...\n")
    forecast = Forecast()
    forecast.resolve_location(geo.lat, geo.lon) 

    print(f'Weather forecasts for {geo.lat} {geo.lon} are provided by the NWS {forecast.office} office, located in {forecast.location}.')

    print('Press enter to retrieve the 7-day forecast.')
    input()
    forecast.update_forecast() #collect forecast data
    for f in forecast.forecast: 
        print(" - " + f)

    print(f'\nPress enter to retrieve the hourly forecast data from your local office.')
    input()
    tempdata = forecast.retrieve_hourly_forecast()
    print(f'Excerpt of hourly time series returned: ')
    print(tempdata.head()) 

    print(f"\nForecast information for {forecast.location} is sourced from numerous regional weather stations. Press enter to retrieve a list.")
    input()
    stations = forecast.retrieve_serving_stations()
    print(f'Weather stations that contribute to the forecasts the NWS sources for {forecast.location} are listed below.')
    print(stations)

    print("\nEach weather station sources its own observations, which we can poll through the API.")
    print("Presse enter to retrieve current observations from these weather stations (this might take a bit)...") 
    input()
    observations = forecast.retrieve_observations(stations['station'])
    print('\nCurrent temperatures by reporting station:')
    print(observations)

    print("\nDeveloper Notes")
    print(" - The NWS API is documented with an OpenAPI UI [here](https://www.weather.gov/documentation/services-web-api), however it's use is not straightforward.")
    print(" - The most intuitive way to learn about the API is to visit the Point Forecast site @ https://www.weather.gov/forecastpoints/ and click around.")
    print(" - Your browser's developer tools (turned on and monitoring the network traffic) will give great insight into the 'approved' way to use the API.\n")

    print("Thanks for enjoying this demo ;)\n")
