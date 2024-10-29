## Team Assignment 7 -- Feature Engineering
## Author: Yiqing Liu & Zejun Bai
## Package: TSFresh


import numpy as np
import pandas as pd
from scipy.fft import fft
from scipy.signal import find_peaks
from tsfresh.examples.robot_execution_failures import download_robot_execution_failures, load_robot_execution_failures
import pytest

# Load data
def load_data():
    """
    Download and load the robot execution failures dataset.
    Returns:
        timeseries (pd.DataFrame): The time series data.
        y (pd.Series): Target labels.
    """
    download_robot_execution_failures()
    timeseries, y = load_robot_execution_failures()
    return timeseries, y

# Data preprocessing
def preprocess_data(df):
    """
    Preprocess time series data by handling missing values and outliers.
    Args:
        df (pd.DataFrame): Original time series data.
    Returns:
        pd.DataFrame: Preprocessed data.
    """
    # Fill missing values
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    
    # Handle outliers
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    df = df.clip(lower=(Q1 - 1.5 * IQR), upper=(Q3 + 1.5 * IQR), axis=1)
    
    return df

# Calculate accelerations
def calculate_accelerations(df):
    """
    Calculate acceleration from force and torque data in each axis.
    Args:
        df (pd.DataFrame): Time series data with force and torque.
    Returns:
        pd.DataFrame: DataFrame with force and torque accelerations.
    """
    accelerations = pd.DataFrame(index=df.index)

    for axis in ['x', 'y', 'z']:
        force_column = f'F_{axis}'
        torque_column = f'T_{axis}'
        
        # Calculate velocity and acceleration for force
        velocity_force = df[force_column].diff()  
        acceleration_force = velocity_force.diff()  
        accelerations[f'{force_column}_acc'] = acceleration_force  
        
        # Calculate velocity and acceleration for torque
        velocity_torque = df[torque_column].diff()
        acceleration_torque = velocity_torque.diff()
        accelerations[f'{torque_column}_acc'] = acceleration_torque

    # Calculate composite accelerations
    accelerations['F_total_acc'] = np.sqrt(accelerations['F_x_acc']**2 + accelerations['F_y_acc']**2 + accelerations['F_z_acc']**2)
    accelerations['T_total_acc'] = np.sqrt(accelerations['T_x_acc']**2 + accelerations['T_y_acc']**2 + accelerations['T_z_acc']**2)
    
    return accelerations

# Extract features
def extract_features(accelerations):
    """
    Extracts statistical, frequency domain, peak, and complexity features.
    Args:
        accelerations (pd.DataFrame): Acceleration data.
    Returns:
        dict: Extracted features.
    """
    features = {}

    # Statistical features
    for col in ['F_total_acc', 'T_total_acc']:
        features[f'{col}_mean'] = accelerations[col].mean()
        features[f'{col}_std'] = accelerations[col].std()
        features[f'{col}_max'] = accelerations[col].max()
        features[f'{col}_min'] = accelerations[col].min()
        features[f'{col}_sum_of_absolute_changes'] = np.sum(np.abs(np.diff(accelerations[col])))

    # Frequency domain features
    for col in ['F_total_acc', 'T_total_acc']:
        fft_vals = fft(accelerations[col].dropna())  # Remove NaN values
        features[f'{col}_fft_max'] = np.max(np.abs(fft_vals))
        features[f'{col}_fft_mean'] = np.mean(np.abs(fft_vals))
        features[f'{col}_fft_std'] = np.std(np.abs(fft_vals))

    # Peak features
    for col in ['F_total_acc', 'T_total_acc']:
        peaks, _ = find_peaks(accelerations[col].dropna())
        features[f'{col}_num_peaks'] = len(peaks)
        features[f'{col}_mean_peak_height'] = np.mean(accelerations[col].iloc[peaks]) if peaks.size > 0 else 0

    # Temporal difference features
    for col in ['F_total_acc', 'T_total_acc']:
        features[f'{col}_mean_diff'] = accelerations[col].diff().mean()
        features[f'{col}_abs_sum_of_changes'] = np.sum(np.abs(accelerations[col].diff()))

    # Complexity features - Shannon entropy
    def shannon_entropy(data):
        """Calculates Shannon entropy."""
        probs = np.histogram(data, bins=10, density=True)[0]
        probs = probs[probs > 0]
        return -np.sum(probs * np.log2(probs))

    for col in ['F_total_acc', 'T_total_acc']:
        features[f'{col}_shannon_entropy'] = shannon_entropy(accelerations[col].dropna())
    
    return features

# Unit tests
def test_preprocess_data():
    df = pd.DataFrame({"A": [1, 2, np.nan, 4, 5], "B": [5, np.nan, 7, 8, np.nan]})
    preprocessed_df = preprocess_data(df)
    assert preprocessed_df.isna().sum().sum() == 0  # Ensure no missing values

def test_calculate_accelerations():
    df = pd.DataFrame({"F_x": [1, 2, 4, 7], "F_y": [1, 3, 6, 10], "F_z": [2, 3, 5, 8],
                       "T_x": [1, 1, 2, 2], "T_y": [0, 1, 1, 0], "T_z": [1, 0, 1, 0]})
    accelerations = calculate_accelerations(df)
    assert "F_x_acc" in accelerations.columns
    assert "T_total_acc" in accelerations.columns

def test_extract_features():
    df = pd.DataFrame({"F_total_acc": [1, 2, 4, 7], "T_total_acc": [1, 3, 6, 10]})
    features = extract_features(df)
    assert "F_total_acc_mean" in features
    assert "T_total_acc_shannon_entropy" in features

if __name__ == "__main__":
    # Load data
    timeseries, y = load_data()
    print("Data loaded.")

    # Preprocess data
    timeseries = preprocess_data(timeseries)
    print("Data preprocessing complete.")

    # Calculate accelerations
    accelerations = calculate_accelerations(timeseries)
    print("Acceleration calculation complete.")
    
    # Extract features
    features = extract_features(accelerations)
    print("Extracted features:\n", features)

    # Run tests
    import sys
    sys.exit(pytest.main([__file__]))
