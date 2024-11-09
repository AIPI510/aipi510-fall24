# import awsgi

# # import pandas as pd 
# import numpy as np
# import os
# import cv2 

# from sklearn.svm import SVC
# from sklearn.preprocessing import StandardScaler
# from sklearn.pipeline import make_pipeline

# import joblib 

# from flask import Flask, request, render_template, flash, redirect, url_for
# from werkzeug.utils import secure_filename

# def load_images(folder):
#     images = []  
#     labels = []  

#     for subfolder in os.listdir(folder):
#         subfolder_path = os.path.join(folder, subfolder)

#         if subfolder == 'dogs':
#             label = 1
#         else:
#             label = 0

#         for imagelist in os.listdir(subfolder_path):
#             if imagelist.endswith(('.jpg', '.jpeg', '.png')):
#                 image_path = os.path.join(subfolder_path, imagelist)
#                 image = cv2.imread(image_path)
#                 image = cv2.resize(image, (64, 64))
#                 images.append(image)
#                 labels.append(label)

#     return np.array(images), np.array(labels)

# X_train, y_train = load_images(f"CatvsDog/train")
# X_test, y_test = load_images(f"CatvsDog/test")

# X_train = X_train.reshape(X_train.shape[0], -1)
# X_test = X_test.reshape(X_test.shape[0], -1)

# X_combined = np.concatenate((X_train, X_test), axis=0)
# y_combined = np.concatenate((y_train, y_test), axis=0)

# svm_model = make_pipeline(StandardScaler(), SVC(kernel='linear', random_state=0))
# svm_model.fit(X_combined, y_combined)

# joblib.dump(svm_model, 'model.joblib')

# model = joblib.load('model.joblib')

# app = Flask(__name__)
# app.secret_key = 'supersecretkey'  # Required for flashing messages

# # Configure upload folder
# UPLOAD_FOLDER = 'static/uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# # Create upload folder if it doesn't exist
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def preprocess_image(image_path):
#     # Load and preprocess the image
#     image = cv2.imread(image_path)
#     image = cv2.resize(image, (64, 64))
#     image = image.flatten()  # Flatten the image for the model
#     return np.array([image])  # Return as a 2D array

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     prediction = None
#     if request.method == 'POST':
#         # Check if any file was uploaded
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
        
#         # If no file was selected
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
        
#         # If file is valid and allowed
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)

#             # Preprocess the uploaded image
#             processed_image = preprocess_image(file_path)
#             # Make prediction
#             prediction = model.predict(processed_image)[0]
#             prediction_label = "Dog" if prediction == 1 else "Cat"

#             return render_template('upload.html', 
#                                    message='File uploaded successfully!',
#                                    image_path=os.path.join('uploads', filename),
#                                    prediction=prediction_label)
    
#     return render_template('upload.html', prediction=prediction)

# # # Add this part to make the server run
# # if __name__ == "__main__":
# #     app.run(host='0.0.0.0', port=5000)

# def lambda_handler(event,context):
#     return awsgi.response(app, event, context, base64_content_types={"image/png"})


import awsgi

import os
import cv2
import joblib
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# Flask app setup
app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (64, 64))
    image = image.flatten().reshape(1, -1)  # Reshape for prediction
    return image

# Loading images function
def load_images(folder):
    images, labels = [], []
    for subfolder in os.listdir(folder):
        label = 1 if subfolder == 'dogs' else 0
        for imagelist in os.listdir(os.path.join(folder, subfolder)):
            if imagelist.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(folder, subfolder, imagelist)
                image = cv2.imread(image_path)
                image = cv2.resize(image, (64, 64))
                images.append(image.flatten())  # Flatten image for model
                labels.append(label)
    return images, labels

X_train, y_train = load_images("CatvsDog/train")
X_test, y_test = load_images("CatvsDog/test")
X_combined = X_train + X_test
y_combined = y_train + y_test

# Model setup
svm_model = make_pipeline(StandardScaler(), SVC(kernel='linear', random_state=0))
svm_model.fit(X_combined, y_combined)

joblib.dump(svm_model, 'model.joblib')

model = joblib.load('model.joblib')


# Flask routes
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    prediction = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            processed_image = preprocess_image(file_path)
            prediction = model.predict(processed_image)[0]
            prediction_label = "Dog" if prediction == 1 else "Cat"

            return render_template('upload.html',
                                   message='File uploaded successfully!',
                                   image_path=os.path.join('uploads', filename),
                                   prediction=prediction_label)
        else:
            flash('Invalid file format or no file uploaded')
            return redirect(request.url)

    return render_template('upload.html', prediction=prediction)

# # Uncomment to run locally
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)

def lambda_handler(event,context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})


