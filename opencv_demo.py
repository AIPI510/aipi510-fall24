import cv2
import math
import matplotlib.pyplot as plt


def extract_pupil(image):
    """
    extracts the pupil's center and radius from an image 
    
    Paramaters
    ---------
    image: numpy array
        a BGR array representation of our input image
    
    Returns
    ---------
    mask: numpy array
        a binary mask highlighting the potential pupil region
    annotated: numpy array
        our image with the predicted center & radius overlayed, if applicable
    """
    temp = image.copy()
    ## Step 1: Feature Engineering to obtain binary mask
    pupil_mask = _feature_engineering(temp)
    # Step 2: Identify pupil candidate
    center, radius = _find_pupil(pupil_mask)
    ## no pupil candidate was found that met criteria
    if not center:
        return temp, temp
    ## Overlay center and radius on image
    cv2.circle(temp, (int(center[0]),int(center[1])), int(radius), (255, 255, 255), 3)
    cv2.line(temp, (int(center[0]),int(center[1])), (int(center[0])+int(radius),int(center[1])), (0, 0, 255), 3)
    return pupil_mask, temp


def _feature_engineering(image):
    """
    conducts feature engineering / image processing using OpenCV 
    
    Paramaters
    ---------
    image: numpy array
        a BGR array representation of our input image
    """
    ## Step 1: Apply Gaussian Blur – helps smoothen the images 
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    ## Step 2: Retrieve grayscale image (e.x. red channel)
    grayscale = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    ## Step 3: Improve image contrast using CLAHE 
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(5,5))
    standardized = clahe.apply(grayscale)
    ## Step 4: Perform binary thresholding of the image 
    _, pupil_mask = cv2.threshold(standardized, 40, 255, cv2.THRESH_BINARY_INV)
    return pupil_mask

def _find_pupil(mask):
    """
    identifies the most likely pupil candidate from the binary mask 
    
    Paramaters
    ---------
    mask: numpy array
        a binary mask highlighting the potential pupil region
    """

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    ## define minimum radius, candidate center and radius
    max_area = 0
    candidate_center, candidate_radius = None, None
    ## loop over contours
    for contour in contours:
        ## find the convex hull of the contour 
        convex_closed = cv2.convexHull(contour, False)
        ## find the perimeter of the contour 
        perimeter = cv2.arcLength(convex_closed, True)
        if perimeter == 0: 
            continue
            ## find the area of the contour
        area = cv2.contourArea(convex_closed)
        ## calculating circularity based on its equation
        circularity = (4*math.pi*area)/(perimeter*perimeter)
        ## our pupil candidate is the contour with the maximal area that meets the circularity requirement below
        if circularity > 0.7 and area > max_area:
            # compute the center of the contour
            approx = cv2.approxPolyDP(convex_closed, perimeter * 0.034, True)
            candidate_center, candidate_radius = cv2.minEnclosingCircle(approx)
            # update max_area
            max_area = area
    return candidate_center, candidate_radius

def _draw_output(image_sequences, output_file='output.jpg'):
    """
    Saves a grid of images where each row contains the original input image, binary mask, and annotated image.
    
    Parameters
    ---------

        image_sequences: list of list of np.ndarray
            A list where each element is a list of 3 images (input, mask, annotated) as numpy arrays.
        output_file: str
            The file path to save the output JPEG image. Default is output.jpg
    """
    # Calculate the number of rows and columns
    n_rows = len(image_sequences)
    n_cols = 3  # Each sequence contains 3 images

    # Create a figure with appropriate dimensions
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 3, n_rows * 3))
    
    # Ensure that `axes` is always a 2D array for consistent indexing
    if n_rows == 1:
        axes = [axes]

    column_titles = ["Input Image", "Binary Mask", "Annotated Image"]

    ## Loop over image sequences
    for i, sequence in enumerate(image_sequences):
        ## Loop over images in a sequence
        for j, image in enumerate(sequence):
            ## Retrieve current axis
            ax = axes[i][j]
            # Set the column titles only for the first row
            if i == 0:
                ax.set_title(column_titles[j], fontsize=12, weight='bold')
            if j == 0:  # Input image (BGR to RGB)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                ax.imshow(image_rgb)
            elif j == 1:  # Binary mask
                ax.imshow(image, cmap='gray')
            elif j == 2:  # Annotated image (BGR to RGB)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                ax.imshow(image_rgb)
            ax.axis('off')

    
    plt.tight_layout()
    plt.savefig(output_file, format='jpeg', dpi=100)
    plt.close(fig)

    print(f'Output successfully written to {output_file}')



if __name__ == "__main__":
    img1 = cv2.imread('./data/test_img_1.jpg')
    img2 = cv2.imread('./data/test_img_2.jpg')
    img3 = cv2.imread('./data/test_img_3.jpg')
    mask1, annotated1 = extract_pupil(img1)
    mask2, annotated2 = extract_pupil(img2)
    mask3, annotated3 = extract_pupil(img3)
    _draw_output([[img1, mask1, annotated1], [img2, mask2, annotated2], [img3, mask3, annotated3]])
    print("Done!")


