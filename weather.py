# Note: The IPGeo, Forecast and Precipitation classes were lifted from auto-d's 
# premodule assignment to boostrap the API interactions, waiting for guidance on
# how this should be annotated. 
        
import requests

class IPGeo: 
    """
    Wrapper for a free IP geo API. Assumed to be called from within the US only.     
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

        print('Looking up location by IP...')
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
    station = None
    location = None
    forecast = None

    def __init__(self): 
        pass

    def resolve_location(self, lat, lon): 
        """
        retrieve a US forecast given a lat/lon pair
        """
        
        # Resolve our location ... e.g. https://api.weather.gov/points/39.7456,-97.0892
        points_base_url = "https://api.weather.gov/points/"
        points_url = points_base_url + str(lat) + ',' + str(lon)

        print("Resolving weather prediction site...")
        response = requests.get(points_url)
        if response.status_code == 200: 
            self.data = response.json()['properties']
            
            self.forecast_url = self.data['forecast']
            self.station = self.data['cwa']

            loc = self.data['relativeLocation']['properties']
            self.location = loc['city'] + ', ' + loc['state']

    def update_forecast(self):
        """
        grab the forecast, requires location resolution be updated prior
        """
        if self.forecast_url: 
            
            print("Retrieving forecast...")
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

    # Consider utilty of a/the python geojson library here in decoding API responses
    # See 

    {'@id': 'https://api.weather.gov/points/35.7919,-78.6541', 
     '@type': 'wx:Point', 'cwa': 'RAH', 
     'forecastOffice': 'https://api.weather.gov/offices/RAH', 
     'gridId': 'RAH', 'gridX': 74, 'gridY': 58, 'forecast': 'https://api.weather.gov/gridpoints/RAH/74,58/forecast', 'forecastHourly': 'https://api.weather.gov/gridpoints/RAH/74,58/forecast/hourly', 'forecastGridData': 'https://api.weather.gov/gridpoints/RAH/74,58', 'observationStations': 'https://api.weather.gov/gridpoints/RAH/74,58/stations', 'relativeLocation': {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [-78.641768, 35.830598]}, 'properties': {'city': 'Raleigh', 'state': 'NC', 'distance': {'unitCode': 'wmoUnit:m', 'value': 4444.3934196161}, 'bearing': {'unitCode': 'wmoUnit:degree_(angle)', 'value': 194}}}, 'forecastZone': 'https://api.weather.gov/zones/forecast/NCZ041', 'county': 'https://api.weather.gov/zones/county/NCC183', 'fireWeatherZone': 'https://api.weather.gov/zones/fire/NCZ041', 'timeZone': 'America/New_York', 'radarStation': 'KRAX'}
    def fetch_grid(self):
        """
        grab the numerical forecast data for a 2.5km area

        See https://weather-gov.github.io/api/gridpoints
        
        """
        if self.forecast_url: 
            
            print("Retrieving forecast...")
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
import datetime

class Precipitation: 
    """
    Wrapper for a very annoying NOAA API to obtain historical precipitation info.
    """

    noaa_token='HGSaAdFuTwXNcAgyrbysQlUXxBTTxsjY' #10 requests/sec, 10000 requests/day
    noaa_url = 'http://www.ncdc.noaa.gov/cdo-web/api/v2/data'

    headers = { 'token' : noaa_token }
    precip = None

    def __init__(self): 
        pass

    def update_precipitation(self, zip_code, days_prior=7): 
        """
        Retrieve historical precipitation data from a NOAA API for a US zip code
        """
        
        # Relative times computed with help from datetime API docs (https://docs.python.org/3/library/datetime.html#examples-of-usage-timedelta)
        end_date = datetime.date.today() 
        start_date = end_date - datetime.timedelta(days=days_prior)
        end = end_date.strftime("%Y-%m-%d")
        start = start_date.strftime("%Y-%m-%d")
         
        # The NOAA APIs seem notorious for their inscrutability, used this API guide: 
        # https://github.com/partytax/ncei-api-guide/blob/master/README.md

        # API expects YYYY-MM-DD for date range
        params = '?' \
            + 'datasetid=GHCND' \
            + '&units=standard' \
            + f'&locationid=ZIP:{zip_code}' \
            + f'&startdate={start}' \
            + f'&enddate={end}'

        print('Querying for historical precipitation, this might take a bit...')

        response = requests.get(self.noaa_url + params, headers=self.headers)
        if response.status_code == 200: 
            self.precip = [] 

            try: 
                results = response.json()['results']
                for result in results: 
                    if result['datatype'] == 'PRCP':
                        date = result['date'].split('T')[0]
                        self.precip.append({ 'date': date, 'precip_inches': str(result['value'])})
            except KeyError as k: 
                print(f"Failed to parse precipitation data response from NOAA API, bailing! \n This may happen if there are no historicals available for the identified zip code ({zip_code})") 
