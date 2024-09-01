'''
Alpha Vantage API Sourcing Tool
Reference of Alpha Vantage API can be found here: https://www.alphavantage.co/documentation/

Background: Alpha Vantage API is a stock market data API that has information from
traditional asset classes like stocks, ETFs, mutual funds to economic indicators.
'''

import requests 
import pandas as pd
import unittest

'''
Sourcing Time Series Intraday from Alpha Vantage
"This API returns current and 20+ years of historical intraday OHLCV time series of the equity specified, 
covering pre-market and post-market hours where applicable (e.g., 4:00am to 8:00pm Eastern Time for the US market). 
You can query both raw (as-traded) and split/dividend-adjusted intraday data from this endpoint. 
The OHLCV data is sometimes called "candles" in finance literature." - reference Alpha Vantage 
(https://www.alphavantage.co/documentation/#intraday)
'''

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
r = requests.get(url)
data = r.json()

'''
Converting to data frame using pandas. Using 'Time Series (5min)'
Reference of using from_dict and converting: 
'https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.from_dict.html'
'''

TimeSeries= data['Time Series (5min)']
df = pd.DataFrame.from_dict(TimeSeries, orient='index')
#print(df)
print(df['1. open'].dtype)

df['1. open'] = df['1. open'].astype(float)

#Unit Test - Reference: https://docs.python.org/3/library/unittest.html; isinstance: https://www.w3schools.com/python/ref_func_isinstance.asp

class Testing(unittest.TestCase):

    def test_if_all_values_are_float(self):
        #Checking data type of '1. open' column which changed its data type to float. if it is not in float data type, it will raise an error.
        self.assertTrue(all(isinstance(value, float) for value in df['1. open'])), "1. open column has non-float values"

    def test_if_there_is_missing_value(self):
        #Checking if '1. open' column has no null values. 
        self.assertFalse(df['1. open'].isnull().any(),"1. open column has missing value")
        
if __name__ =='__main__':
    unittest.main()

