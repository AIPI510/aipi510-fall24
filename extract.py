import boto3
import csv
import json

# -- Overview -- 
# This Lambda function is the first stage of a serverless ETL (Extract, Transform, Load) pipeline. 
# Its job is to extract and clean messy startup funding data from an S3 bucket and prepare it for further processing. 
# Think of it as the data janitor that makes sense of the chaos — fixing dates, removing unnecessary commas, 
# and ensuring every field is ready for prime-time analysis.

# The dataset we’re working with is Indian Startup Funding Data, containing information about when startups raised money, 
# how much they raised, who invested, and what industries they belong to. 
# This function does the Extract part of ETL, with a sprinkle of Transform for data cleaning.

# The ETL data pipeline, defined in the etl_pipeline_atl.json, orchestrates a serverless workflow using 
# AWS Step Functions to manage and process data efficiently. This ensures a seamless and fault-tolerant data workflow, 
# integrating all stages of the ETL process.



#-----------------------------------------------------------------------------------------------------------------------------------------------------#

# S3 client, our pipeline's delivery executive.
# It’ll fetch files from Amazon S3 (think of it as our data warehouse in the cloud) and return cleaned, shiny data later.
s3 = boto3.client('s3')


def lambda_handler(event, context):
    # First, we set up a storage spot for cleaned data because, the raw data we’re working with 
    # (funding details of Indian startups) can be a bit messy, just like the pitches at the Duke AI hackathon.
    bucket_name = 'etl-intermediate-storage'
    
    # This is the cleaned data’s new name when we upload it to our temporary S3 spot.
    file_key = 'extracted-data.json'
    
    # Here’s our raw material: a CSV file loaded with startup funding details.
    # Spoiler alert: we’re going to clean up names, dates, and even commas from the funding amounts (seriously, who does that?).
    source_file = 'startup_funding.csv'

    try:
        # **1: Let’s grab the CSV from our S3 warehouse**
        # Picture this: a dusty Excel sheet tucked away in the bucket `etl-indian-startup-funding`.
        # We fetch it like an intern running to grab chai (it's not chai tea) for the team.
        response = s3.get_object(Bucket='etl-indian-startup-funding', Key=source_file)
        
        # Now we’re cracking open the file and reading it line by line.
        lines = response['Body'].read().decode('utf-8').splitlines()

        # **2: Time for some serious data cleaning**
        reader = csv.DictReader(lines)
        
        # We’re going to build a shiny, cleaned-up dataset, just like how startups pivot to sound “fundable”.
        cleaned_data = []

        # Let’s dive into each row and clean the mess.
        for row in reader:
            cleaned_row = {
                "Date": row.get("Date dd/mm/yyyy", "").strip(),  # Date of funding (or when the founder sold their soul to VCs).
                "Startup": row.get("Startup Name", "").strip(),  # Name of the startup (cue buzzwords: “synergy”, “disruption”).
                "Industry": row.get("Industry Vertical", "").strip(),  # What space they’re in (no, “AI for Dosa Makers” isn’t valid).
                "SubVertical": row.get("SubVertical", "").strip(),  # The niche they’re chasing (probably still in beta).
                "City": row.get("City  Location", "").strip(),  # Where they’re based (a.k.a where they rented co-working space).
                "Investors": row.get("Investors Name", "").strip(),  # Who believed in their “vision” (or their PPT).
                "InvestmentType": row.get("InvestmentnType", "").strip(),  # Pre-seed? Seed? Series Z? Does it even matter anymore?
                "AmountUSD": parse_amount(row.get("Amount in USD", ""))  # The *real* deal: how much money they raised (post “adjustments”).
            }
            # Add the cleaned row to our list
            cleaned_data.append(cleaned_row)

        # **3: Save the cleaned data back to S3**
        # This cleaned dataset is now ready for the next stage. It’s like getting feedback on your MVP
        # and saying, “We’ll fix it in the next sprint.” Here, we save it in S3 for real.
        s3.put_object(
            Bucket=bucket_name, 
            Key=file_key,
            Body=json.dumps(cleaned_data),
            ContentType='application/json' 
        )

        return {"bucket": bucket_name, "key": file_key}

    except Exception as e:
        # If something breaks (a.k.a the demo doesn’t work), log the error and move on. 
        # We’re not here to fail silently — let’s make noise.
        return {"error": str(e)}


def parse_amount(amount):
    # Helper function to remove commas and make funding a proper number.
    try:
        return int(amount.replace(",", "")) if amount else 0
    except ValueError:
        # If something funky sneaks into the amount field (like “N/A”), we default to 0.
        return 0
