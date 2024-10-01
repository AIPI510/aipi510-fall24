import unittest
import numpy as np
import pandas as pd
from ta5_wukong import one_sample_t_test  # Correctly import the module
import tempfile
import os

class TestOneSampleTTest(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        # Create a temporary directory for storing uploaded files
        self.temp_dir = tempfile.mkdtemp()

        # Create a sample CSV file with specified values
        self.sample_data = pd.DataFrame({
            'data': [1, 2, 3, 4, 5, 6, 7, 7, 8, 8, 8]  
        })
        self.sample_csv_path = os.path.join(self.temp_dir, 'sample_data.csv')
        self.sample_data.to_csv(self.sample_csv_path, index=False)  # Save as CSV file

        self.population_mean = 5  # Define the population mean
        self.alpha = 0.05  # Significance level

    def tearDown(self):
        """Clean up the test environment."""
        # Remove temporary directory and its files
        for filename in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, filename)
            os.remove(file_path)
        os.rmdir(self.temp_dir)  # Remove the temporary directory

    def test_two_sided_t_test(self):
        """Test the functionality of the two-sided one-sample t-test."""
        sample_data = pd.read_csv(self.sample_csv_path)['data']
        result = one_sample_t_test(sample_data, self.population_mean, alpha=self.alpha, test_type='two-sided')

        print("Two-sided Test Actual t-statistic:", result['t_stat'])
        print("Two-sided Test Actual p-value:", result['p_value'])

        expected_t_stat = 0.4747  
        expected_p_value = 0.6452  

        # Assertion checks to verify the test results
        self.assertAlmostEqual(result['t_stat'], expected_t_stat, places=4)
        self.assertAlmostEqual(result['p_value'], expected_p_value, places=4)
        self.assertEqual(result['result'], "Fail to reject the null hypothesis (H0)")

    def test_left_tailed_t_test(self):
        """Test the functionality of the left-tailed one-sample t-test."""
        sample_data = pd.read_csv(self.sample_csv_path)['data']
        result = one_sample_t_test(sample_data, self.population_mean, alpha=self.alpha, test_type='left-tailed')

        print("Left-tailed Test Actual t-statistic:", result['t_stat'])
        print("Left-tailed Test Actual p-value:", result['p_value'])

        expected_t_stat = 0.4747
        expected_p_value = 0.3226  # Expected p-value for left-tailed test

        # Assertion checks
        self.assertAlmostEqual(result['t_stat'], expected_t_stat, places=4)
        self.assertAlmostEqual(result['p_value'], expected_p_value, places=4)
        self.assertEqual(result['result'], "Fail to reject the null hypothesis (H0)")

    def test_right_tailed_t_test(self):
        """Test the functionality of the right-tailed one-sample t-test."""
        sample_data = pd.read_csv(self.sample_csv_path)['data']
        result = one_sample_t_test(sample_data, self.population_mean, alpha=self.alpha, test_type='right-tailed')

        print("Right-tailed Test Actual t-statistic:", result['t_stat'])
        print("Right-tailed Test Actual p-value:", result['p_value'])

        expected_t_stat = 0.4747
        expected_p_value = 0.3226  

        # Assertion checks
        self.assertAlmostEqual(result['t_stat'], expected_t_stat, places=4)
        self.assertAlmostEqual(result['p_value'], expected_p_value, places=4)
        self.assertEqual(result['result'], "Fail to reject the null hypothesis (H0)")

if __name__ == '__main__':
    unittest.main()
