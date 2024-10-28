import streamlit as st
from torchvision.datasets import FGVCAircraft
from torch.utils.data import Subset
import numpy as np
import cv2
from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt

st.title("Feature Engineering in Images 📷")
st.write("Feature engineering for images is about extracting useful information from raw images. We might want to use this information to train a classifier, so lets keep that in mind when we're engineering these features.")

# Initialize session state variables if not already set
for state_var in ['dataset', 'sample_img', 'grey_image', 'blurred_image', 'edge_detect', 'corner_img', 'corner', 'super_pixel', 'super_pixel_img', 'SIFT_img']:
    if state_var not in st.session_state:
        st.session_state[state_var] = None

# Define transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Load the dataset and limit to a subset
def load_subset(dataset_size=100):
    if st.session_state.dataset is None:
        full_dataset = FGVCAircraft(root='data', annotation_level='family', download=True, transform=transform)
        indices = np.random.choice(len(full_dataset), dataset_size, replace=False)
        st.success("Successfully loaded 100 items")
        st.session_state.dataset = Subset(full_dataset, indices)

# Step 1: Load dataset subset
if st.button("Load Dataset Subset"):
    load_subset()
    if st.session_state.dataset:
        st.session_state.sample_img, _ = st.session_state.dataset[30]
        st.write("Here is an example image from the dataset.")
        img_pil = transforms.ToPILImage()(st.session_state.sample_img)
        st.image(img_pil, caption="Sample Image", use_column_width=True)
        st.write("How might we get some information out of this that we might use in a classifier? Well perhaps to identify which planes are which we would look at the shape. A simple way of extracting this is edge detection")

# Step 2: Convert to grayscale
if st.session_state.sample_img is not None and st.button("Convert to Greyscale"):
    st.write("First we convert to greyscale")
    img_np = np.array(transforms.ToPILImage()(st.session_state.sample_img))
    st.session_state.grey_image = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    st.image(st.session_state.grey_image, caption="Greyscale Image", use_column_width=True)
    st.write("Then we will need to apply gaussian blurring to remove noise and detail")

# Step 3: Apply Gaussian blur
if st.session_state.grey_image is not None and st.button("Apply Gaussian Blurring"):
    st.session_state.blurred_image = cv2.GaussianBlur(st.session_state.grey_image, (5, 5), 0)
    st.image(st.session_state.blurred_image, caption="Blurred Image", use_column_width=True)
    st.write("Now we're ready to apply a Canny edge detector")

# Step 4: Apply Canny edge detection
if st.session_state.blurred_image is not None and st.button("Apply Edge Detection"):
    st.session_state.edge_detect = cv2.Canny(st.session_state.blurred_image, threshold1=100, threshold2=200)
    st.image(st.session_state.edge_detect, caption="Edges", use_column_width=True)
    st.write("We could also use a Harris corner detection algorithm to try to extract the shape")

# Step 5: Load a new image for Harris corner detection
if st.session_state.edge_detect is not None and st.button("Load New Image for Corner Detection"):
    load_subset()
    if st.session_state.dataset:
        st.session_state.corner_img, _ = st.session_state.dataset[13]
        st.write("New image for corner detection.")
        corner_img_pil = transforms.ToPILImage()(st.session_state.corner_img)
        st.image(corner_img_pil, caption="Image for Corner Detection", use_column_width=True)

# Step 6: Apply Harris corner detection
if st.session_state.corner_img is not None and st.button("Apply Harris Corner Detection"):
    st.write("Applying Harris corner detection...")
    corner_img_np = np.array(transforms.ToPILImage()(st.session_state.corner_img))
    gray_corner_img = cv2.cvtColor(corner_img_np, cv2.COLOR_RGB2GRAY).astype(np.float32)
    corners = cv2.cornerHarris(gray_corner_img, blockSize=6, ksize=11, k=0.5)
    
    # Mark detected corners in magenta
    thresh_img = cv2.cvtColor(gray_corner_img.astype(np.uint8), cv2.COLOR_GRAY2RGB)
    thresh_img[corners > corners.mean()] = [255, 0, 255]
    st.session_state.corner = thresh_img  # Store corner result in session state
    
    fig, ax = plt.subplots()
    ax.imshow(thresh_img)
    ax.axis("off")
    st.pyplot(fig)
    st.write("We can also use a technique for simplifying the image into 'superpixels'. This groups pixels of similar colour and location together, as they're likely to be one 'thing' ")

# Step 7: Load a new image for SuperPixel segmentation
if st.session_state.corner is not None and st.button("Load New Image for SuperPixel Segmentation"):
    load_subset()
    if st.session_state.dataset:
        st.session_state.super_pixel, _ = st.session_state.dataset[62]
        st.write("New image for SuperPixel segmentation.")
        super_pixel_pil = transforms.ToPILImage()(st.session_state.super_pixel)
        st.image(super_pixel_pil, caption="Image for SuperPixel Segmentation", use_column_width=True)

# Step 8: Apply SuperPixel segmentation
if st.session_state.super_pixel is not None and st.button("Apply SuperPixel Segmentation"):
    st.write("Applying SuperPixel segmentation...")
    lsc_img_np = np.array(transforms.ToPILImage()(st.session_state.super_pixel))
    lsc = cv2.ximgproc.createSuperpixelLSC(
        lsc_img_np,  # Target image
        region_size=20,  # Average superpixel size
        ratio=0.075  # Compactness
    )
    lsc.iterate(5)
    mask = lsc.getLabelContourMask()
    super_pixel_img = cv2.bitwise_and(lsc_img_np, lsc_img_np, mask=255-mask)
    st.session_state.super_pixel_img = super_pixel_img
    
    fig, ax = plt.subplots()
    ax.imshow(super_pixel_img)
    ax.axis("off")
    st.pyplot(fig)
    st.write("What about looking for the most important features independent of scale and rotation? For this, we can use SIFT (Scale-Invariant Feature Transform). SIFT is a 'key point' detector, which is useful in the planes dataset because identifying different planes often depends on features like engine size, tail shape, etc.")

# Step 9: Load a new image for SIFT
if st.session_state.super_pixel_img is not None and st.button("Load New Image for SIFT"):
    load_subset()
    if st.session_state.dataset:
        st.session_state.SIFT_img, _ = st.session_state.dataset[88]
        st.write("New image for SIFT.")
        SIFT_pil = transforms.ToPILImage()(st.session_state.SIFT_img)
        st.image(SIFT_pil, caption="Image for SIFT", use_column_width=True)

# Step 10: Apply SIFT feature detection
if st.session_state.SIFT_img is not None and st.button("Apply SIFT"):
    st.write("Applying SIFT feature detection...")
    SIFT_img_np = np.array(transforms.ToPILImage()(st.session_state.SIFT_img))
    sift = cv2.SIFT_create()
    grey = cv2.cvtColor(SIFT_img_np, cv2.COLOR_RGB2GRAY)
    keypoints, descriptors = sift.detectAndCompute(grey, None)
    output_image = cv2.drawKeypoints(SIFT_img_np, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    fig, ax = plt.subplots()
    ax.imshow(output_image)
    ax.axis("off")
    st.pyplot(fig)
    










