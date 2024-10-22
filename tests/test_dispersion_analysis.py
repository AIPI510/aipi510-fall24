import unittest
from dispersion_analysis import (
    calculate_variance,
    calculate_standard_deviation,
    calculate_iqr,
    calculate_range
)


class TestDispersionCalculations(unittest.TestCase):

    def setUp(self):
        """Set up sample data for tests."""
        self.data = [10, 12, 23, 23, 16, 23, 21, 16]

    def test_variance(self):
        """Test variance calculation."""
        result = calculate_variance(self.data)
        expected = 27.428571428571427
        self.assertAlmostEqual(result, expected, places=5)

    def test_standard_deviation(self):
        """Test standard deviation calculation."""
        result = calculate_standard_deviation(self.data)
        expected = 5.237229365663817
        self.assertAlmostEqual(result, expected, places=5)

    def test_iqr(self):
        """Test interquartile range (IQR) calculation."""
        result = calculate_iqr(self.data)
        expected = 9.0
        self.assertAlmostEqual(result, expected, places=5)

    def test_range(self):
        """Test range calculation."""
        result = calculate_range(self.data)
        expected = 13
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
