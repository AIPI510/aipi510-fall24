# Team Assignment 10 - Data Engineering

**Team RRKing**

**Reina Shi, Roxanne Wang**


## Overview
This ETL pipeline extracts paper data from the Hugging Face Arxiver dataset, transforms it into a standardized format, and loads it into an S3 bucket. The pipeline is orchestrated using AWS Step Functions.

Dataset URL: https://huggingface.co/datasets/neuralwork/arxiver 

## Architecture
- **Extract**: Fetches data from Hugging Face API
- **Transform**: Cleans and standardizes the data
- **Load**: Saves processed data to S3
- **Error Handler**: Manages errors across all stages
- **Step Functions**: Orchestrates the workflow

## Implementation Details

### Extract Stage
1. Connects to Hugging Face API
2. Fetches paper data with size limits
3. Initial data validation
4. Error handling and logging

### Transform Stage
1. Data cleaning and standardization
2. Field validation
3. Format standardization
4. Error handling

### Load Stage
1. S3 bucket write operations
2. Data persistence
3. Success/failure reporting
4. Error handling

## Error Handling
- Each function includes comprehensive error handling
- Step Functions includes error handling and retry logic