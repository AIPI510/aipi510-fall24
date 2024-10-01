import numpy as np


def calculate_variance(data):
    """
    Variance represents the degree of spread in a set of data points.
    """
    return np.var(data, ddof=1)


def calculate_standard_deviation(data):
    """
    Standard deviation indicats how spread out the values are from the mean.
    """
    return np.std(data, ddof=1)


def calculate_iqr(data):
    """
    The interquartile range (IQR) represent the range between the first quartile (Q1)
    and the third quartile (Q3) of a dataset, covering the middle 50% of the data points.
    """
    q75 = np.percentile(data, 75, method='midpoint')
    q25 = np.percentile(data, 25, method='midpoint')
    return q75 - q25


def calculate_range(data):
    """
    Range is a measure of spread that represents the difference between the maximum and minimum values in a dataset.
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
