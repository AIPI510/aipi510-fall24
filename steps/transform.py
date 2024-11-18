# lambda function assumes that the 'data' key in the API response always contains a list of dictionaries, each representing a stock entry.

import json
import pandas as pd
import io




def lambda_handler(event, context):
    transform_response = lambda response: pd.DataFrame(json.loads(response)['data'])
    df = transform_response(event)

    # Convert DataFrame to CSV string
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_string = csv_buffer.getvalue()

    return {
        'statusCode': 200,
        'body': csv_string('Lambda function executed successfully'),
        'headers': {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=data.csv'
        }
    }
