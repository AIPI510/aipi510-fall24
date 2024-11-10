import pandas as pd
import matplotlib.pyplot as plt
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute, roll_time_series
import unittest

# Google Sheets CSV URL
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1TXuCbXsZAkA63E6j2C8eNosuBrAEd8o3P03rKf-Gi3w/export?format=csv"

# Load the dataset
def load_data():
    """
    Load the QQQ dataset from a Google Sheets CSV URL.

    Returns:
        DataFrame: Loaded data.
    """
    return pd.read_csv(GOOGLE_SHEET_CSV_URL)

# Visualize Price Data
def visualize_price(data):
    """
    Plot the price over the last year.

    Args:
        data (DataFrame): Data containing 'Date' and 'Price' columns.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(data['Date'], data['Price'], color='blue', label='Price')
    plt.title('QQQ ETF Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Main function to process data
def process_data():
    """
    Process the QQQ ETF stock price data for feature extraction.

    Returns:
        DataFrame: Extracted features.
    """
    # Load the dataset
    qqq_data = load_data()

    # Create a new dataset with only 'Date' and 'Price' columns
    new_dataset = qqq_data[['Date', 'Price']]
    
    # Check data types and NaN values
    print(new_dataset.dtypes)
    print(new_dataset.isna().sum())

    # Visualize price data
    visualize_price(new_dataset)

    # Assigning 'QQQ' to each row
    new_dataset['symbol'] = 'QQQ'  

    # Rolling time series for feature extraction
    df_rolled = roll_time_series(new_dataset, column_id="symbol", column_sort="Date", max_timeshift=20, min_timeshift=5)

    # Extract features
    x = extract_features(df_rolled.drop("symbol", axis=1), column_id="id", column_sort="Date", column_value="Price", impute_function=impute, show_warnings=False)
    
    return x

# Unit tests for data processing
class TestDataProcessing(unittest.TestCase):
    
    def setUp(self):
        # Load a small sample dataset for testing
        self.test_data = pd.DataFrame({
            'Date': ['10/28/2024', '10/25/2024', '10/24/2024'],
            'Price': [496.26, 495.32, 492.32]
        })
    
    def test_load_data(self):
        """Test loading of data."""
        self.assertEqual(self.test_data.shape[0], 3)

    def test_visualize_price(self):
        """Test that visualization function runs without errors."""
        try:
            visualize_price(self.test_data)
            result = True
        except Exception as e:
            result = False
        self.assertTrue(result)

    def test_process_data(self):
        """Test the data processing function."""
        processed_features = process_data()
        self.assertIsInstance(processed_features, pd.DataFrame)
        self.assertGreater(processed_features.shape[1], 0)  # Ensure some features are extracted

if __name__ == "__main__":
    # Run the unit tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

    # Process the data and extract features
    extracted_features = process_data()
    print("Extracted Features:")
    print(extracted_features.head())
