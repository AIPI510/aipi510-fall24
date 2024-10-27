from sklearn.datasets import fetch_openml
import numpy as np
import pandas as pd
import cv2

def load_mnist(fetch_openml=fetch_openml):
    '''
    Loads the MNIST dataset.

    Parameter:
        - fetch_openml (function): Mockable function to call in order to load MNIST data (default: sklearn.datasets.fetch_openml)

    Returns:
        tuple: A tuple containing the images and labels
            - X (numpy.ndarray): collection of 28x28 arrays representing each image in the MNIST dataset
            - y (numpy.ndarray): collection of labels
    '''
    mnist = fetch_openml('mnist_784', version=1, parser='auto')
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

def display_features(img, features, imshow=cv2.imshow, waitKey=cv2.waitKey, destroyAllWindows=cv2.destroyAllWindows):
    '''
    Displays image with overlay of Harris corner features.

    Parameters:
        - img (numpy.ndarray): 28x28 array representing an image from the MNIST dataset
        - features (numpy.ndarray): 28x28 array representing whether or not a pixel is a corner in the image
        - imshow (function): Mockable function to call in order to show an image (default: cv2.imshow)
        - waitKey (function): Mockable function to call in order to wait for a keypress (default: cv2.waitKey)
        - destroyAllWindows (function): Mockable function to call in order to destroy the opened image windows (default: cv2.destroyAllWindows)
    '''
    img = cv2.cvtColor(np.float32(img), cv2.COLOR_GRAY2BGR)
    img[features] = [0, 0, 225]
    imshow('Harris Corners', img)
    waitKey(0)
    destroyAllWindows()

def main():
    '''
    Entrypoint function to run the script.
    '''
    # Load the MNIST dataset
    print('Loading MNIST dataset...')
    X,y = load_mnist()

    # Apply Harris corner detection to all images
    print('Applying OpenCV Harris Corners feature detection...')
    features = np.array([harris_corners(img) for img in X])

    # Create a DataFrame with the features and labels
    df_features = pd.DataFrame([f.astype(int).flatten() for f in features])
    df_features['label'] = y

    # Display the first few rows of the DataFrame
    print('First few rows of the feature dataframe:')
    print(df_features.head(10))

    # Display one of the images with the features overlaid
    print('\nDisplaying example of one of the images with the features overlaid. Press any key to close...')
    display_features(X[28], features[28])

if __name__ == '__main__':
    main()

### UNIT TESTS ###
import unittest
from unittest.mock import patch, MagicMock, ANY

class TestFunctions(unittest.TestCase):
    
    @patch('sklearn.datasets.fetch_openml')
    def test_load_mnist_succeeds(self, mock_fetch_openml):
        load_mnist(mock_fetch_openml)
        mock_fetch_openml.assert_called_once_with('mnist_784', version=1, parser='auto')

    @patch('sklearn.datasets.fetch_openml')
    def test_load_mnist_fails(self, mock_fetch_openml):
        mock_fetch_openml.side_effect = Exception('Failed to load dataset.')
        with self.assertRaises(Exception):
            load_mnist(mock_fetch_openml)
        mock_fetch_openml.assert_called_once_with('mnist_784', version=1, parser='auto')

    def test_harris_corners_wrong_input_type(self):
        with self.assertRaises(ValueError):
            harris_corners('waffle')

    def test_harris_corners_happy_case(self):
        features = harris_corners(np.zeros((100, 100)))
        self.assertEqual(features.shape, (100, 100))

    @patch('cv2.imshow')
    @patch('cv2.waitKey')
    @patch('cv2.destroyAllWindows')
    def test_display_features_fails_at_imshow(self, mock_destroyAllWindows, mock_waitKey, mock_imshow):
        mock_imshow.side_effect = Exception('Failed to show image.')
        img = np.zeros((100, 100))
        with self.assertRaises(Exception):
            display_features(img, harris_corners(img), imshow=mock_imshow, waitKey=mock_waitKey, destroyAllWindows=mock_destroyAllWindows)
        mock_imshow.assert_called_once_with(ANY, ANY)
        mock_waitKey.assert_not_called()
        mock_destroyAllWindows.assert_not_called()

    @patch('cv2.imshow')
    @patch('cv2.waitKey')
    @patch('cv2.destroyAllWindows')
    def test_display_features_succeeds(self, mock_destroyAllWindows, mock_waitKey, mock_imshow):
        img = np.zeros((100, 100))
        display_features(img, harris_corners(img), imshow=mock_imshow, waitKey=mock_waitKey, destroyAllWindows=mock_destroyAllWindows)
        mock_imshow.assert_called_once_with(ANY, ANY)
        mock_waitKey.assert_called_once_with(0)
        mock_destroyAllWindows.assert_called_once()
