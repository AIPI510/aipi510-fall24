import os
import sys
import argparse
import unittest
import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio
from flask import Flask, request, jsonify, render_template_string, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Function Definitions
def one_sample_t_test(sample_data, population_mean, alpha=0.05, test_type='two-sided'):
    t_stat, p_value = stats.ttest_1samp(sample_data, population_mean)

    # Adjust p-value and determine the result based on the test type
    if test_type == 'two-sided':
        adjusted_p_value = p_value
        reject_null = p_value < alpha
    elif test_type == 'left-tailed':
        adjusted_p_value = p_value / 2
        reject_null = (adjusted_p_value < alpha) and (t_stat < 0)
    elif test_type == 'right-tailed':
        adjusted_p_value = p_value / 2
        reject_null = (adjusted_p_value < alpha) and (t_stat > 0)
    else:
        raise ValueError("Unsupported test type. Choose 'two-sided', 'left-tailed', or 'right-tailed'.")

    if reject_null:
        result_str = "Reject the null hypothesis (H0). There is sufficient evidence to support the alternative hypothesis."
    else:
        result_str = "Fail to reject the null hypothesis (H0). There is not enough evidence to support the alternative hypothesis."

    return t_stat, adjusted_p_value, result_str

def visualize_interactive(sample_data, population_mean, t_stat, test_type='two-sided', alpha=0.05, return_html=False):
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Sample Data Distribution', 't-Distribution'))

    # Histogram for sample data
    fig.add_trace(
        go.Histogram(
            x=sample_data,
            nbinsx=15,
            marker_color='lightblue',
            opacity=0.75,
            name='Sample Data',
        ),
        row=1, col=1
    )

    # Add vertical lines for sample mean and population mean
    max_y_hist = max(np.histogram(sample_data, bins=15)[0]) + 5
    fig.add_trace(
        go.Scatter(
            x=[np.mean(sample_data)] * 2, y=[0, max_y_hist],
            mode='lines', line=dict(color='red', dash='dash'),
            name=f'Sample mean: {np.mean(sample_data):.2f}'
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=[population_mean] * 2, y=[0, max_y_hist],
            mode='lines', line=dict(color='blue', dash='dash'),
            name=f'Population mean: {population_mean}'
        ),
        row=1, col=1
    )

    # t-distribution and critical regions
    df = len(sample_data) - 1
    x = np.linspace(-4, 4, 500)
    y = stats.t.pdf(x, df)

    # Plot t-distribution
    fig.add_trace(
        go.Scatter(
            x=x, y=y,
            mode='lines', line=dict(color='blue'),
            name=f't-distribution (df={df})'
        ),
        row=1, col=2
    )

    # Critical regions based on the test type
    if test_type == 'two-sided':
        crit_value = stats.t.ppf(1 - alpha / 2, df)
        crit_range_left = x[x <= -crit_value]
        crit_range_right = x[x >= crit_value]

        # Shaded critical regions
        fig.add_trace(
            go.Scatter(
                x=crit_range_left, y=stats.t.pdf(crit_range_left, df),
                fill='tozeroy', mode='lines',
                line=dict(color='red'),
                name=f'Left Critical region (≤ -{crit_value:.2f})'
            ),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(
                x=crit_range_right, y=stats.t.pdf(crit_range_right, df),
                fill='tozeroy', mode='lines',
                line=dict(color='red'),
                name=f'Right Critical region (≥ {crit_value:.2f})'
            ),
            row=1, col=2
        )
    elif test_type == 'left-tailed':
        crit_value = stats.t.ppf(alpha, df)
        crit_range = x[x <= crit_value]

        fig.add_trace(
            go.Scatter(
                x=crit_range, y=stats.t.pdf(crit_range, df),
                fill='tozeroy', mode='lines',
                line=dict(color='red'),
                name=f'Critical region (≤ {crit_value:.2f})'
            ),
            row=1, col=2
        )
    elif test_type == 'right-tailed':
        crit_value = stats.t.ppf(1 - alpha, df)
        crit_range = x[x >= crit_value]

        fig.add_trace(
            go.Scatter(
                x=crit_range, y=stats.t.pdf(crit_range, df),
                fill='tozeroy', mode='lines',
                line=dict(color='red'),
                name=f'Critical region (≥ {crit_value:.2f})'
            ),
            row=1, col=2
        )

    # Add a line for the calculated t-statistic
    fig.add_trace(
        go.Scatter(
            x=[t_stat] * 2, y=[0, max(y)],
            mode='lines', line=dict(color='green', dash='dash'),
            name=f't-statistic: {t_stat:.2f}'
        ),
        row=1, col=2
    )

    # Set overall layout
    fig.update_layout(
        title_text='Interactive One-Sample t-Test Visualization',
        showlegend=True,
        height=600,
        width=1000
    )

    if return_html:
        return fig.to_html(full_html=False)
    else:
        return fig

