# TSFresh : Script for feature extraction on timeseries data
# Team Impasta - TA 7 

## How to run:
## python3 ta7_tsfresh_demo_team_impasta.py


from tsfresh import extract_features, select_features
from tsfresh.examples.robot_execution_failures import download_robot_execution_failures, load_robot_execution_failures
import numpy as np
from tsfresh.utilities.dataframe_functions import impute






def fetch_timeseries_data():
    download_robot_execution_failures()
    timeseries, y = load_robot_execution_failures()
    return timeseries, y

def abs_energy(x):
    return np.dot(x, x)

def rms(x):
    return np.sqrt(np.mean(x**2))

def remove_nans(x):
    impute(x)

if __name__ == "__main__":
    timeseries, y = fetch_timeseries_data()
    ids = timeseries['id'].unique()
    # extract_features extracts a lot of features grouped by id
    # for each time series associated with an entity, it gives you useful information
    # shown below
    extracted_features = extract_features(timeseries, column_id="id", column_sort = "time")
    print("Columns obtained from the extracted features")
    print(extracted_features.columns)

    print(f"Energy of F_x feature for id : {1}, from extracted features:", extracted_features.loc[1]['F_x__abs_energy'])
    F_x = timeseries[timeseries['id'] == 1]['F_x'].to_numpy()
    print(f"Energy of F_x feature for id : {1} calculated using numpy : ", abs_energy(F_x))

    print("Do the extracted features have any NaNs?")
    print(extracted_features.isna().sum()['T_z__query_similarity_count__query_None__threshold_0.0'])

    print("Imputing to remove Nans... ")
    remove_nans(extracted_features)
    print("Number of Nan's after imputing")
    print(extracted_features.isna().sum()['T_z__query_similarity_count__query_None__threshold_0.0'])

    # Selecting features using tsfresh
    # The select features functionality does some hypothesis testing to figure out which features to select
    X_selected = select_features(extracted_features, y)

    print("Selected features:")
    print(X_selected.columns)

###### TESTS
## How to run tests:
## pytest ta7_tsfresh_demo_team_impasta.py

def test_download_correctly():
    """
    Tests that the download of the robot execution dataset happens correctly
    And that the number of id's and number of rows in labels is the same
    """
    timeseries, y = fetch_timeseries_data()

    assert(timeseries['id'].unique().shape[0] == y.shape[0])

def test_abs_energy():
    h = np.array([1, 2, -1])
    assert( abs_energy(h) == 6)

def test_remove_nans():
    import pandas as pd
    k = pd.DataFrame({'test_vals': [1, 2, 3, np.nan]})
    remove_nans(k)
    assert(k.isna().sum()['test_vals'] == 0)