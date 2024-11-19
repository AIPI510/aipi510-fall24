# Team assignment 10 - Team Impasta

### Extract
The extract function does the following:

- Load the csv file `forestfires.csv` from the S3 bucket named `shaunakbucket`.
- Return the csv as a 2D list wrapped in a JSON object

### Transform
The transform function does the following:

- Load the data received from the response body
- Calculates the mean and variance along the 0 axis (Along the rows)
- Normalizes the data by subtracting the mean and dividing by the variance.
- Returning the normalized data wrapped in a JSON file.


### Load

- Loads the response body obtained as a 2D list
- Writes the 2D list to a csv and stores it in the S3 bucket named `shaunakbucket`.


## Step Function State Machine

- `StartsAt` : Defines the starting point of the ETL orchestration.
- `States` : Defines the different states of the Step function in a sequential manner.
- `Extract`: First state, and links to the lambda function in the `Parameters.FunctionName` key. The `Next` parameter defines the lambda function to pass the output of `Extract` to. In this case, the next function is `Transform`.
- `Transform`: Second state, and links to the lambda function in `FunctionName`. `Next` function is the `Load` function.
- `Load`: Third state. Saves the data obtained into a csv format and stores it in the bucket. The `End` = true signifies that this is the last state of the step function.