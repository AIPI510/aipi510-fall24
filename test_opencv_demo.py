import unittest
import numpy as np
from torchvision import datasets, transforms
from opencv_demo import calculate_color_histogram, calculate_texture_description, detect_edges

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
    unittest.main()