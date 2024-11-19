import pandas as pd
import io

def lambda_handler(event, context):
    try:
        # Get the CSV data from the event
        csv_data = event['data']
        
        # Read the CSV content into a pandas DataFrame
        data = pd.read_csv(io.StringIO(csv_data))
        
        # Ensure the State column is treated as a string and normalize values
        data['State'] = data['State'].astype(str).str.strip().str.upper()
        
        # Filter for vehicles in NC
        nc_data = data[data['State'] == 'NC']
        
        # Convert the filtered DataFrame back to CSV
        filtered_csv = nc_data.to_csv(index=False)
        
        return {
            'status': 'success',
            'filtered_data': filtered_csv
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
