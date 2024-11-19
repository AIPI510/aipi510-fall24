import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Handle errors from the ETL pipeline and log them appropriately.
    Args:
        event: Error information and metadata
        context: AWS Lambda context
    Returns:
        dict: Error details
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