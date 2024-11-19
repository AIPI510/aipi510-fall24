import json
import boto3
import io
import requests
import logging

def lambda_handler(event, context):
    """ Extract GDP data from the World Bank API for a year specified by user, 
        then save two JSON files (GDP data and Country List) into S3 input bucket."""
    
    # Add logs to the CloudWatch
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # year input from event
    year = str(event['year'])

    # URL for query from World Bank API, to query GDP data in specified year
    gdp_url = f"https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?per_page=1000&&format=json&date={year}"  
    logger.info(f'URL for GDP data: {gdp_url}')

    # JSON request from gdp_url and return GDP JSON data
    try:
        response = requests.get(url=gdp_url)
        response.raise_for_status()
        gdp_data = response.json()
        if not gdp_data:
            raise RuntimeError("No json data returned from the World Bank API query")
    except requests.HTTPError as http_err:
        logger.info(f'HTTP error occurred: {http_err}')
    except Exception as err:
        logger.info(f'Other error occurred: {err}')

    logger.info("Retrieved GDP JSON data")

    # JSON request from countrylist_apicall_url and return GDP country list data
    countrylist_url = "https://api.worldbank.org/v2/country?format=json&per_page=1000"
    logger.info(f'URL for Country List data: {countrylist_url}')

    try:
        response = requests.get(url=countrylist_url)
        response.raise_for_status()
        countrylist_data = response.json()
        if not countrylist_data:
            raise RuntimeError("No json data returned from the World Bank API query")
    except requests.HTTPError as http_err:
        logger.info(f'HTTP error occurred: {http_err}')
    except Exception as err:
        logger.info(f'Other error occurred: {err}')

    logger.info("Retrieved Country List JSON data")

    # Initialize the S3 client
    s3 = boto3.client('s3')

    input_bucket_name = 'matana-etl-input-s3'
    input_file_key_gdp = 'gdp_rawdata_' + year + '.json'
    input_file_key_countrylist = 'countrylist.json'
    
    try:
        # Write two JSON files into S3 Bucket
        s3.put_object(Bucket=input_bucket_name, Key=input_file_key_gdp, Body=bytes(json.dumps(gdp_data).encode('UTF-8')))
        s3.put_object(Bucket=input_bucket_name, Key=input_file_key_countrylist, Body=bytes(json.dumps(countrylist_data).encode('UTF-8')))

        logger.info("Two JSON files written to S3 Input Bucket")

        # Passing key parameters to next lambda (transform)
        return {
            'statusCode': 200,
            'body': {
                "year": year,
                "input_bucket_name": input_bucket_name,
                "input_file_key_gdp": input_file_key_gdp,
                "input_file_key_countrylist": input_file_key_countrylist
                    }       
        } 

    except Exception as e:
        # Return an error message if failed
        return {
            'statusCode': 500,
            'body': str(e)
        }
