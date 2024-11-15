# Team Assignment #8
## Data Engineering

## Author: Haochen Li

Reference: https://medium.com/@akhilxox/deploying-the-ultimate-dog-vs-384bc7a920ed

Instruction for the whole process:
- step0 set up aws bucket, aws access key and secret
- step1 install CLI. For code space bash: 
`curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install`

- step2 follow the instructions on reference (thanks to Akhil), but remember to change the bucket name and resource, function name (change to the same of the filename where the lambda_handler rest), then add the following code to the end of yml to avoid oversize error.
```yml
package:
  individually: true

  exclude:
    - node_modules/**  # Exclude node modules (not needed for Python Lambda)
    - .git/**  # Exclude git history and configurations
    - .serverless/**  # Exclude Serverless build artifacts
    - aws/**  
    - model/training.py  # Exclude training script (only inference needed)
    - model/cat_dog_model.onnx  # Exclude ONNX model 
    - model/cat_dog_model.pkl  # Exclude the other model
    - _pycache_  # Exclude Python cache files
    - awscliv2.zip  # Exclude large AWS CLI installation file
    - "*.md"  # Exclude markdown files
    - "*.json"  # Exclude JSON files 
    - "*.txt"  # Exclude any text files not required for runtime
    - "README.md"  # Exclude README file
    - package-lock.json  # Exclude Node.js lock files
    - package.json  # Exclude Node.js package file
    - .venv/**  # Exclude virtual environment
```

- step3 run the following code to check the result `curl -X POST https://2vyc0ptf3g.execute-api.us-east-1.amazonaws.com/dev/predict -H "Content-Type: application/json" -d '{"features": [28, 3, 8, 1, 5]}'`

* Steps taken for Extract are documented
* Steps taken for Transform are documented
* Steps taken for Load are documented
* The Step Functions state machine is documented

# Following are the requirements by assignments

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


