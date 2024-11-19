# Transform lambda function
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Normalizes the data passed to this function
    Accepts: JSON with a body containing a 2D list. 
    The first list is a header list, and the remaining contains data

    Returns: Transformed data
    """
    try:
        logger.info("Initiated transform")
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

        logger.info("Mean: " + ','.join([str(x) for x in mean_csv]))
        logger.info("Variance: " + ','.join([str(x) for x in var_csv]))
        logger.info("Transform function completed!")

        return {
            'statusCode': 200,
            'body': output_csv
        }
    except Exception as e:
        logger.error("Run into error! " + str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }
