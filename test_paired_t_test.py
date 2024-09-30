import unittest
import pandas as pd
from paired_t_test import DataAnalyzer
from scipy import stats
import logging

class TestDataAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = DataAnalyzer('prem.csv')
        self.analyzer.preprocess_data()

    # Test that data is preprocessed correctly
    def test_preprocess_data(self):
        
        
        t_data_shape = self.analyzer.t_data.shape

        # Check if the shape is correct, should have 6 columns after preprocessing
        self.assertEqual(t_data_shape[1], 6)  
        # Check if 'diff' column is created
        self.assertIn('diff', self.analyzer.t_data.columns)

    # Test that outliers are handled correctly
    def test_handle_outliers(self):
        
        # Handle outliers
        self.analyzer.handle_outliers()

        # Ensure there are no outliers
        Q1 = self.analyzer.t_data['diff'].quantile(0.25)
        Q3 = self.analyzer.t_data['diff'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        self.assertTrue((self.analyzer.t_data['diff'] >= lower_bound).all())
        self.assertTrue((self.analyzer.t_data['diff'] <= upper_bound).all())

    # Test the results 
    def test_results(self):
        
        t_stat, p_value = self.analyzer.t_test()

        # Capture the printed output using a context manager
        with self.assertLogs(level='INFO') as log:
            self.analyzer.results(p_value)

        # Check the printed results based on the p_value
        if p_value < 0.05:
            self.assertIn("The means of the two samples are different", log.output[0])
        else:
            self.assertIn("The means of the two samples are equal.", log.output[0])


    
if __name__ == "__main__":
    unittest.main()
