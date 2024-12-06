import json
import requests
import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ETL Extract Function
def extract_data(event, context):
    """
    Extract data from HuggingFace API
    """
    try:
        # HuggingFace API setup
        HF_TOKEN = "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"
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Accept": "application/json"
        }
        
        # Using the correct dataset API endpoint with fewer records
        dataset_name = "neuralwork/arxiver"
        api_url = f"https://datasets-server.huggingface.co/rows"
        params = {
            "dataset": dataset_name,
            "config": "default",
            "split": "train",
            "offset": 0,
            "length": 3  # Reduced to 3 papers to stay within size limit
        }
        
        logger.info(f"Fetching dataset: {dataset_name}")
        response = requests.get(api_url, headers=headers, params=params)
        
        response.raise_for_status()
        data = response.json()
        
        # Extract paper data with trimmed content
        papers = []
        for row in data.get('rows', []):
            row_data = row.get('row', {})
            # Trim long text fields
            abstract = row_data.get('abstract', '')[:500] if row_data.get('abstract') else ''
            markdown = row_data.get('markdown', '')[:1000] if row_data.get('markdown') else ''
            
            paper = {
                'id': row_data.get('paper_id', '')[:50],
                'title': row_data.get('title', '')[:200],
                'abstract': abstract,
                'authors': row_data.get('authors', [])[:5],  # Limit number of authors
                'publication_date': row_data.get('published', '')[:10],
                'url': f"https://arxiv.org/abs/{row_data.get('paper_id', '')}"[:100],
                'markdown_content': markdown
            }
            papers.append(paper)
        
        logger.info(f"Successfully processed {len(papers)} papers")
        
        # Log size of response for debugging
        response_size = len(json.dumps(papers))
        logger.info(f"Response size: {response_size} bytes")
        
        return {
            "statusCode": 200,
            "body": json.dumps(papers)
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Failed to fetch data from Hugging Face API",
                "details": str(e)
            })
        }
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Internal server error",
                "details": str(e)
            })
        }

# ETL Transform Function
def transform_data(event, context):
    """
    Transform the extracted data
    """
    # Extract data from the event object
    if 'body' in event:
        data = json.loads(event['body'])
    else:
        data = event
    
    # Ensure data is a list of dictionaries
    if isinstance(data, str):
        data = json.loads(data)
    elif isinstance(data, dict):
        data = [data]
    
    # Perform data cleaning and formatting
    transformed_data = []
    for item in data:
        if isinstance(item, dict):
            transformed_item = {
                'arxiv_id': item.get('id', '').strip(),
                'title': item.get('title', '').strip(),
                'abstract': item.get('abstract', '').strip(),
                'authors': [author.strip() for author in item.get('authors', [])],
                'publication_date': item.get('publication_date', '').strip(),
                'url': item.get('url', '').strip(),
                'markdown_content': item.get('markdown_content', '').strip()
            }
            transformed_data.append(transformed_item)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'transformed_data': transformed_data})
    }

