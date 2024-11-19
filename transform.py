import boto3
import json

# -- Overview -- 
# The Transform Stage is the second phase of the ETL (Extract, Transform, Load) pipeline. 
# This stage processes cleaned data from the Extract Stage to generate meaningful insights. 
# Specifically, it aggregates startup funding amounts by city, enabling data-driven analysis of 
# which cities are attracting the most investment.


#-----------------------------------------------------------------------------------------------------------------------------------------------------#

# S3 client helps us fetch data from one bucket (Intermediate Storage) and send it wherever it’s needed next.
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Imagine you're a startup founder, and you’ve just hired someone to organize your funding data.
        # They tell you where the cleaned-up data is stored (bucket name and file key). 
        # We’re retrieving that information here.
        bucket_name = event['bucket']  # This is the bucket where cleaned data is stored temporarily.
        file_key = event['key']  # And this is the name of the cleaned file we’re about to process.

        # **1: Fetch Cleaned Data**
        # Our cleaned funding data is sitting in S3 (Intermediate Storage). We’re going to fetch it.
        # Think of this as pulling a Google Sheet (With the right permissions for once) someone just shared with you.
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
    
        data = json.loads(response['Body'].read())

        # **2: Transform the Data**
        # Let’s do something useful with this data: calculate how much funding each city has received.
        # This step is like analyzing your startup’s traction — where’s the money really coming from?
        city_funding = {}  # This will be our final report: {City: Total Funding}

        # We loop through each record in the cleaned data to build our city-wise funding report.
        for record in data:
            # Grab the city name and funding amount from each record.
            city = record.get("City")  # e.g., "Bangalore"
            amount = record.get("AmountUSD", 0)  # Funding amount (defaults to 0 if not present)

            if city:  # We’re only interested in records with valid city names.
                # Add the funding amount to the city’s total. If it’s the first time seeing this city, start at 0.
                city_funding[city] = city_funding.get(city, 0) + amount

        # By the end of this loop, we’ll have something like:
        # {"Bangalore": 3000000, "Mumbai": 2000000, "Delhi": 1500000}

        # **3: Return the Transformed Data**
        return {"transformed_data": city_funding}

    except Exception as e:
        # **4: Error Handling**
        # If something goes wrong — like missing data or permissions issues — we’ll catch it here.
        # Instead of crashing the pipeline, we return an error message for debugging.
        return {"error": str(e)}
