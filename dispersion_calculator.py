from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from pyecharts.charts import Boxplot
from pyecharts import options as opts
import pandas as pd
import numpy as np
from scipy import stats
import os


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


# Route to serve the index page
@app.route('/')
def home():
    return render_template('index.html')


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
        return redirect(url_for('home'))
    return 'Invalid file type, only CSV is allowed.', 400


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

        return render_template('boxplot.html')

    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
