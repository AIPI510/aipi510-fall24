import json
import pandas as pd
import io

def lambda_handler(event, context):
    '''
    Lambda function handler to transform data into CSV format.
    '''

    df = pd.DataFrame(json.loads(event['body'])['data'])

    # Convert DataFrame to CSV string
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_string = csv_buffer.getvalue()

    return {
        'statusCode': 200,
        'body': csv_string,
        'headers': {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=data.csv'
        }
    }
