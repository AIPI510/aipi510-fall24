       
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
        points_url = points_base_url + str(lat) + ',' + str(lon)

        response = requests.get(points_url)
        if response.status_code == 200: 
            self.data = response.json()['properties']
            
            self.forecast_url = self.data['forecast']
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
                    if period['number'] <= 7:
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
    
    def validate_grid(self, station, x, y):
        """
        test the validity of a grid/station combo, this function has no prerequisites
        """
        gridpoint_url = f"{self.gridpoint_base_url}{station}/{x},{y}"
        response = requests.get(gridpoint_url) 
        return True if response.status_code == 200 else False

    def retrieve_grid_forecast(self):
        """
        grab the numerical forecast data for a 2.5km area

        See https://weather-gov.github.io/api/gridpoints
        
        """
        if self.forecast_url: 
            
            response = requests.get(self.forecast_url) 
            if response.status_code == 200: 
                
                self.forecast = []
                
                # todo refactor this to parse out the time series we need 
                # for period in response.json()['properties']['periods']: 
                #     if period['number'] <= 7:
                #         self.forecast.append(
                #             "Day " 
                #             + str(period['number']) 
                #             + ": " 
                #             + period['detailedForecast']
                #         )
            else: 
                raise Exception("Forecast URL (" + self.forecast_url + ") returned unexpected code: " + str(response.status_code))

        else: 
            raise Exception("No forecast URL found!")
        
        #@todo pack time series into a dataframe to simplify plotting... 

    def retrieve_serving_stations(self): 
        """
        get a list of the stations that service this grid point
        """ 
        gridpoint_base_url = 'https://api.weather.gov/gridpoints/'
        station_url = f"{gridpoint_base_url}{self.office}/{self.data['gridX']},{self.data['gridY']}/stations"
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
            observation_url = f"{stations_base_url}{station}/observations/latest"
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