# ETL Load Function
def load_data(event, context):
    """
    Load the transformed data into S3
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Extract transformed data from the event object
        if 'body' in event:
            body = json.loads(event['body'])
            transformed_data = body.get('transformed_data', [])
        else:
            transformed_data = event.get('transformed_data', [])
        
        logger.info(f"Transformed data to load: {json.dumps(transformed_data)}")
        
        # Define the destination S3 bucket and key
        s3_bucket = 'myhuggingfacebucket002'
        s3_key = 'transformed_data.json'
        
        # Initialize S3 client
        s3 = boto3.client('s3', region_name='us-east-2')
        
        # Convert transformed data to JSON
        transformed_data_json = json.dumps(transformed_data)
        
        # Upload the transformed data to the S3 bucket
        s3.put_object(
            Bucket=s3_bucket, 
            Key=s3_key, 
            Body=transformed_data_json
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Data successfully loaded into S3 bucket.',
                'bucket': s3_bucket,
                'key': s3_key
            })
        }
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error: {error_msg}")
        return {
            'statusCode': 500,
            'error': error_msg,
            'body': json.dumps({
                'error': error_msg,
                'stage': 'Load'
            })
        }

# Error Handler Function
def handle_error(event, context):
    """
    Handle errors from the ETL pipeline and log them appropriately
    """
    error = event.get('error', 'Unknown error')
    stage = event.get('stage', 'Unknown stage')
    
    error_message = f"Error in {stage} stage: {error}"
    logger.error(error_message)
    
    return {
        'statusCode': 500,
        'body': json.dumps({
            'error': error_message,
            'stage': stage
        })
    }

# AWS Step Functions State Machine Definition
STEP_FUNCTIONS_DEFINITION = {
    "Comment": "ETL Pipeline for Arxiver Dataset",
    "StartAt": "Extract",
    "States": {
        "Extract": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-2:084375553688:function:etl-extract",
            "Retry": [
                {
                    "ErrorEquals": [
                        "Lambda.ServiceException",
                        "Lambda.AWSLambdaException",
                        "Lambda.SdkClientException"
                    ],
                    "IntervalSeconds": 2,
                    "MaxAttempts": 3,
                    "BackoffRate": 2
                }
            ],
            "Catch": [
                {
                    "ErrorEquals": ["States.ALL"],
                    "ResultPath": "$.error",
                    "Next": "ExtractError"
                }
            ],
            "Next": "CheckExtractStatus"
        },
        "CheckExtractStatus": {
            "Type": "Choice",
            "Choices": [
                {
                    "Variable": "$.statusCode",
                    "NumericEquals": 200,
                    "Next": "Transform"
                }
            ],
            "Default": "ExtractError"
        },
        "Transform": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-2:084375553688:function:etl-transform",
            "Retry": [
                {
                    "ErrorEquals": [
                        "Lambda.ServiceException",
                        "Lambda.AWSLambdaException",
                        "Lambda.SdkClientException"
                    ],
                    "IntervalSeconds": 2,
                    "MaxAttempts": 3,
                    "BackoffRate": 2
                }
            ],
            "Catch": [
                {
                    "ErrorEquals": ["States.ALL"],
                    "ResultPath": "$.error",
                    "Next": "TransformError"
                }
            ],
            "Next": "CheckTransformStatus"
        },
        "CheckTransformStatus": {
            "Type": "Choice",
            "Choices": [
                {
                    "Variable": "$.statusCode",
                    "NumericEquals": 200,
                    "Next": "Load"
                }
            ],
            "Default": "TransformError"
        },
        "Load": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-2:084375553688:function:etl-load",
            "Retry": [
                {
                    "ErrorEquals": [
                        "Lambda.ServiceException",
                        "Lambda.AWSLambdaException",
                        "Lambda.SdkClientException"
                    ],
                    "IntervalSeconds": 2,
                    "MaxAttempts": 3,
                    "BackoffRate": 2
                }
            ],
            "Catch": [
                {
                    "ErrorEquals": ["States.ALL"],
                    "ResultPath": "$.error",
                    "Next": "LoadError"
                }
            ],
            "Next": "CheckLoadStatus"
        },
        "CheckLoadStatus": {
            "Type": "Choice",
            "Choices": [
                {
                    "Variable": "$.statusCode",
                    "NumericEquals": 200,
                    "Next": "Success"
                }
            ],
            "Default": "LoadError"
        },
        "ExtractError": {
            "Type": "Pass",
            "Parameters": {
                "error.$": "$.error",
                "stage": "Extract"
            },
            "Next": "Failed"
        },
        "TransformError": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-2:084375553688:function:etl-error-handler",
            "Parameters": {
                "error.$": "$.error",
                "stage": "Transform"
            },
            "Next": "Failed"
        },
        "LoadError": {
            "Type": "Task",
            "Resource": "arn:aws:lambda:us-east-2:084375553688:function:etl-error-handler",
            "Parameters": {
                "error.$": "$.error",
                "stage": "Load"
            },
            "Next": "Failed"
        },
        "Success": {
            "Type": "Succeed"
        },
        "Failed": {
            "Type": "Fail",
            "Error": "ETLError",
            "Cause": "Error during ETL process. Check CloudWatch logs for details."
        }
    }
}
