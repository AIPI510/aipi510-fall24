import tsfresh
from tsfresh.examples.robot_execution_failures import download_robot_execution_failures, load_robot_execution_failures
from tsfresh import extract_features

download_robot_execution_failures()
timeseries, y = load_robot_execution_failures()

print(timeseries)



# features = extract_features(timeseries, column_id='id', column_sort='time')

