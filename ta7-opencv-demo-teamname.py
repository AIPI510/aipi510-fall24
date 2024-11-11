import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os

import pytest

def loaddataset():

    """
    Load the CIFAR-10 dataset using TensorFlow.
    
    Ouput:
        X_train: The training dataset.
        y_train: The training labels.
        X_test: The testing dataset.
        y_test: The testing labels
    """

    dataset = tf.keras.datasets.cifar10.load_data()
    (X_train, y_train), (X_test, y_test) = dataset

    return X_train, y_train, X_test, y_test

def data_visualization(dataset, index):

    """
    Visualize one picture in the dataset.
    
    Input:
        dataset: The dataset to be visualized.
        index: The index of the picture to be visualized.

    """

    image = dataset[index]

    plt.imshow(image)

    plt.axis('off')

    plt.show()


def resize_images(images, width, height):

    """
    Resize the image to the specified width and height.
    
    Input:
        images: The images to be resized.
        width: The width of the resized images.
        height: The height of the resized images.

    Output:
        resized_images: The resized images.
    """

    resized_images = [cv2.resize(image, (width, height)) for image in images]

    return np.array(resized_images)

def normailize_images(images):

    """
    Normalize the image.

    Input:
        images: The images to be normalized.
    
    Output:
        images: The normalized images.
    """

    return np.array(images / 255.0)

def flip_images(images):

    """
    Flip the image horizontally.
    
    Input:
        images: The images to be flipped.

    Ouput:
        fliped_images: The fliped images.
    """

    fliped_images = [cv2.flip(image, 1) for image in images]

    return np.array(fliped_images)

def rotate_images(images, angle):

    """
    Rotate the image.

    Input:
        images: The images to be rotated.
        angle: The angle to rotate the images.

    Output:
        rotated_images: The rotated images.
    """

    h, w = images.shape[1:3]

    rotation_matrix = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)

    rotated_images = [cv2.warpAffine(image, rotation_matrix, (w, h)) for image in images]

    return np.array(rotated_images)


def data_engineering(dataset):

    """ 
    Do data engineering tasks on this dataset And Visualize one image after each data engineering step.
        
    Input:
        dataset: The dataset for data engineering.

    """

    # Show the visualized data before data engineering

    data_visualization(dataset, 0)

    # Resize the images

    resized_dataset = resize_images(dataset, 100, 100)

    # Show the visualized data after resizing

    data_visualization(resized_dataset, 0)

    # Normalize the images

    normalized_dataset = normailize_images(dataset)

    # Show the visualized data after normalizing

    data_visualization(normalized_dataset, 0)

    # Flip the images

    fliped_dataset = flip_images(dataset)

    # Show the visualized data after flipping

    data_visualization(fliped_dataset, 0)

    # Rotate the images

    rotated_dataset = rotate_images(dataset, 45)

    # Show the visualized data after rotating

    data_visualization(rotated_dataset, 0)

if __name__ == "__main__":
    
    # Disable oneDNN custom operations in TensorFlow
    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

    X_train, y_train, X_test, y_test = loaddataset()

    data_engineering(X_train)
    
@pytest.fixture
def sample_data():

    """Load a subset of images for testing."""

    X_train, _, _, _ = loaddataset()
    return X_train[:5]  # Using a subset of images for testing

def test_loaddataset():

    """Test loading the CIFAR-10 dataset."""

    X_train, y_train, X_test, y_test = loaddataset()
    assert X_train.shape == (50000, 32, 32, 3)
    assert X_test.shape == (10000, 32, 32, 3)
    assert y_train.shape == (50000, 1)
    assert y_test.shape == (10000, 1)

def test_resize_images(sample_data):

    """Test resizing images to new dimensions."""

    resized_images = resize_images(sample_data, 64, 64)
    assert all(img.shape == (64, 64, 3) for img in resized_images)

def test_normalize_images(sample_data):

    """Test normalization of images."""

    normalized_images = normailize_images(sample_data)
    assert np.all((normalized_images >= 0) & (normalized_images <= 1))

def test_flip_images(sample_data):

    """Test flipping images horizontally."""

    flipped_images = flip_images(sample_data)
    for original, flipped in zip(sample_data, flipped_images):
        assert np.array_equal(original[:, ::-1], flipped)

def test_rotate_images(sample_data):

    """Test rotating images by a specified angle."""

    rotated_images = rotate_images(sample_data, 45)  # Rotate by 45 degrees

    assert all(img.shape == (32, 32, 3) for img in rotated_images)  # Check if dimensions are retained