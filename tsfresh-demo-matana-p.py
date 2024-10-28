import pandas as pd
import numpy as np

import tsfresh
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh.feature_extraction.feature_calculators import set_property

def load_csv():
    """Load data from local CSV file, and return pandas dataframe"""
    try:
        # Read the csv file and put it into pandas dataframe, remove initial/redundant space, and choose specific columns as input for the dataframe
        """CSV source (Air Pollution Data for two cities in Thailand: Bangkok and Chiang Mai): 
            https://aqicn.org/city/bangkok/
            https://aqicn.org/city/chiang-mai/
            The data were downloaded as separate CSV files, then combined into a single file, and added a new column "city" """
        
        df = pd.read_csv('data/thailand-air-quality.csv', usecols=["city", "date", "pm25", "pm10"], skipinitialspace = True)
        # Convert date column to have proper date format
        df["date"]= pd.to_datetime(df["date"], dayfirst=False, yearfirst=False)
        # Drop rows without pm25/pm10 data
        df.dropna(subset=["pm25", "pm10"], inplace=True)
        # Sort the data based on city (ascending), and then date (most recent date first)
        df = df.sort_values(by=["city", "date"], ascending=[True, False])
        return df
        
    except Exception as err:
        print(f'Error in CSV file loading occurred: {err}')


# Custom Feature Function
@set_property("fctype", "simple")
def goodair_pct_day_count(x, p, t):
     """Custom Feature: Return True if number of days with good air (AQI <= threshold t) is not less than p% of total number of days
     x: time series to calculate feature
     p: percentage of total number of days
     t: AQI threshold"""
     if ((x <= t).sum()/x.size >= p):
        return True
     return False
# Register the Custom Feature Calculator (goodair_pct_day_count_above) to make it available as a feature calculator in the tsfresh library
setattr(tsfresh.feature_extraction.feature_calculators, "goodair_pct_day_count", goodair_pct_day_count)


def extract_features_and_impute(df):
    """Extract features, then impute missing values"""
    # Set the list of features to be extracted
    fc_parameters = {   
                        'mean': None,
                        'median': None,
                        'maximum': None,
                        'minimum': None,
                        'standard_deviation': None,
                        'variation_coefficient': None,
                        'variance': None,
                        'skewness': None,
                        'kurtosis': None,
                        'first_location_of_maximum': None,      
                        'last_location_of_maximum': None,
                        'first_location_of_minimum': None,
                        'last_location_of_minimum': None,
                        'count_above': [{'t': 50}, {'t': 100}],  # count % of days with PM2.5/PM10 AQI above 50 / 100 (US EPA AQI standard)
                        'count_below': [{'t': 50}, {'t': 100}],  # count % of days with PM2.5/PM10 AQI below 50 / 100
                    }
    # Add custom feature: goodair_pct_day_count to fc_parameters
    fc_parameters[goodair_pct_day_count] = [{'t': 50, 'p': 0.99}, {'t': 100, 'p': 0.99}]

    # Extract features from df
    extracted_features = extract_features(df, column_id='city', column_sort='date', default_fc_parameters=fc_parameters)

    # Impute missing values
    impute(extracted_features)
    return extracted_features


def test_load_data():
    """Test loading data from CSV, by checking if the PM2.5 AQI pollution data loaded is in typical range"""
    df = load_csv()
    assert (df["pm25"].max() < 10000) & (df["pm25"].max() >= 0)


def test_goodair_pct_day_count():
    """Test goodair_pct_day_count by a test set of numbers below"""
    x = np.array([60, 40, 30, 45, 20])
    p = 0.75
    t = 50
    assert goodair_pct_day_count(x, p, t) == True


def test_extract_features_and_impute():
    """Test extracting features and imputing missing values, by checkin if %day count of PM2.5 below 100 AQI is no more than 100% """
    df = load_csv()
    extracted_features = extract_features_and_impute(df)
    assert extracted_features["pm25__count_below__t_100"].max() < 1


def main():
    """ Extract features from data from the source CSV file"""
    # Load data from CSV file into dataframe df
    df = load_csv()
    print("Sample of Data:")
    print(df.head())

    # Extract features according to the predefined feature list
    extracted_features = extract_features_and_impute(df)
    pd.set_option("display.max_columns", None)
    print("\nFeatures extracted from the data:")
    print(extracted_features.head())


if __name__ == '__main__':
	main()