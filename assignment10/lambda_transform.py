import json
import pandas as pd
from io import StringIO

def lambda_handler(event, context):
    # get the data (the csv file) from event
    data = event["data"]
    # Use StringIO to process the data
    data = StringIO(data)
    df = pd.read_csv(data)
    # retrieve the state, which should all be "NC"
    df["state"] = df["Recipient Region"].str.split(",").str[0]
    # data is saves as a csv file
    csv_data = df.to_csv(index=False)
    return {
        'statusCode': 200,
        'data': csv_data
    }