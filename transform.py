import json
import logging
import csv
from io import StringIO

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        # Parse the incoming event to extract data
        extracted_data = json.loads(event['body'])['extracted_data']

        # Transform: Example transformation (count rows)
        csv_reader = csv.reader(StringIO("\n".join(extracted_data)))
        row_count = sum(1 for _ in csv_reader) - 1  # Subtract header row

        # Log the transformation
        logger.info(f"Transformed data: Row count is {row_count}")

        # Return the transformed data
        return {
            'statusCode': 200,
            'body': json.dumps({'aggregated_data': {'row_count': row_count}})
        }

    except KeyError as e:
        logger.error(f"Missing key in event: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing or incorrect input format.'})
        }

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'An unexpected error occurred.'})
        }