# Flask App Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    t_stat = None
    p_value = None
    hypothesis_result = None
    interactive_plot = None

    if request.method == 'POST':
        # Get file and parameters
        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Get user inputs
        file_type = request.form['file_type']
        column_name = request.form['column_name']
        population_mean = float(request.form['population_mean'])
        alpha = float(request.form['alpha'])
        test_type = request.form['test_type']

        # Read the file
        if file_type == 'csv':
            df = pd.read_csv(file_path)
        elif file_type == 'excel':
            df = pd.read_excel(file_path)
        else:
            return "Unsupported file type"

        if column_name not in df.columns:
            return f"Column {column_name} does not exist."

        sample_data = pd.to_numeric(df[column_name], errors='coerce').dropna()
        if sample_data.empty:
            return "The selected column contains no valid data."

        # Perform t-test
        t_stat, p_value, hypothesis_result = one_sample_t_test(sample_data, population_mean, alpha, test_type)

        # Generate interactive plot
        interactive_plot = visualize_interactive(sample_data, population_mean, t_stat, test_type, alpha, return_html=True)

    return render_template_string(TEMPLATE, t_stat=t_stat, p_value=p_value, interactive_plot=interactive_plot, hypothesis_result=hypothesis_result)

@app.route('/get_columns', methods=['POST'])
def get_columns():
    file = request.files['file']
    file_type = request.form['file_type']

    if file_type == 'csv':
        df = pd.read_csv(file)
    elif file_type == 'excel':
        df = pd.read_excel(file)
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    columns = df.columns.tolist()
    return jsonify({"columns": columns})

# HTML Template
TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>One-Sample t-Test</title>
</head>
<body>
    <h1>One-Sample t-Test</h1>
    <form id="uploadForm" action="/" method="POST" enctype="multipart/form-data">
        <label for="file">Select a data file:</label>
        <input type="file" name="file" id="file" required><br><br>

        <label for="file_type">File type:</label>
        <select name="file_type" id="file_type" required>
            <option value="csv">CSV</option>
            <option value="excel">Excel</option>
        </select><br><br>

        <label for="column_name">Column name:</label>
        <select name="column_name" id="column_name" required>
            <option value="">Please upload a file first</option>
        </select><br><br>

        <label for="population_mean">Population mean:</label>
        <input type="number" step="0.01" name="population_mean" required><br><br>

        <label for="alpha">Significance level (alpha):</label>
        <input type="number" step="0.01" name="alpha" required><br><br>

        <label for="test_type">Test type:</label>
        <select name="test_type" required>
            <option value="two-sided">Two-sided test</option>
            <option value="left-tailed">Left-tailed test</option>
            <option value="right-tailed">Right-tailed test</option>
        </select><br><br>

        <button type="submit">Submit</button>
    </form>

    {% if t_stat is not none and p_value is not none %}
    <h2>Results</h2>
    <p>T-statistic: {{ t_stat }}</p>
    <p>P-value: {{ p_value }}</p>
    <p><strong>Hypothesis Result:</strong> {{ hypothesis_result }}</p>
    <h2>Visualization</h2>
    <div>{{ interactive_plot|safe }}</div>
    <br><br>
    <button id="startNewTest" type="button">Start a new test</button>
    {% endif %}

    <script>
        document.getElementById('file').addEventListener('change', function() {
            const formData = new FormData();
            const fileInput = document.getElementById('file');
            formData.append('file', fileInput.files[0]);
            formData.append('file_type', document.getElementById('file_type').value);

            fetch('/get_columns', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const columnSelect = document.getElementById('column_name');
                columnSelect.innerHTML = '';  // Clear the dropdown
                
                if (data.columns) {
                    data.columns.forEach(column => {
                        const option = document.createElement('option');
                        option.value = column;
                        option.textContent = column;
                        columnSelect.appendChild(option);
                    });
                } else {
                    columnSelect.innerHTML = '<option value="">No columns found</option>';
                }
            })
            .catch(error => {
                console.error('Error fetching column names:', error);
            });
        });

        document.getElementById('startNewTest').addEventListener('click', function() {
            location.href = "/";
        });
    </script>
