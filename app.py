import streamlit as st 
from datetime import datetime
import pandas as pd 
import numpy as np
import pickle
import json
import xgboost as xgb
from st_files_connection import FilesConnection
from io import BytesIO
import boto3
import sklearn

# title of the Web App
st.title("See how much your car is worth NOW in just a minute!")
st.subheader("This application predicts the price of your vehicle in just a minute, with minimal information provided. Note that results are only estimations and real-world numbers differ case-by-case.")
st.write("Specify your car information below:")

# processor_path = '/Users/owner/Desktop/data_science/ml_course/aipi510/assignment9/preprocessor.pkl'
# model_path = "/Users/owner/Desktop/data_science/ml_course/aipi510/assignment9/xgbr_model.pkl"

bucket_name = 'churn-challenge'
file_key = 'churn-challenge/x_train.csv'

conn = st.connection('s3', type=FilesConnection)

df = conn.read("churn-challenge/x_train.csv", input_format="csv", ttl=600)
s3 = boto3.resource('s3')

with BytesIO() as file:
   s3.Bucket("churn-challenge").download_fileobj("preprocessor.pkl", file)
   file.seek(0)    # move back to the beginning after writing
   processor = pickle.load(file)

with BytesIO() as mod:
   s3.Bucket("churn-challenge").download_fileobj("xgbr_model.pkl", mod)
   mod.seek(0)    # move back to the beginning after writing
   model = pickle.load(mod)


def user_inputs(df):
    brand = st.selectbox("Select Brand", df["brand"].unique())
    model = st.selectbox("Select Model", df["model"].unique())
    model_year = st.number_input("Model Year", min_value=2000, max_value=2024, step=1)
    milage = st.number_input("Mileage", min_value=0, step=1000)
    fuel_type = st.selectbox("Select Fuel Type", df["fuel_type"].unique())
    engine = st.selectbox("Select Engine", df["engine"].unique())  
    transmission = st.selectbox("Select Transmission", df["transmission"].unique())
    accident = st.selectbox("Accident History", ["Yes", "No"])  # Assuming binary options

    data = {
        'brand': brand,
        'model': model,
        'model_year': model_year,
        'milage': milage,
        'fuel_type': fuel_type,
        'engine': engine,
        'transmission': transmission,
        'accident': accident
    }

    df = pd.DataFrame(data, index=[0])
    return df

def data_transform(df, processor):
    return processor.transform(df)

# Predict with the model 
def predict(model, transformed):
    output = np.rint(model.predict(transformed))
    return output

def main():
    # A confirmation so the user knows what the input row looks like
    x_input = user_inputs(df)

    # design user interface
    if st.button("Find out"):
        transformed = data_transform(x_input, processor)
        prediction = predict(model, transformed)
        st.subheader("Estimate based on your inputs:")
        # here, define more informative statements, such as recommended actions, cautions, statistics you want to include, etc...
        st.write(f"{prediction}") # customize this 
        
if __name__ == "__main__":
    main()
