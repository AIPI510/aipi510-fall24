# Team Assignment #8
## Data Engineering

## Instructions
Design and implement a serverless ETL data pipeline using AWS Lambda and Step Functions to process data from a source, transform it, and load it into a destination.
### Requirements:
* Use AWS Lambda functions for each step of the ETL process
* Orchestrate the pipeline using AWS Step Functions
* Implement error handling and logging

### Steps:
#### Extract:
* Create a Lambda function to extract data from a source (e.g., S3 bucket, DynamoDB table, or external API)
* The function should retrieve the data and pass it to the next step
#### Transform:
* Create a Lambda function to transform the extracted data
* Implement data transformation of your choice (ie data cleaning, formatting, or aggregation)
#### Load:
* Create a Lambda function to load the transformed data into a destination (e.g., another S3 bucket, DynamoDB table, or RDS instance)
#### Orchestration:
* Design a Step Functions state machine to coordinate the three Lambda function
* Implement error handling and retry logic
#### Testing and Validation:
* Test the pipeline with sample data
* Verify that the data is correctly processed and loaded

## Submission
### Part 1:
Submit your Lambda function code for each step (Extract, Transform, Load) and your step functions state machine definition (JSON or YAML). 
To submit your code, make a PR into the etl-ta8 branch and add me and the TA as reviewers. 
### Part 2:
Submit a video (<3 mins) demonstrating that your Lambda functions work as expected. In the video, you should test the pipeline with sample data and verify that the data is correctly processed and loaded.

## Rubric
### Video (25 points)
* Video is <3 minutes
* Video walks through process clearly
* The pipeline is tested with sample data
* The Lambda functions works as expected
* The data is correctly processed and loaded

### Code (20 points)
* Code is clean and well organized
* Code is documented with docstrings and comments 
* Code is free of commented out code (ie debug print statements)
* Branching and PRs were done appropriately
* Steps taken for Extract are documented
* Steps taken for Transform are documented
* Steps taken for Load are documented
* The Step Functions state machine is documented


