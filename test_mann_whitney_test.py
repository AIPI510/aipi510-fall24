import unittest
from unittest.mock import patch
import pandas as pd
from mann_whitney_test import perform_mann_whitney_test

class TestMannWhitneyUFunction(unittest.TestCase):

    @patch('mann_whitney_test.pd.read_csv')
    @patch('builtins.print')
    def test_perform_mann_whitney_test(self, mock_print, mock_read_csv):
        # Mock DataFrame for testing
        mock_data = pd.DataFrame({
            'Employment_Type': ['Remote', 'Remote', 'Remote', 'In-Office', 'In-Office', 'In-Office'],
            'Productivity_Score': [80, 85, 88, 78, 82, 77]
        })

        # Mocking the pandas read_csv return value to be the manually constructed DataFrame
        mock_read_csv.return_value = mock_data

        # Run the function
        perform_mann_whitney_test('dummy_path.csv')

        # Check the print statements
        mock_print.assert_any_call('Mann-Whitney U Test Statistic: 8.0')
        mock_print.assert_any_call('P-value: 0.2')

if __name__ == '__main__':
    unittest.main()