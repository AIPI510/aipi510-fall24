def get_robot_data():
    """
    Overview:
        load in the robot failures dataset.
        Parts of this code were generated with the help of Perplexity AI
    Param:
        None.
    Returns:
        dataframe and target column.
    """

    from tsfresh.examples.robot_execution_failures import download_robot_execution_failures, load_robot_execution_failures

    download_robot_execution_failures()
    return load_robot_execution_failures()

def calculate_total_value(df):
    """
    Overview:
        calculates total value of both force and torque.

    Param:
        robot dataframe

    Returns:
        dataframe with the additional columns. Total Value of force and torque over time.
    """
    import numpy as np
    import pandas as pd

    def calculate_3d_value(group, cols):
        # get the velocity
        val_x = group[cols[0]]
        val_y = group[cols[1]]
        val_z = group[cols[2]]

        
        # get the magnitude of 3D acceleration vector using numpy
        return np.sqrt(val_x ** 2 + val_y ** 2 + val_z ** 2)
    
    df['force_3D'] = df.groupby('id').apply(
        calculate_3d_value, ['F_x', 'F_y', 'F_z']).reset_index(level=0, drop=True)
    df['torque_3D'] = df.groupby('id').apply(
        calculate_3d_value, ['T_x', 'T_y', 'T_z']).reset_index(level=0, drop=True)
    
    df['force_3D'] = df['force_3D'].fillna(0).round(4)
    df['torque_3D'] = df['torque_3D'].fillna(0).round(4)

    return df

def calculate_accelerations(df):
    """
    Overview:
        calculate 3-dimensional accelerations of the robot dataframe.

    Param:
        robot dataframe

    Returns:
        dataframe with the additional columns. Acceleration of force and torque over time.
    """

    import numpy as np
    import pandas as pd

    # def calculate_3d_acceleration(group, cols):
    #     # get the velocity
    #     vx = group[cols[0]].diff() / group['time'].diff()
    #     vy = group[cols[1]].diff() / group['time'].diff()
    #     vz = group[cols[2]].diff() / group['time'].diff()

    #     # get the acceleration
    #     ax = vx.diff() / group['time'].diff()
    #     ay = vy.diff() / group['time'].diff()
    #     az = vz.diff() / group['time'].diff()

    #     # get the magnitude of 3D acceleration vector using numpy
    #     velocity_magnitude = np.sqrt(vx ** 2 + vy ** 2 + vz ** 2)
    #     acceleration_magnitude = np.sqrt(ax ** 2 + ay ** 2 + az ** 2)
    #     return pd.Series({'velocity': velocity_magnitude, 'acceleration': acceleration_magnitude})


    # force_result = df.groupby('id', group_keys=False).apply(
    #     calculate_3d_acceleration, ['F_x', 'F_y', 'F_z']).reset_index(level=0, drop=True)
    # df['force_yank'] = force_result['velocity'].to_numpy()
    # df['force_acceleration'] = force_result['acceleration'].to_numpy()

    # # Calculate for torque
    # torque_result = df.groupby('id', group_keys=False).apply(
    #     calculate_3d_acceleration, ['T_x', 'T_y', 'T_z']).reset_index(level=0, drop=True)
    # df['torque_rotatum'] = torque_result['velocity'].to_numpy()
    # df['torque_acceleration'] = torque_result['acceleration'].to_numpy()
    # # # get the force and torque accelerations
    # # df['yank'],df['force_acceleration'] = df.groupby('id').apply(
    # #     calculate_3d_acceleration, ['F_x', 'F_y', 'F_z']).reset_index(level=0, drop=True)
    # # df['rotatum'],df['torque_acceleration'] = df.groupby('id').apply(
    # #     calculate_3d_acceleration, ['T_x', 'T_y', 'T_z']).reset_index(level=0, drop=True)

    # # format as 4 decimals and fill w 0 if nan
    # df['force_acceleration'] = df['force_acceleration'].fillna(0).round(4)
    # df['torque_acceleration'] = df['torque_acceleration'].fillna(0).round(4)
    # df['force_yank'] = df['force_yank'].fillna(0).round(4)
    # df['torque_rotatum'] = df['torque_rotatum'].fillna(0).round(4)

    # return df

def calculate_accelerations(df):
    """
    Overview:
        calculate 3-dimensional accelerations of the robot dataframe.

    Param:
        robot dataframe

    Returns:
        dataframe with the additional columns. Acceleration of force and torque over time.
    """

    import numpy as np

    def calculate_3d_acceleration(group, cols):
        # get the velocity
        vx = group[cols[0]].diff() / group['time'].diff()
        vy = group[cols[1]].diff() / group['time'].diff()
        vz = group[cols[2]].diff() / group['time'].diff()

        # get the acceleration
        ax = vx.diff() / group['time'].diff()
        ay = vy.diff() / group['time'].diff()
        az = vz.diff() / group['time'].diff()

        # get the magnitude of 3D acceleration vector using numpy
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



def calculate_work_3d(df):
    """
    Overview:
        calculate 3-dimensional work of the robot dataframe.

    Param:
        robot dataframe

    Returns:
        dataframe with the additional columns. Work done over time.
    """
    import numpy as np
    import pandas as pd
    def calculate_3d_work(group, force_cols):
        # Calculate displacement
        dx = group[force_cols[0]].diff().cumsum()
        dy = group[force_cols[1]].diff().cumsum()
        dz = group[force_cols[2]].diff().cumsum()
        
        # Calculate work as dot product of force and displacement
        work = (group[force_cols[0]] * dx + 
                group[force_cols[1]] * dy + 
                group[force_cols[2]] * dz)
        
        # Cumulative sum of work
        return work.cumsum()
    
    # get the work done
    df['work_done'] = df.groupby('id').apply(
        calculate_3d_work, ['F_x', 'F_y', 'F_z']).reset_index(level=0, drop=True)
    
    # format as 4 decimals and fill w 0 if nan
    df['work_done'] = df['work_done'].fillna(0).round(4)

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
    import pandas as pd
    # get the robot data
    timeseries, y = get_robot_data()

    # create copy and calculate
    df = calculate_accelerations(timeseries.copy())

    df = calculate_total_value(df)

    df = calculate_work_3d(df)

    print(df)
    df.to_csv('filename.csv', index=False)
    return df, y


if __name__ == "__main__":
    df, y = main()
