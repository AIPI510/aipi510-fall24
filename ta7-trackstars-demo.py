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
def init_state(): 
    for state_var in [
        'dataset', 
        'sample_img', 
        'grey_image', 
        'blurred_image', 
        'edge_detect', 
        'corner_img', 
        'corner', 
        'super_pixel', 
        'super_pixel_img', 
        'SIFT_img',
        'SIFT']:
        if state_var not in st.session_state:
            st.session_state[state_var] = None

if 'button1' not in st.session_state:
    init_state()

def click_button1():
    st.session_state.button1 = True


st.write("""
    We'll load the [Fine-Grained Visual Classification of Aircraft (FGVC-Aircraft)dataset](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html)
    by way of the [associated dataset interface](https://pytorch.org/vision/main/generated/torchvision.datasets.FGVCAircraft.html#torchvision.datasets.FGVCAircraft)
    built into PyTorch.
    """)
st.write("""
    The dataset consists of 10,200 images, which offers a reasonable amount of diversity while 
    remaining within a single narrow task (fixed-wing aircraft classification). This task helps illustrate 
    how up-front feature engineering can present feature diversity to a classifier that might improve its 
    overall accuracy (or at least save training time getting to the desired accuracy). 
    """)
st.write("""
    Let's start by loading the dataset. This could take a bit. See the console output for progress, the app will continue once
    the FGVC archive is unpacked and ready for use. 
    """)

# Load the dataset and limit to a subset
def load_subset(dataset_size=100):

    if st.session_state.dataset is None:

        data_dir = 'data'

        # Define transformation
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])

        with st.spinner("Downloading..."): 
            
            # Pytorch dataset semantics with help from the overview of pytorch dataset interactions here: 
            # https://pytorch.org/tutorials/beginner/basics/data_tutorial.html
            full_dataset = FGVCAircraft(
                root=data_dir, 
                annotation_level='family', 
                download=True, 
                transform=transform
                )

        with st.spinner("Loading 100 random images..."): 

            indices = np.random.choice(len(full_dataset), dataset_size, replace=False)            
            st.session_state.dataset = Subset(full_dataset, indices)

    st.success("Dataset loaded.")

