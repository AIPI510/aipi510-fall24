import os
import unittest
import tempfile
import pandas as pd
from dispersion_calculator import app


class DispersionApiTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test environment."""
        self.app = app.test_client()
        self.app.testing = True

        # Create a temporary directory for uploading files
        self.temp_upload_folder = tempfile.mkdtemp()
        app.config['UPLOAD_FOLDER'] = self.temp_upload_folder

        # Create a sample CSV file
        self.sample_data = pd.DataFrame({
            'data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        })
        self.sample_csv_path = os.path.join(self.temp_upload_folder, 'data.csv')
        self.sample_data.to_csv(self.sample_csv_path, index=False)

    def tearDown(self):
        """Clean up the test environment."""
        # Delete all files in the temporary upload directory
        for filename in os.listdir(self.temp_upload_folder):
            file_path = os.path.join(self.temp_upload_folder, filename)
            os.remove(file_path)

        # Delete the temporary upload directory
        os.rmdir(self.temp_upload_folder)

    def test_file_upload(self):
        """Test file upload functionality."""
        with open(self.sample_csv_path, 'rb') as file:
            response = self.app.post('/upload', data={'file': file}, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful upload

    def test_calculate_measures(self):
        """Test calculate measures functionality."""
        # First, upload the file
        with open(self.sample_csv_path, 'rb') as file:
            self.app.post('/upload', data={'file': file}, content_type='multipart/form-data')

        # Then, calculate measures for the 'data' column
        response = self.app.get('/calculate?column=data')
        self.assertEqual(response.status_code, 200)

        expected_measures = {
            "standard_deviation": self.sample_data['data'].std(ddof=1),
            "variance": self.sample_data['data'].var(ddof=1),
            "range": self.sample_data['data'].max() - self.sample_data['data'].min(),
            "interquartile_range": self.sample_data['data'].quantile(0.75) - self.sample_data['data'].quantile(0.25)
        }

        data = response.get_json()

        # Check if calculated values are approximately equal to expected values
        self.assertAlmostEqual(data['standard_deviation'], expected_measures['standard_deviation'], places=2)
        self.assertAlmostEqual(data['variance'], expected_measures['variance'], places=2)
        self.assertAlmostEqual(data['range'], expected_measures['range'], places=2)
        self.assertAlmostEqual(data['interquartile_range'], expected_measures['interquartile_range'], places=2)

    def test_generate_boxplot(self):
        """Test boxplot generation functionality."""
        # First, upload the file
        with open(self.sample_csv_path, 'rb') as file:
            self.app.post('/upload', data={'file': file}, content_type='multipart/form-data')

        # Then, generate box plot for the 'data' column
        response = self.app.get('/boxplot?column=data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Boxplot of data", response.data)  # Check if the generated HTML contains the title of the boxplot


if __name__ == '__main__':
    unittest.main()
