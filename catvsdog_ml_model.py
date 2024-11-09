# https://www.kaggle.com/datasets/samuelcortinhas/cats-and-dogs-image-classification/data

import pandas as pd
import numpy as np
import os
import cv2 

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
# from sklearn.metrics import accuracy_score

def load_images(folder):
    images = []  
    labels = []  

    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)

        if subfolder == 'dogs':
            label = 1
        else:
            label = 0

        for imagelist in os.listdir(subfolder_path):
            if imagelist.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(subfolder_path, imagelist)
                image = cv2.imread(image_path)
                image = cv2.resize(image, (64, 64))
                images.append(image)
                labels.append(label)

    return np.array(images), np.array(labels)

X_train, y_train = load_images(f"CatvsDog/train")
X_test, y_test = load_images(f"CatvsDog/test")

X_prueba, y_prueba = load_images(f"CatvsDog/prueba")

X_train = X_train.reshape(X_train.shape[0], -1)
X_test = X_test.reshape(X_test.shape[0], -1)

X_combined = np.concatenate((X_train, X_test), axis=0)
y_combined = np.concatenate((y_train, y_test), axis=0)

X_prueba = X_prueba.reshape(X_prueba.shape[0], -1)

svm_model = make_pipeline(StandardScaler(), SVC(kernel='linear', random_state=0))
svm_model.fit(X_combined, y_combined)

# Make predictions on the test set
svm_predictions = svm_model.predict(X_prueba)

print(svm_predictions)

# accuracy_svm = accuracy_score(y_test, svm_predictions)

# print(accuracy_svm)