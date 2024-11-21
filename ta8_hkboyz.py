import json
import boto3
import pandas as pd
import io

def extract_handler(event, context):
    """
    Extract Lambda function that reads Excel files from S3 bucket
    """
    try:
        # Initialize S3 client
        s3_client = boto3.client('s3')
        
        # Get bucket and file information from event
        source_bucket = 'excelfilesource'
        file_key = event['file_key']
        
        # Download file from S3
        response = s3_client.get_object(Bucket=source_bucket, Key=file_key)
        excel_data = response['Body'].read()
        df = pd.read_excel(io.BytesIO(excel_data))
        json_data = df.to_json(orient='records')
        
        return {
            'statusCode': 200,
            'body': json_data,
            'file_name': file_key.split('.')[0]  # Remove extension for CSV naming
        }
    
    except Exception as e:
        print(f"Error in extract function: {str(e)}")
        raise Exception(f"Extract function failed: {str(e)}")

def transform_handler(event, context):
    """
    Transform Lambda function that processes the data
    """
    try:
        # Get data from previous step
        body = event['body']
        file_name = event['file_name']
        df = pd.read_json(body)
        
        # Data cleaning
        df = df.dropna(how='all')
        df = df.drop_duplicates()
        df = df.reset_index(drop=True)
        json_data = df.to_json(orient='records')
        
        return {
            'statusCode': 200,
            'body': json_data,
            'file_name': file_name
        }
    
    except Exception as e:
        print(f"Error in transform function: {str(e)}")
        raise Exception(f"Transform function failed: {str(e)}")

def load_handler(event, context):
    """
    Load Lambda function that saves the data as CSV to S3 bucket
    """
    try:
        # Initialize S3 client
        s3_client = boto3.client('s3')
        
        # Get data from previous step
        body = event['body']
        file_name = event['file_name']
        df = pd.read_json(body)
        
        # Convert to CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        
        destination_bucket = 'csvfiledestination' 
        
        # Upload CSV to S3
        s3_client.put_object(
            Bucket=destination_bucket,
            Key=f"{file_name}.csv",
            Body=csv_buffer.getvalue()
        )
        
        return {
            'statusCode': 200,
            'message': f"Successfully saved {file_name}.csv to {destination_bucket}",
            'destination_bucket': destination_bucket,
            'file_name': f"{file_name}.csv"
        }
    
    except Exception as e:
        print(f"Error in load function: {str(e)}")
        raise Exception(f"Load function failed: {str(e)}")

def lambda_handler(event, context):
    """
    Main handler that orchestrates the ETL process
    """
    try:
        # Extract function
        extract_result = extract_handler(event, context)
        if extract_result['statusCode'] != 200:
            raise Exception("Error: Extract step failed")
            
        # Transform function
        transform_result = transform_handler(extract_result, context)
        if transform_result['statusCode'] != 200:
            raise Exception("Error: Transform step failed")
            
        # Load function
        load_result = load_handler(transform_result, context)
        if load_result['statusCode'] != 200:
            raise Exception("Error: Load step failed")
            
        return {
            'statusCode': 200,
            'message': 'Serverless ETL process completed successfully!',
            'details': load_result
        }
        
    except Exception as e:
        print(f"Error in ETL process: {str(e)}")
        return {
            'statusCode': 500,
            'message': f"ETL process failed: {str(e)}"
        }