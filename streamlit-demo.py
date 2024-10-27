import streamlit as st
from torchvision.datasets import FGVCAircraft
import torch
from torch.utils.data import Dataset
from torchvision.datasets import FGVCAircraft
import cv2


st.title("Feature Engineering in Images 📷")
st.write("Feature engineering for images is about extracting useful information from the raw images. We might do this for the purposes of creating a classifier.")

if st.button("Continue"):
    st.write("Let's use the FGVCAircraft database as an example.")
    if st.button("Download Dataset"):
        training_data = FGVCAircraft(
            root = 'data',
            annotation_level = 'family',
            download = True 
            )
        

    







