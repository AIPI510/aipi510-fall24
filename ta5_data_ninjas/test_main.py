import unittest
import numpy as np
from ta5_data_ninjas_main import stat_std_moment, moment, stat_mean

class TestHelperFunctions(unittest.TestCase):

    def setUp(self):
        # Setup common variables for tests
        self.x = np.linspace(-5, 5, 1000)
        self.delta_x = (self.x[-1] - self.x[0]) / len(self.x)
        self.y = (1 / np.sqrt(2 * np.pi * 1)) * np.exp(-0.5 * (self.x ** 2))  # Standard normal distribution

    def test_stat_mean(self):
        mean = stat_mean(self.x, self.y, self.delta_x)
        expected_mean = 0  # Mean of standard normal distribution
        self.assertAlmostEqual(round(mean,2), expected_mean, places=2, msg="Mean calculation is incorrect")

    def test_moment(self):
        # Test second moment (variance)
        variance = moment(self.x, self.y, self.delta_x, 2)
        expected_variance = 1  # Variance of standard normal distribution
        self.assertAlmostEqual(round(variance), expected_variance, places=2, msg="second moment calculation is incorrect")
        
        # Test third moment E[(X-mean)^3]
        skewness = moment(self.x, self.y, self.delta_x, 3)
        expected_skewness = 0  # third moment of standard normal distribution
        self.assertAlmostEqual(round(skewness), expected_skewness, places=2, msg="third moment calculation is incorrect")
        
        # Test fourth moment E[(X-mean)^3]
        kurtosis = moment(self.x, self.y, self.delta_x, 4)
        expected_kurtosis = 3  # fourth moment of standard normal distribution (excess kurtosis is 0)
        self.assertAlmostEqual(round(kurtosis), expected_kurtosis, places=2, msg="fourth moment calculation is incorrect")

    def test_stat_std_moment(self):
        # Test skewness 
        skewness = stat_std_moment(self.x, self.y, self.delta_x, 3)
        expected_skewness = 0  # Skewness of standard normal distribution
        self.assertAlmostEqual(round(skewness), expected_skewness, places=2, msg="Skewness calculation is incorrect")
        
        # Test kurtosis
        kurtosis = stat_std_moment(self.x, self.y, self.delta_x, 4)
        expected_kurtosis = 3  # Excess kurtosis of standard normal distribution
        self.assertAlmostEqual(round(kurtosis), expected_kurtosis, places=2, msg="Kurtosis calculation is incorrect")
