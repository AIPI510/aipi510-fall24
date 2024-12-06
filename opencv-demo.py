# Importing necessary libraries
import cv2
import numpy as np
from sklearn.datasets import load_sample_image
import matplotlib.pyplot as plt

# Load the 'china.jpg' sample image from sklearn built-in dataset
image = load_sample_image('china.jpg')

# Convert to BGR format for OpenCV compatibility
image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# Convert the image to grayscale because feature detection works better on grayscale images
gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

# SIFT (Scale-Invariant Feature Transform)
# It detects scale and rotation-invariant features. It's useful for object recognition and image matching.
sift = cv2.SIFT_create()
# Detect keypoints and compute descriptors
kps_sift, des_sift = sift.detectAndCompute(gray, None)
# Draw keypoints on the image
img_sift = cv2.drawKeypoints(gray, kps_sift, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# ORB (Oriented FAST and Rotated BRIEF)
# It's a faster alternative to SIFT and SURF
orb = cv2.ORB_create()
# Detect keypoints and compute descriptors
kps_orb, des_orb = orb.detectAndCompute(gray, None)
# Draw keypoints on the image
img_orb = cv2.drawKeypoints(gray, kps_orb, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Harris Corner Detection
# Finds corners in the image. Identifies corners based on intensity changes in multiple directions.
harris = cv2.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)
# Dilate the result to mark the corners
harris = cv2.dilate(harris, None)
img_harris = image_bgr.copy()
# Threshold for an optimal value, marking corners in red
img_harris[harris > 0.01 * harris.max()] = [0, 0, 255]

# Shi-Tomasi Corner Detection
# An improvement over Harris, used in tracking applications.
corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)
corners = np.int32(corners)
img_shi = image_bgr.copy()
# Draw circles around detected corners
for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img_shi, (x, y), 3, 255, -1)

# Canny Edge Detection
# Detects edges in the image, useful for shape analysis and object detection.
edges = cv2.Canny(gray, 100, 200)

# Display results
plt.figure(figsize=(20, 10))

# Original Image
plt.subplot(231), plt.imshow(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB))
plt.title('Original Image'), plt.axis('off')

# SIFT Features
plt.subplot(232), plt.imshow(cv2.cvtColor(img_sift, cv2.COLOR_BGR2RGB))
plt.title('SIFT Features'), plt.axis('off')

# ORB Features
plt.subplot(233), plt.imshow(cv2.cvtColor(img_orb, cv2.COLOR_BGR2RGB))
plt.title('ORB Features'), plt.axis('off')

# Harris Corner Detection
plt.subplot(234), plt.imshow(cv2.cvtColor(img_harris, cv2.COLOR_BGR2RGB))
plt.title('Harris Corner Detection'), plt.axis('off')

# Shi-Tomasi Corner Detection
plt.subplot(235), plt.imshow(cv2.cvtColor(img_shi, cv2.COLOR_BGR2RGB))
plt.title('Shi-Tomasi Corner Detection'), plt.axis('off')

# Canny Edge Detection
plt.subplot(236), plt.imshow(edges, cmap='gray')
plt.title('Canny Edge Detection'), plt.axis('off')

# Adjust layout and display the plot
plt.tight_layout()
plt.show()

# Print the number of features detected by each method
print(f"Number of SIFT keypoints: {len(kps_sift)}")
print(f"Number of ORB keypoints: {len(kps_orb)}")
print(f"Number of Shi-Tomasi corners: {len(corners)}")