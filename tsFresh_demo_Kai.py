import pandas as pd
import matplotlib.pyplot as plt
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute, roll_time_series
import unittest

# Load the dataset
def load_data(file_path):
    """
    Load the QQQ dataset from a CSV file.

    Returns:
        DataFrame: Loaded data.
    """
    return pd.read_csv(file_path)

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
def process_data(file_path):
    """
    Process the QQQ ETF stock price data for feature extraction.

    Args:
        file_path (str): The path to the CSV file.
    
    Returns:
        DataFrame: Extracted features.
    """
    # Load the dataset
    qqq_data = load_data(file_path)

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

    """
    1. Rolling:
    The "20 entries" represent the number of rows in your original dataset that were processed to generate feature
    2. Feature extraction:
    The "19 features" reflect the unique statistical characteristics computed from those entries during the feature extraction process.
    """



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
        processed_features = process_data('QQQ_ETF_Stock_Price_History.csv')
        self.assertIsInstance(processed_features, pd.DataFrame)
        self.assertGreater(processed_features.shape[1], 0)  # Ensure some features are extracted

if __name__ == "__main__":
    # Run the unit tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

    # Process the data and extract features
    extracted_features = process_data('QQQ_ETF_Stock_Price_History.csv')
    print("Extracted Features:")
    print(extracted_features.head())
    
    """
    Feature Extraction Results:
    Each row stands for a uniqur time point from the QQQ dataset.
    Each column stands for a unique feature that tsFresh calculated based on the Price.
    [5 rows x 783 columns]
    5 rows: This output shows the first 5 time points after rolling; the full set would contain a row for each time point processed.
    783 columns: tsfresh extracted 783 features based on the Price column, representing various statistical and temporal characteristics.
    """
