'''
This script contains the lambda handler function that is used to extract the data (i.e loading it
from hugging face)
'''
import json
import pandas as pd
import gzip
import base64

def lambda_handler(event, context):
    df = pd.read_csv("hf://datasets/AdonisVainglory/Cocktailer/final_cocktails.csv")
    data_json = df.to_json(orient='records')
    
    # Compressing the data here
    compressed_data = base64.b64encode(gzip.compress(data_json.encode('utf-8'))).decode('utf-8')

    return {
    'statusCode': 200,
    'dataframe': compressed_data
    }