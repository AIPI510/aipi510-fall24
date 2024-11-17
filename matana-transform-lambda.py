import json
import boto3
import io
import pandas as pd

def lambda_handler(event, context):
    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Load json passing from extract lambda
    payload = event['body']
    year = payload['year']
    input_bucket_name = payload['input_bucket_name']
    input_file_key_gdp = payload['input_file_key_gdp']
    input_file_key_countrylist = payload['input_file_key_countrylist']

    # Number of top countries to show in the resulting table
    top = 20

    # JSON file name for the transformed data
    file_key_gdp_transformed = 'gdp_transformeddata_' + year + '.json'

    print("Input Payload loaded")

    try:
        # Read from JSON files in S3 Bucket
        response_gdp = s3.get_object(Bucket=input_bucket_name, Key=input_file_key_gdp)
        gdp_data = json.loads(response_gdp['Body'].read().decode('utf-8'))

        response_countrylist = s3.get_object(Bucket=input_bucket_name, Key=input_file_key_countrylist)
        countrylist_data = json.loads(response_countrylist['Body'].read().decode('utf-8'))

        print("JSON loaded")

        # Create pandas dataframe from GDP JSON
        country_id, gdp_value = [], []
        for country_entries in gdp_data[1]:
            country_id.append(country_entries['country']['id'])
            gdp_value.append(country_entries['value'])
            gdp_df = pd.DataFrame([country_id, gdp_value], index=["country_id","gdp_value"]).T

        # Create pandas dataframe for the list of countries (excluding Aggregates), from countrylist JSON
        country_id, country_name = [], []
        for country_entries in countrylist_data[1]:
            if country_entries['region']['value'] != "Aggregates":
                country_id.append(country_entries['iso2Code'])
                country_name.append(country_entries['name'])
            countrylist_df = pd.DataFrame([country_id, country_name], index=["country_id","country_name"]).T

        print("Two dataframes created")

        # Merge countrylist_df and gdp_df to remove all Aggregates' GDP data, and sort the data in descending order.
        gdp_noagg_df = pd.merge(countrylist_df, gdp_df, on = "country_id", how="inner").sort_values(by="gdp_value", ascending=False).head(top)
        # Reset index of the gdp_noagg_df dataframe, and set them to start from 1 instead of 0, so that the country with highest GDP value/per capita/growth will ranked as first
        gdp_noagg_df = gdp_noagg_df.reset_index(drop=True)
        gdp_noagg_df.index = gdp_noagg_df.index + 1

        print("Two dataframes merged")

        s3.put_object(Bucket=input_bucket_name, Key=file_key_gdp_transformed, Body=bytes(json.dumps(gdp_noagg_df.to_json()).encode('UTF-8')))

        print("Resulting dataframe written as JSON into S3 Bucket")

        # Passing key parameters to next lambda (load)
        return {
            'statusCode': 200,
            'body': {
                "year": year,
                "input_bucket_name": input_bucket_name,
                "file_key_gdp_transformed": file_key_gdp_transformed
                    }       
        } 

    except Exception as e:
        # Return an error message if failed
        return {
            'statusCode': 500,
            'body': str(e)
        }
