import tsfresh
from tsfresh.examples.robot_execution_failures import download_robot_execution_failures, load_robot_execution_failures
from tsfresh import extract_features
import pandas as pd
import numpy as np


def get_robot_data():
    """
    Overview:
        load in the robot failures dataset.
    Param:
        None.
    Returns:
        dataframe and target column.
    """
    download_robot_execution_failures()
    return load_robot_execution_failures()


def calculate_accelerations(df):
    """
    Overview:
        calculate 3-dimensional accelerations of the robot dataframe.

    Param:
        robot dataframe

    Returns:
        dataframe with the additional columns. Acceleration of force and torque over time.
    """

    def calculate_3d_acceleration(group, cols):
        # get the velocity
        vx = group[cols[0]].diff() / group['time'].diff()
        vy = group[cols[1]].diff() / group['time'].diff()
        vz = group[cols[2]].diff() / group['time'].diff()

        # get the acceleration
        ax = vx.diff() / group['time'].diff()
        ay = vy.diff() / group['time'].diff()
        az = vz.diff() / group['time'].diff()

        # Calculate magnitude of 3D acceleration vector
        return np.sqrt(ax ** 2 + ay ** 2 + az ** 2)

    # get the force and torque accelerations
    df['force_acceleration'] = df.groupby('id').apply(
        calculate_3d_acceleration, ['F_x', 'F_y', 'F_z']).reset_index(level=0, drop=True)
    df['torque_acceleration'] = df.groupby('id').apply(
        calculate_3d_acceleration, ['T_x', 'T_y', 'T_z']).reset_index(level=0, drop=True)

    # format as 4 decimals and fill w 0 if nan
    df['force_acceleration'] = df['force_acceleration'].fillna(0).round(4)
    df['torque_acceleration'] = df['torque_acceleration'].fillna(0).round(4)

    return df


def main():
    """
    Overview:
        executes the robot data analysis.
    Param:
        None.
    Returns:
        a dataframe with robot data containing accelerations of movements.
    """
    # get the robot data
    timeseries, y = get_robot_data()

    # create copy and calculate
    df = calculate_accelerations(timeseries.copy())

    print(df.head(10))

    return df, y


if __name__ == "__main__":
    df, y = main()
