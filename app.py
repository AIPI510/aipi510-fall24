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

fuel_types = ['Gasoline', 'E85 Flex Fuel', 'Hybrid', 'Diesel', 'Plug-In Hybrid']

def user_inputs(df):
    brand = st.selectbox("Select Brand", df["brand"].unique())
    model_options = df[df["brand"] == brand]["model"].unique()
    model_options.sort()
    model = st.selectbox("Select Model", model_options)
    model_year = st.number_input("Model Year", min_value=2000, max_value=2024, step=1)
    milage = st.number_input("Mileage (Miles)", min_value=0, step=1000)
    fuel_type = st.selectbox("Select Fuel Type", fuel_types)
    accident = st.selectbox("Accident History", ["Yes", "No"]) 

    data = {
        'brand': brand,
        'model': model,
        'model_year': model_year,
        'milage': milage,
        'fuel_type': fuel_type,
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
    st.title("How much $ is your car NOW?")
    st.write("This application predicts the price of your vehicle in just a minute, with minimal information provided. Note that results are only estimations and real-world numbers differ case-by-case.")

    # Collect user inputs
    user_data = user_inputs(df)

    # When the "Find out" button is pressed
    if st.button("Find out"):
        # Transform user data and make prediction
        transformed_data = data_transform(user_data, processor)
        predicted_price = predict(model, transformed_data)[0]
        
        # Display the predicted price in a formatted style
        st.markdown(
            f"<div style='text-align: center; font-size: 24px; font-weight: bold; color: green;'>Predicted Price: ${round(predicted_price/1000)}k</div>",
            unsafe_allow_html=True
        ) 
        
if __name__ == "__main__":
    main()
