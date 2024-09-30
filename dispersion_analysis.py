import numpy as np


def calculate_variance(data):
    """
    Calculate the variance of a dataset.
    
    Parameters:
    data (list or ndarray): A list or array of numerical values.

    Returns:
    float: Variance of the data.
    """
    return np.var(data, ddof=1)


def calculate_standard_deviation(data):
    """
    Calculate the standard deviation of a dataset.

    Parameters:
    data (list or ndarray): A list or array of numerical values.

    Returns:
    float: Standard deviation of the data.
    """
    return np.std(data, ddof=1)


def calculate_iqr(data):
    """
    Calculate the interquartile range (IQR) of a dataset.

    Parameters:
    data (list or ndarray): A list or array of numerical values.

    Returns:
    float: Interquartile range of the data.
    """
    q75 = np.percentile(data, 75, interpolation='midpoint')
    q25 = np.percentile(data, 25, interpolation='midpoint')
    return q75 - q25


def calculate_range(data):
    """
    Calculate the range of a dataset.

    Parameters:
    data (list or ndarray): A list or array of numerical values.

    Returns:
    float: Range of the data.
    """
    return np.max(data) - np.min(data)


if __name__ == "__main__":
    # Sample data
    data = [10, 12, 23, 23, 16, 23, 21, 16]

    # Calculate and display measures of dispersion
    print("Variance:", calculate_variance(data))
    print("Standard Deviation:", calculate_standard_deviation(data))
    print("Interquartile Range (IQR):", calculate_iqr(data))
    print("Range:", calculate_range(data))
