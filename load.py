import boto3
import json
import logging

# -- Overview -- 
# The Load Stage is the final step in the ETL (Extract, Transform, Load) pipeline. 
# This stage is responsible for saving the processed, aggregated data (generated during the Transform Stage) 
# into an S3 bucket. The goal is to make the insights available for downstream use.


#-----------------------------------------------------------------------------------------------------------------------------------------------------#

# Logging system is like a CTO tracking production deployments.
# INFO logs are for bragging rights (successful operations), and ERROR logs are for... well, explaining what broke.
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    s3 = boto3.client('s3')

    # Define the final destination for our transformed data.
    # Think of this as the VC dashboard where all startup funding trends are stored for everyone to admire.
    bucket_name = 'etl-indian-startup-output'  # The final resting place for our processed data.
    file_key = 'transformed-data.json'        # The name of our report file in JSON format.

    try:
        # **1: Grab the Transformed Data**
        # This is where the spotlight shifts to the results from the Transform stage.
        # The aggregated funding data by city lands here, passed via Step Functions.
        transformed_data = event.get('transformed_data', {})
        # Example `transformed_data`: {"Bangalore": 3000000, "Mumbai": 2000000, "Delhi": 1500000}

        # **2: Store the Data in the Destination Bucket**
        # Time to upload this to S3, so it’s ready for the next AIPI class.
        s3.put_object(
            Bucket=bucket_name,          
            Key=file_key,                  
            Body=json.dumps(transformed_data),  
            ContentType='application/json'
        )
        
        # **3: Log the Success**
        # You know that feeling when you successfully close a funding round? This is the equivalent.
        logger.info(f"Data loaded successfully to {bucket_name}/{file_key}")
        
        # Return a success message to mark the final step of the ETL process.
        return {'message': 'Data loaded successfully'}

    except Exception as e:
        # **4: Handle Errors Gracefully**
        # Just like us founders know how to pivot after rejection, we’ll log and handle any issues here.
        logger.error(f"Error uploading data to S3: {e}")
        
        # Return the error message, so it’s clear what went wrong (we’re not here to hide bugs, and call it 'features').
        return {'error': str(e)}