</body>
</html>
'''

# Unit Tests
class TestOneSampleTTest(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        # Create sample data
        self.sample_data = pd.Series([1, 2, 3, 4, 5, 6, 7, 7, 8, 8, 8])
        self.population_mean = 5
        self.alpha = 0.05

    def test_two_sided_t_test(self):
        """Test the functionality of the two-sided one-sample t-test."""
        t_stat, p_value, result_str = one_sample_t_test(self.sample_data, self.population_mean, alpha=self.alpha, test_type='two-sided')

        print("Two-sided Test Actual t-statistic:", t_stat)
        print("Two-sided Test Actual p-value:", p_value)

        expected_t_stat = 0.4747
        expected_p_value = 0.6452

        self.assertAlmostEqual(t_stat, expected_t_stat, places=3)
        self.assertAlmostEqual(p_value, expected_p_value, places=3)
        self.assertEqual(result_str, "Fail to reject the null hypothesis (H0). There is not enough evidence to support the alternative hypothesis.")

    def test_left_tailed_t_test(self):
        """Test the functionality of the left-tailed one-sample t-test."""
        t_stat, p_value, result_str = one_sample_t_test(self.sample_data, self.population_mean, alpha=self.alpha, test_type='left-tailed')

        print("Left-tailed Test Actual t-statistic:", t_stat)
        print("Left-tailed Test Actual p-value:", p_value)

        expected_t_stat = 0.4747
        expected_p_value = 0.3226

        self.assertAlmostEqual(t_stat, expected_t_stat, places=3)
        self.assertAlmostEqual(p_value, expected_p_value, places=3)
        self.assertEqual(result_str, "Fail to reject the null hypothesis (H0). There is not enough evidence to support the alternative hypothesis.")

    def test_right_tailed_t_test(self):
        """Test the functionality of the right-tailed one-sample t-test."""
        t_stat, p_value, result_str = one_sample_t_test(self.sample_data, self.population_mean, alpha=self.alpha, test_type='right-tailed')

        print("Right-tailed Test Actual t-statistic:", t_stat)
        print("Right-tailed Test Actual p-value:", p_value)

        expected_t_stat = 0.4747
        expected_p_value = 0.3226

        self.assertAlmostEqual(t_stat, expected_t_stat, places=3)
        self.assertAlmostEqual(p_value, expected_p_value, places=3)
        self.assertEqual(result_str, "Fail to reject the null hypothesis (H0). There is not enough evidence to support the alternative hypothesis.")

# Main Execution
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask app, unit tests, or main execution.')
    parser.add_argument('mode', choices=['flask', 'test', 'main'], help='Mode to run: flask, test, or main')

    args = parser.parse_args()

    if args.mode == 'flask':
        app.run(debug=True)
    elif args.mode == 'test':
        unittest.main(argv=[sys.argv[0]])
    elif args.mode == 'main':
        # Example data for testing
        sample_data = np.array([1, 2, 3, 4, 5, 6, 7, 7, 8, 8, 8])
        population_mean = 5
        alpha = 0.05
        test_type = 'two-sided'

        # Perform the one-sample t-test
        t_stat, p_value, result_str = one_sample_t_test(sample_data, population_mean, alpha=alpha, test_type=test_type)

        print("T-statistic:", t_stat)
        print("P-value:", p_value)
        print("Result:", result_str)

        # Visualize the results
        fig = visualize_interactive(sample_data, population_mean, t_stat, test_type=test_type, alpha=alpha, return_html=False)
        fig.show()
