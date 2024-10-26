''' 
Assignment 7 - Feature Engineering
Name: Evan Moh
Date: 10/29/24

Summary of Project: This project will demonstrate feature engineering capability using TSfresh library 
by using airline passenger data.

'''
# Import all the libraries needed for feature engineering and loading data. I will use TSFresh for time series data
import pandas as pd
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute
from multiprocessing import freeze_support
import unittest

def load_data():
    #Importing airline passenger data from Github. 
    url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv' 
    df = pd.read_csv(url) 
    df['Month'] = pd.to_datetime(df['Month'])
    df['ID']=1
    return df
    
def perform_feature_extraction(df):
    extracted_features = extract_features(df, column_id= 'ID', column_sort='Month', column_value ='Passengers', disable_progressbar=True, n_jobs=1)
    impute(extracted_features)
    return(extracted_features)


# Unit test class to validate data loading and feature extraction functions.
class TestFeatureEngineering(unittest.TestCase):
    # First unit test is checking if all the expected columns are there.
    def test_load_data_columns(self):
        df = load_data()
        self.assertIn('Month', df.columns, "Data load error: 'Month' column missing")
        self.assertIn('ID', df.columns, "Data load error: 'ID' column missing")
        self.assertIn('Passengers', df.columns, "Data load error: 'Passenger' column missing")
    
    #Second unit test is checking if feature extraction happened.
    def test_perform_feature_extraction(self):
        df = perform_feature_extraction(df)
        self.assertGreater(extracted_features.shape[1], 0, "Feature extraction didn't produce any features.")

if __name__ == "__main__":
    
    freeze_support()  # For cross-platform compatibility
    # Run unit tests
    unittest.main(exit=False)
    # Load data and perform feature extraction
    df = load_data()
    extracted_features = perform_feature_extraction(df)
    # Print all generated feature names
    print("Generated Feature Names:\n", extracted_features.columns.tolist())
    print("Extracted Features:\n", extracted_features.head())
   
'''
As a result of the codes ran, there are multiple features generated like, Passengers_variance_larger_than_standard_deviation, 
Passengers_has_duplicate_max, Passengers_has_duplicated_min, Passengers__Sample_entropy,etc. As a result of this, I got 1 row x 783 columns.
'''