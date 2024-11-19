from io import StringIO
import pandas as pd
import json

def lambda_handler(event, context):
    try:
        # Extract data from the event
        data = event.get("body")
        if not data:
            raise ValueError("No data received.")

        print("Successfully loaded data.")

        data = pd.read_csv(StringIO(data))

        data = data[['Area Name', 'Sex', 'Value']]

        data = data.sort_values(by="Value", ascending=False)

        serialized_data = data.to_json(orient="records")

        return {
            'statusCode': 200,
            'body': serialized_data  
        }

    except Exception as e:
        print(f"Exception occurred: {e}")
        return {'statusCode': 500, 'body': str(e)}
