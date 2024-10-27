import cv2
import tensorflow as tf

# Need Additional Requirements:
# numpy 1.23.5
# pandas 1.5.3
# tensorflow 2.18.0
# openc-python 4.10.0.84

def loaddataset():

    """Load the CIFAR-10 dataset."""

    dataset = tf.keras.datasets.cifar10.load_data()
    (X_train, y_train), (X_test, y_test) = dataset

    return X_train, y_train, X_test, y_test

def data_engineering(dataset):

    """ Do data engineering tasks on this dataset"""

    

    print(dataset)

if __name__ == "__main__":
    
    X_train, y_train, X_test, y_test = loaddataset()
    data_engineering(X_train)
    