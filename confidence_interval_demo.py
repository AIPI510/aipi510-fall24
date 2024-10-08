import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
import seaborn as sns
import matplotlib.pyplot as plt
import math

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 35.994,
	"longitude": -78.8986,
	"hourly": "temperature_2m",
	"start_date": "2024-07-01",
	"end_date": "2024-10-01"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m

hourly_dataframe = pd.DataFrame(data = hourly_data)

sample_size = hourly_dataframe.shape[0]
sample_mean = hourly_dataframe['temperature_2m'].mean()
std_dev = hourly_dataframe['temperature_2m'].std()
z = 1.96

print(sample_size)
print(sample_mean)
print(std_dev)
upper_bound = sample_mean + z * (std_dev/math.sqrt(sample_size))
lower_bound = sample_mean - z * (std_dev/math.sqrt(sample_size))

sns.lineplot(x=hourly_dataframe['date'], y=hourly_dataframe['temperature_2m'])
plt.xticks(rotation=45) 
plt.title("Temperature Change by date in Durham")
plt.ylabel('Temperature (Celsius)')
plt.xlabel('Date')
plt.tight_layout()
plt.show()


sns.histplot(hourly_dataframe, bins=10, kde=True) 
plt.title("Distribution of Temperature in Durham")
plt.xlabel('Temperature (Celsius)')
plt.ylabel('Count of Temperature Values')
plt.show()

sns.lineplot(x=hourly_dataframe['date'], y=hourly_dataframe['temperature_2m'])
plt.axhline(y=lower_bound, color='red', linestyle='--', label=str(lower_bound))
plt.axhline(y=upper_bound, color='red', linestyle='--', label=str(upper_bound))
plt.xticks(rotation=45) 
plt.title("Temperature Change by date in Durham")
plt.ylabel('Temperature (Celsius)')
plt.xlabel('Date')
plt.tight_layout()
plt.show()

sns.histplot(hourly_dataframe, bins=10, kde=True) 
plt.axvline(x=lower_bound, color='red', linestyle='--', label=f'{lower_bound}')
plt.axvline(x=upper_bound, color='red', linestyle='--', label=f'{upper_bound}')
plt.title("Distribution of Temperature in Durham")
plt.xlabel('Temperature (Celsius)')
plt.ylabel('Count of Temperature Values')
plt.show()


