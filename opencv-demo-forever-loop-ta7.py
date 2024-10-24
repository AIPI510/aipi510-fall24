from sklearn.datasets import fetch_openml
import numpy as np
import pandas as pd
import cv2

def load_mnist():
    '''
    Loads the MNIST dataset.

    Returns:
        tuple: A tuple containing the images and labels
            - X (numpy.ndarray): collection of 28x28 arrays representing each image in the MNIST dataset
            - y (numpy.ndarray): collection of labels
    '''
    mnist = fetch_openml('mnist_784', version=1)
    X = mnist.data.to_numpy().reshape(-1, 28, 28)  # Reshape to 28x28 images
    y = mnist.target.astype(int)
    return X,y

def harris_corners(image):
    '''
    Applies Harris corner detection.

    Returns:
        corners (numpy.ndarray): collection of 28x28 boolean arrays representing whether or not a pixel is a corner in each image
    '''
    # Convert image to float32
    gray = np.float32(image)
    # Apply Harris corner detection
    dst = cv2.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)
    # Dilate corner image to enhance corner points
    dst = cv2.dilate(dst, None)
    # Apply threshold of 0.01 to classify corner vs not a corner
    corners = dst > 0.01 * dst.max()
    return corners

def display_features(img, features):
    '''
    Displays image with overlay of Harris corner features.

    Parameters:
        - img (numpy.ndarray): 28x28 array representing an image from the MNIST dataset
        - features (numpy.ndarray): 28x28 array representing whether or not a pixel is a corner in the image
    '''
    img = cv2.cvtColor(np.float32(img), cv2.COLOR_GRAY2BGR)
    img[features] = [0, 0, 225]
    cv2.imshow('Harris Corners', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Load the MNIST dataset
X,y = load_mnist()

# Apply Harris corner detection to all images
features = np.array([harris_corners(img) for img in X])

# Create a DataFrame with the features and labels
df_features = pd.DataFrame([f.astype(int).flatten() for f in features])
df_features['label'] = y

# Display the first few rows of the DataFrame
print(df_features.head(10))

# Display one of the images with the features overlaid
display_features(X[28], features[28])
