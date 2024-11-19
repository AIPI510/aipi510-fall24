import json
import boto3
import io
import pandas as pd
import logging

def lambda_handler(event, context):
    """ Load the JSON file from Transform Lambda, 
        and return CSV file saved in the S3 output bucket """
    
    # Add logs to the CloudWatch
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Load json passing from extract lambda
    payload = event['body']
    year = payload['year']
    input_bucket_name = payload['input_bucket_name']
    file_key_gdp_transformed = payload['file_key_gdp_transformed']

    # JSON file name for the output data
    output_bucket_name = 'matana-etl-output-s3'
    output_file_key = 'gdp_stat_' + year + '.csv'

    logger.info("Input Payload loaded")

    try:
        # Read from JSON files in S3 Bucket
        response_gdp_transformed = s3.get_object(Bucket=input_bucket_name, Key=file_key_gdp_transformed)
        gdp_transformed_data = json.loads(response_gdp_transformed['Body'].read().decode('utf-8'))

        logger.info("JSON loaded")

        gdp_transformed_df = pd.read_json(gdp_transformed_data)

        logger.info("JSON converted into dataframe")

        # Write the dataframe as CSV and save it in the S3 Output Bucket
        csv_buffer = io.StringIO()
        gdp_transformed_df.to_csv(csv_buffer, index=False)
        response = s3.put_object(Bucket=output_bucket_name, Key=output_file_key, Body=csv_buffer.getvalue())
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        logger.info("Resulting dataframe written as CSV into S3 Output Bucket")

        # Return key parameters
        return {
            'statusCode': 200,
            'body': {
                "year": year,
                "output_bucket_name": output_bucket_name,
                "output_file_key": output_file_key
                    }       
        } 

    except Exception as e:
        # Return an error message if failed
        return {
            'statusCode': 500,
            'body': str(e)
        }