# Step 1: Load dataset subset
if st.session_state.dataset or st.button("Load Dataset Subset"):
    
    load_subset()

    st.session_state.sample_img, _ = st.session_state.dataset[25]
    st.write("Here is a random image from the dataset.")
    img_pil = transforms.ToPILImage()(st.session_state.sample_img)
    st.image(img_pil, caption="Sample Image", use_column_width=True)
    st.write("""
        How might we get some information out of this that we might use in a classifier? 
        Perhaps we would look at the shape to help identify the aircraft. A simple 
        way of extracting this is edge detection... 
    """)
    stage = 2

    # Step 2: Convert to grayscale
    if st.session_state.grey_image is not None or st.button("Convert to Greyscale"):
        st.write("First we convert to greyscale, as many of our transformation operate on a single color channel... ")
        img_np = np.array(transforms.ToPILImage()(st.session_state.sample_img))
        st.session_state.grey_image = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        st.image(st.session_state.grey_image, caption="Greyscale Image", use_column_width=True)
        
        st.write("""
            Now we apply gaussian blurring to remove noise. While could be a separate channel in and of itself
            to a classifier, the blurring reduces the number of small compression artificats that reduce the 
            quality and utility of the transformations we'll apply next. 
            """)

        # Step 3: Apply Gaussian blur
        if st.session_state.blurred_image is not None or st.button("Apply Gaussian Blurring"):
            st.session_state.blurred_image = cv2.GaussianBlur(st.session_state.grey_image, (5, 5), 0)
            st.image(st.session_state.blurred_image, caption="Blurred Image", use_column_width=True)
            st.write("Now we're ready to apply a canny edge detector")

            # Step 4: Apply Canny edge detection
            if st.session_state.edge_detect is not None or st.button("Apply Edge Detection"):
                st.session_state.edge_detect = cv2.Canny(st.session_state.blurred_image, threshold1=100, threshold2=200)
                st.image(st.session_state.edge_detect, caption="Edges", use_column_width=True)
                st.write("We could also use a Harris corner detection algorithm to try to extract the shape")

                # Step 5: Load a new image for Harris corner detection
                if st.session_state.corner_img is not None or st.button("Load New Image for Corner Detection"):
                    load_subset()
                    if st.session_state.dataset:
                        st.session_state.corner_img, _ = st.session_state.dataset[13]
                        st.write("New image for corner detection.")
                        corner_img_pil = transforms.ToPILImage()(st.session_state.corner_img)
                        st.image(corner_img_pil, caption="Image for Corner Detection", use_column_width=True)

                    # Step 6: Apply Harris corner detection
                    if st.session_state.corner is not None or st.button("Apply Harris Corner Detection"):
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
                        if st.session_state.super_pixel is not None or st.button("Load New Image for SuperPixel Segmentation"):
                            load_subset()
                            if st.session_state.dataset:
                                st.session_state.super_pixel, _ = st.session_state.dataset[62]
                                st.write("New image for SuperPixel segmentation.")
                                super_pixel_pil = transforms.ToPILImage()(st.session_state.super_pixel)
                                st.image(super_pixel_pil, caption="Image for SuperPixel Segmentation", use_column_width=True)

                            # Step 8: Apply SuperPixel segmentation
                            if st.session_state.super_pixel_img is not None or st.button("Apply SuperPixel Segmentation"):
                                
                                # We use the concept of a superpixel to establish large picture elements based 
                                # on the LSC segmentation algorithm. See openCV superpixel docs and the LSC class: 
                                # https://docs.opencv.org/3.4/df/d6c/group__ximgproc__superpixel.html
                                # https://docs.opencv.org/4.x/d5/da0/classcv_1_1ximgproc_1_1SuperpixelLSC.html    
                                st.write("Applying SuperPixel segmentation...")
                                lsc_img_np = np.array(transforms.ToPILImage()(st.session_state.super_pixel))
                                lsc = cv2.ximgproc.createSuperpixelLSC(
                                    lsc_img_np,     
                                    region_size=20,  # Average superpixel size
                                    ratio=0.075      # Compactness
                                )
                                
                                # Iteratively segment to identify the superpixels
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
                                if st.session_state.SIFT_img is not None or st.button("Load New Image for SIFT"):
                                    load_subset()
                                    if st.session_state.dataset:
                                        st.session_state.SIFT_img, _ = st.session_state.dataset[88]
                                        st.write("New image for SIFT.")
                                        SIFT_pil = transforms.ToPILImage()(st.session_state.SIFT_img)
                                        st.image(SIFT_pil, caption="Image for SIFT", use_column_width=True)

                                    # Step 10: Apply SIFT feature detection
                                    if st.session_state.SIFT is not None or st.button("Apply SIFT"):
                                        st.write("Applying SIFT feature detection...")
                                        SIFT_img_np = np.array(transforms.ToPILImage()(st.session_state.SIFT_img))
                                        sift = cv2.SIFT_create()
                                        grey = cv2.cvtColor(SIFT_img_np, cv2.COLOR_RGB2GRAY)
                                        keypoints, descriptors = sift.detectAndCompute(grey, None)
                                        st.session_state.SIFT = cv2.drawKeypoints(SIFT_img_np, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                                        
                                        fig, ax = plt.subplots()
                                        ax.imshow(st.session_state.SIFT)
                                        ax.axis("off")
                                        st.pyplot(fig)

                                        st.write("""
                                            All images retain copyrights of the original owners, which are outlined on the dataset page [here](https://www.robots.ox.ac.uk/~vgg/data/fgvc-aircraft/#ack). 
                                        """)










