
"""

The library that we've chosen to explore is called scikit-image.
It's an alternative to Opencv and it's an open source project.
The dataset that we've chosen to work on is that of the faces and non-faces dataset.
The data exploration is done by selecting a subset of this dataset. This was deemed ideal since all the feature-extractions can be displayed through just a single image.
The subset chosen is that of the first 4 images, which in this case would be just the faces, but blurred.

"""
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, filters, morphology, feature, color, util
from skimage.transform import rescale
from skimage.feature import blob_log
import cv2


#function to create the subplot.
def create_subplot(rows, cols, figsize=(20, 20)):
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    fig.tight_layout(pad=3.0)
    return fig, axes

#function to display the images
def display_image(ax, image, title):
    """
    takes the ax, image and title as the input and shows the image as the output.
    here we set cmap = "gray" because since all the images in the dataset are grey, and setting it without the gray factor,
    throws in an input error for some of the operations because.
    Also without `cmap='gray'`, grayscale images may be displayed incorrectly, 
    often with misleading colors, as matplotlib defaults to displaying images in RGB color if no colormap is specified.
    """
    if image.ndim == 2:
        ax.imshow(image, cmap='gray')
    else:
        ax.imshow(image)
    ax.set_title(title)
    ax.axis('off')

def process_single_image(image, operation_name):
    """
    Takes in the iamge and the operation to be performed
    Apply a single operation to an image and return the result and this can be repeated for other images using a loop.

    Some operations, such as erosion, dilation, canny edge detection, and skeletonization, are typically applied to grayscale images. 
    The check for `image.ndim == 3` ensures that if the image is in RGB format, it is first converted to grayscale before performing these operations.
    For operations that don't specifically require grayscale (like flipping or adding noise), this check is not necessary.
    x
    """
    if operation_name == "grayscale":
    # Converts to grayscale only if the image has three color channels (RGB).
        return color.rgb2gray(image) if image.ndim == 3 else image
    elif operation_name == "rescale":
    # Rescales the image to half its size with anti-aliasing for smoother scaling.
        return rescale(image, scale=0.5, anti_aliasing=True)
    elif operation_name == "flip":
    # Flips the image horizontally; works for both grayscale and RGB images.
        return np.fliplr(image)
    elif operation_name == "noise":
    # Adds Gaussian noise; applies to both grayscale and RGB images.
        return util.random_noise(image, mode='gaussian')
    elif operation_name == "erosion":
    # Erosion is generally used on binary or grayscale images for edge detection or thinning.
        gray = color.rgb2gray(image) if image.ndim == 3 else image
        return morphology.erosion(gray)
    elif operation_name == "dilation":
    # Dilation is often applied to grayscale or binary images to expand white areas.
        gray = color.rgb2gray(image) if image.ndim == 3 else image
        return morphology.dilation(gray)
    elif operation_name == "canny":
    # Canny edge detection requires a grayscale image as input.
        gray = color.rgb2gray(image) if image.ndim == 3 else image
        return feature.canny(gray)
    elif operation_name == "blur":
    # Applies Gaussian blurring; works on both grayscale and RGB images.
        return filters.gaussian(image, sigma=1)
    elif operation_name == "skeleton":
    # Skeletonization is a morphological operation for thinning binary images.
    # Converts to grayscale, then binarize with Otsu's threshold if the image is RGB.
        gray = color.rgb2gray(image) if image.ndim == 3 else image
        binary = gray > filters.threshold_otsu(gray)
        return morphology.skeletonize(binary)
    
def process_and_display_dataset():
    # Load the faces dataset
    faces = data.lfw_subset()
    
    # Select a subset of images (first 4 images)
    subset = faces[:4]
    
    # List of operations to apply
    operations = [
        "original", "grayscale", "rescale", "flip", 
        "noise", "erosion", "dilation", "canny",
        "blur", "skeleton"
    ]
    
    # Create figure
    n_images = len(subset)
    n_operations = len(operations)
    fig, axes = create_subplot(n_images, n_operations, figsize=(20, 16))
    
    # Process and display each image
    for img_idx, image in enumerate(subset):
        print(f"\nProcessing image {img_idx + 1}/{n_images}")
        
        for op_idx, operation in enumerate(operations):
            if operation == "original":
                result = image
                print(f"Original image shape: {image.shape}")
            else:
                print(f"Applying {operation}...")
                result = process_single_image(image, operation)
                print(f"- {operation} shape: {result.shape}")
                if operation == "rescale":
                    print(f"- Reduced size by 50%")
                elif operation == "canny":
                    print(f"- Detected {np.sum(result)} edge pixels")
                elif operation == "skeleton":
                    print(f"- Created skeleton with {np.sum(result)} pixels")
            
            # Display the result
            display_image(axes[img_idx, op_idx], result, 
                        f"Image {img_idx+1}\n{operation.title()}")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print("-" * 50)
    for img_idx, image in enumerate(subset):
        print(f"\nImage {img_idx + 1}:")
        print(f"- Original dimensions: {image.shape}")
        if image.ndim == 3:  
            gray = color.rgb2gray(image)
        else:
            gray = image         
        print(f"- Average intensity: {np.mean(gray):.3f}")
        print(f"- Standard deviation: {np.std(gray):.3f}")
        edges = feature.canny(gray)
        print(f"- Edge pixel percentage: {(np.sum(edges) / edges.size * 100):.2f}%")
        
    # Adjust layout and display
    plt.suptitle("Face Dataset Processing Operations", fontsize=16)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    process_and_display_dataset()


#Unit Testing
import unittest


class TestImageProcessingFunctions(unittest.TestCase):

    def test_create_subplot(self):
        rows, cols = 2, 2
        fig, axes = create_subplot(rows, cols)
        self.assertEqual(len(axes), rows)  
        self.assertEqual(len(axes[0]), cols)  

    def test_display_image(self):
        fig, ax = plt.subplots()
        image = data.camera()
        try:
            display_image(ax, image, "Test Image")
            plt.close(fig)  
        except Exception as e:
            self.fail(f"display_image raised an exception unexpectedly: {e}")

    def test_process_single_image_grayscale(self):
        image_rgb = data.astronaut()
        result = process_single_image(image_rgb, "grayscale")
        self.assertEqual(result.ndim, 2)  

    def test_process_single_image_rescale(self):
        image = data.camera()
        result = process_single_image(image, "rescale")
        self.assertEqual(result.shape[0], image.shape[0] // 2)  

    def test_process_single_image_flip(self):
        image = data.camera()
        result = process_single_image(image, "flip")
        self.assertTrue(np.array_equal(result, np.fliplr(image)))  

    def test_process_single_image_noise(self):
        image = data.camera()
        result = process_single_image(image, "noise")
        self.assertEqual(result.shape, image.shape) 

    def test_process_single_image_erosion(self):
        image = data.camera()
        result = process_single_image(image, "erosion")
        self.assertEqual(result.shape, image.shape)  

   

if __name__ == "__main__":
    unittest.main()
