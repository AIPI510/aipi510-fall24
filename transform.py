# Transform lambdafunction
import json

def lambda_handler(event, context):
    """
    Normalizes the data passed to this function
    Accepts: JSON with a body containing a 2D list. 
    The first list is a header list, and the remaining contains data

    Returns: Transformed data
    """
    try:
        forest_fires_2D = event['body']
        M = len(forest_fires_2D)
        N = len(forest_fires_2D[0])

        output_csv = []
        # Copying header
        output_csv.append(forest_fires_2D[0])
        mean_csv = [0 for _ in range(N)]
        var_csv = [0 for _ in range(N)]

        # Ignoring the first line, since it is a header line
        for i in range(1, M):
            for j in range(N):
                current_value = float(forest_fires_2D[i][j])
                mean_csv[j] += current_value / (M - 1)
            
        for i in range(1, M):
            for j in range(N):
                current_value = float(forest_fires_2D[i][j])
                var_csv[j] += (current_value - mean_csv[j])**2 / (M - 1)

        for i in range(1, M):
            k = []
            for j in range(N):
                current_value = float(forest_fires_2D[i][j])
                k.append((current_value - mean_csv[j]) / (var_csv[j])**0.5)
            output_csv.append(k)

        return {
            'statusCode': 200,
            'body': output_csv
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
