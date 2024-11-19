'''
This script contains the lambda handler function that is used to transform the data (in our case,
we are one hot encoding features and changing the 'alcoholic' feature into 1 or 0 instead of a string)
'''
import pandas as pd
import gzip
import base64
import json

def lambda_handler(event, context):
    # Get compressed data from previous state
    compressed_data = event['dataframe']
    
    # uncompress the data
    json_data = gzip.decompress(base64.b64decode(compressed_data)).decode('utf-8')
    df = pd.read_json(json_data, orient='records')

    # drop Unnamed: 0 as a column and make the index the id column
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.set_index('id')

    # convert alcoholic column to binary
    df['alcoholic'] = df['alcoholic'].apply(lambda x: 1 if x == 'Alcoholic' else 0)

    # one hot encode the category and glassType columns columns
    df = pd.get_dummies(df, columns=['category', 'glassType'], drop_first=True)

    # compress the transformed dataframe
    data_json = df.to_json(orient='records')
    compressed_data = base64.b64encode(gzip.compress(data_json.encode('utf-8'))).decode('utf-8')
    
    return {
        'statusCode': 200,
        'dataframe': compressed_data
    }