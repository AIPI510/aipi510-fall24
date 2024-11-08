import os
import numpy as np
import pandas as pd
from scipy import stats
from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from flask_cors import CORS
from pyecharts.charts import Boxplot
from pyecharts import options as opts
import unittest
import tempfile

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

# Ensure uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HTML template for the main page
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Dispersion Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f4f4f9;
            color: #333;
        }

        input, button {
            padding: 10px;
            margin-top: 10px;
        }

        button {
            cursor: pointer;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
        }

        button:hover {
            background-color: #0056b3;
        }

        #results p {
            margin-top: 20px;
        }

        h1 {
            color: #333;
        }
    </style>
</head>
<body>
    <h1>Data Dispersion Calculator</h1>
    
    <!-- Upload dataset form -->
    <form id="uploadForm" onsubmit="uploadFile(event)">
        <label for="file">Upload your CSV file:</label>
        <input type="file" name="file" id="file" accept=".csv">
        <button type="submit">Upload File</button>
    </form>

    <div>
        <label for="dataInput">Enter Column Name:</label>
        <input type="text" id="dataInput" placeholder="e.g., height">
        <button onclick="calculateDispersion()">Calculate</button>
        <button onclick="generateBoxPlot()">Generate Box Plot</button>
    </div>

    <div id="results">
        <p id="standardDeviation">Standard Deviation:</p>
        <p id="variance">Variance:</p>
        <p id="range">Range:</p>
        <p id="interquartileRange">Interquartile Range:</p>
    </div>
    
    <script>
        function uploadFile(event) {
            event.preventDefault();  // Prevent the form from submitting in the traditional way

            const formData = new FormData();
            const fileInput = document.getElementById('file');
            const file = fileInput.files[0];
            
            if (!file) {
                alert("Please select a file first.");
                return;
            }

            formData.append('file', file);

            fetch('http://127.0.0.1:5001/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const uploadStatus = document.getElementById('uploadStatus');
                uploadStatus.textContent = data.message;

                if (data.message === "File uploaded successfully") {
                    uploadStatus.style.color = "green";
                } else {
                    uploadStatus.style.color = "red";
                }
            })
            .catch(error => {
                console.error('Error:', error);
                const uploadStatus = document.getElementById('uploadStatus');
                uploadStatus.textContent = "File upload failed.";
                uploadStatus.style.color = "red";
            });
        }

        function calculateDispersion() {
            const columnName = document.getElementById('dataInput').value;

            if (!columnName) {
                alert("Please enter a column name.");
                return;
            }

            fetch(`http://127.0.0.1:5001/calculate?column=${columnName}`)
                .then(response => {
                    console.log('Response Status:', response.status);
                    if (!response.ok) {
                        throw new Error('Request failed, please check the column name.');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Data received:', data);
                    if (data.error) {
                        alert(data.error);
                        return;
                    }

                    document.getElementById('standardDeviation').innerText = 'Standard Deviation: ' + data.standard_deviation.toFixed(2);
                    document.getElementById('variance').innerText = 'Variance: ' + data.variance.toFixed(2);
                    document.getElementById('range').innerText = 'Range: ' + data.range.toFixed(2);
                    document.getElementById('interquartileRange').innerText = 'Interquartile Range: ' + data.interquartile_range.toFixed(2);
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Failed to calculate. Make sure the API is running and the column name is correct.');
                });
        }

        function generateBoxPlot() {
            const columnName = document.getElementById('dataInput').value;

            if (!columnName) {
                alert("Please enter a column name.");
                return;
            }

            window.location.href = `http://127.0.0.1:5001/boxplot?column=${columnName}`;
        }
    </script>
</body>
</html>
"""

# Route to serve the index page
@app.route('/')
def home():
    return render_template_string(html_template)

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv')
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully"})
    return jsonify({"message": "Invalid file type, only CSV is allowed."}), 400

# Route to calculate measures of dispersion
@app.route('/calculate', methods=['GET'])
def calculate_measures():
    try:
        data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv'))  # Path to your uploaded CSV file
        column_name = request.args.get('column', default='data', type=str)  # Get column name

        if column_name not in data.columns:
            return jsonify({"error": "Column not found"}), 404

        data_values = data[column_name].dropna().to_numpy()

        measures = {
            "standard_deviation": float(np.std(data_values, ddof=1)),
            "variance": float(np.var(data_values, ddof=1)),
            "range": float(np.max(data_values) - np.min(data_values)),
            "interquartile_range": float(stats.iqr(data_values))
        }

        return jsonify(measures)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to generate the box plot
@app.route('/boxplot', methods=['GET'])
def generate_boxplot():
    try:
        data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv'))  # Path to your uploaded CSV file
        column_name = request.args.get('column', default='data', type=str)

        if column_name not in data.columns:
            return "Column not found", 404

        data_values = data[column_name].dropna().tolist()

        # Create Boxplot using pyecharts
        boxplot = Boxplot()
        boxplot.add_xaxis([column_name])
        boxplot_data = [data_values]
        boxplot.add_yaxis("Boxplot", boxplot.prepare_data(boxplot_data))
        boxplot.set_global_opts(title_opts=opts.TitleOpts(title="Boxplot of {}".format(column_name)))

        # Save the boxplot as an HTML file
        boxplot_path = os.path.join('templates', 'boxplot.html')
        boxplot.render(boxplot_path)

        return render_template_string(open(boxplot_path).read())

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

# Unit tests for dispersion analysis functions
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

# Unit tests for Flask API
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
            self.assertEqual(response.status_code, 200)  # Expecting success response

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
        self.assertIn("Boxplot of data", response.get_data(as_text=True))  # Check if the generated HTML contains the title of the boxplot

if __name__ == '__main__':
    unittest.main()
