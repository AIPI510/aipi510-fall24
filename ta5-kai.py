import pandas as pd
import numpy as np
import unittest

# Load the dataset from URL
url = "https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD"
df = pd.read_csv(url)

# Select Model Year as an example for statistical analysis
column = 'Model Year'

# Descriptive Statistics Functions (Using Pandas)
def calculate_mean(column):
    return df[column].mean()

def calculate_median(column):
    return df[column].median()

def calculate_mode(column):
    return df[column].mode()[0]

def calculate_std(column):
    return df[column].std()

def calculate_variance(column):
    return df[column].var()

def calculate_range(column):
    return df[column].max() - df[column].min()

def calculate_iqr(column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    return q3 - q1

def calculate_skewness(column):
    return df[column].skew()

def calculate_kurtosis(column):
    return df[column].kurt()

# Simple Display of Results (Demo)
def display_statistics(column):
    print(f"Mean of {column}: {calculate_mean(column)}")
    print(f"Median of {column}: {calculate_median(column)}")
    print(f"Mode of {column}: {calculate_mode(column)}")
    print(f"\nStandard Deviation of {column}: {calculate_std(column)}")
    print(f"Variance of {column}: {calculate_variance(column)}")
    print(f"Range of {column}: {calculate_range(column)}")
    print(f"Interquartile Range (IQR) of {column}: {calculate_iqr(column)}")
    print(f"\nSkewness of {column}: {calculate_skewness(column)}")
    print(f"Kurtosis of {column}: {calculate_kurtosis(column)}")

# Run the statistics display
display_statistics(column)

# Unit Test Class
class TestDescriptiveStatistics(unittest.TestCase):

    def setUp(self):
        self.column = column

    def test_mean(self):
        expected_mean = df[self.column].mean()
        self.assertAlmostEqual(calculate_mean(self.column), expected_mean)

    def test_median(self):
        expected_median = df[self.column].median()
        self.assertEqual(calculate_median(self.column), expected_median)

    def test_mode(self):
        expected_mode = df[self.column].mode()[0]
        self.assertEqual(calculate_mode(self.column), expected_mode)

    def test_standard_deviation(self):
        expected_std = df[self.column].std()
        self.assertAlmostEqual(calculate_std(self.column), expected_std)

    def test_variance(self):
        expected_variance = df[self.column].var()
        self.assertAlmostEqual(calculate_variance(self.column), expected_variance)

    def test_range(self):
        expected_range = df[self.column].max() - df[self.column].min()
        self.assertEqual(calculate_range(self.column), expected_range)

    def test_iqr(self):
        expected_iqr = df[self.column].quantile(0.75) - df[self.column].quantile(0.25)
        self.assertAlmostEqual(calculate_iqr(self.column), expected_iqr)

    def test_skewness(self):
        expected_skew = df[self.column].skew()
        self.assertAlmostEqual(calculate_skewness(self.column), expected_skew)

    def test_kurtosis(self):
        expected_kurtosis = df[self.column].kurt()
        self.assertAlmostEqual(calculate_kurtosis(self.column), expected_kurtosis)

# Run Unit Tests
if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
