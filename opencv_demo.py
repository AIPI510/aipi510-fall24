import cv2
import numpy as np
from torchvision import datasets, transforms
from skimage.feature import local_binary_pattern
import matplotlib.pyplot as plt
import unittest
import sys

# Main functions
def calculate_color_histogram(image):
    # Calculate the color histogram for each channel (R, G, B) of the image
    channels = ('r', 'g', 'b')
    hist = {}
    for i, color in enumerate(channels):
        hist[color] = cv2.calcHist([image], [i], None, [256], [0, 256])
    return hist

def calculate_texture_description(image):
    # Calculate texture description using LBP
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Parameters for LBP
    radius = 1
    n_points = 8 * radius

    # Compute LBP
    lbp = local_binary_pattern(gray_image, n_points, radius, method='uniform')

    # Compute the histogram of LBP
    lbp_hist, _ = np.histogram(lbp, bins=np.arange(0, n_points + 3), density=True)
    
    return lbp_hist

def detect_edges(image, low_threshold=30, high_threshold=100):
    # Detect edges using the Canny edge detection method
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray_image, low_threshold, high_threshold)
    return edges

def main():
    # Load CIFAR-10 dataset
    transform = transforms.Compose([transforms.ToTensor()])
    cifar = datasets.CIFAR10(root="./data", train=True, download=True, transform=transform)

    # Select a sample image and label
    sample_image, sample_label = cifar[0]

    # Convert the image to a format compatible with OpenCV (H, W, C) and scale to [0, 255]
    sample_image = (sample_image.numpy() * 255).astype(np.uint8).transpose(1, 2, 0)

    # Calculate color histograms
    color_hist = calculate_color_histogram(sample_image)

    # Calculate texture description
    texture_descriptors = calculate_texture_description(sample_image)

    # Detect edges
    edges = detect_edges(sample_image)

    # Plot results
    plt.figure(figsize=(12, 8))

    # Original image
    plt.subplot(2, 2, 1)
    plt.imshow(sample_image)
    plt.title('Original Image')

    # Color histograms
    plt.subplot(2, 2, 2)
    for color, hist in color_hist.items():
        plt.plot(hist, color=color)
    plt.xlim([0, 256])
    plt.title('Color histograms')

    # Texture description
    plt.subplot(2, 2, 3)
    plt.bar(range(len(texture_descriptors)), texture_descriptors)
    plt.title('Texture Descriptors (LBP)')

    # Edge detection
    plt.subplot(2, 2, 4)
    plt.imshow(edges, cmap="gray")
    plt.title("Edges")

    plt.tight_layout()
    plt.show()

# Unit tests
class TestOpencv(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load CIFAR-10 dataset
        transform = transforms.Compose([transforms.ToTensor()])
        cifar = datasets.CIFAR10(root="./data", train=True, download=True, transform=transform)
        
        # Select a sample image and convert the image to a format compatible with OpenCV (H, W, C) and scale to [0, 255]
        sample_image, _ = cifar[0]
        cls.image = (sample_image.numpy() * 255).astype(np.uint8).transpose(1, 2, 0)

    def test_calculate_color_histogram(self):
        # Test if the function returns a dictionary with expected keys
        hist = calculate_color_histogram(self.image)
        self.assertIsInstance(hist, dict)
        self.assertEqual(set(hist.keys()), {'r', 'g', 'b'})

    def test_calculate_texture_description(self):
        # Test if the function returns an array of expected length
        texture_descriptor = calculate_texture_description(self.image)
        self.assertIsInstance(texture_descriptor, np.ndarray)

    def test_detect_edges(self):
        # Test if the function returns an edge-detected image of the correct shape
        edges = detect_edges(self.image)
        self.assertIsInstance(edges, np.ndarray)
        self.assertEqual(edges.shape, self.image.shape[:2])

if __name__ == "__main__":
    if '--test' in sys.argv:
        # Run unit tests if the --test flag is provided
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        # Run the main function
        main()
