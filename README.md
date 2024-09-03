# Team Assignment #1

## Team information
This is the team Wukong. And the members are Zejun Bai and Yiqing Liu.

## Overview
This script is used to fetch the air quality forecast dataset from the Transport for London (TfL) Unified API, specifically utilizing the AirQuality endpoint. The dataset is updated hourly and contains forecast data for the next few days. The script processes the data, stores it in a pandas DataFrame, and then saves the data as a CSV file.

## Features
1. Fetches air quality forecast data from the TfL Unified API.
2. Extracts and displays key information such as forecast type, forecast summary, and various pollutant levels.
3. Stores the processed data into a pandas DataFrame.
4. Saves the data as a CSV file named air_quality_forecast.csv.


## Usage
1. Clone the repository or download the script.
2. Run the script using Python: 
    ```bash
    python api_tfl_air_quality.py
    ```


## Instructions
1. Create a feature branch in the class GitHub repository for your team. 

2. Put together a code demo for your assigned topic. 
Code should be:
* Clean and well organized script
* Using best practices (if you aren’t sure, go back to the Premodule content)
* Well-commented
* Contains appropriate unit testing
* Clear name (ie ‘web-scraping-selenium.py’)

3. Create a <5 minute video documenting your topic and code demo. 

## Submission
To submit your code, make a PR into the data-sourcing-ta1 branch and add me and the TA as reviewers. In your PR, add the link to your demo video. Also, add any requirements (and versions) that are not currently in the requirements.txt file to the text of your PR.

## Topics
* Web scraping with Selenium
* Web scraping with Beautiful Soup
* Web scraping using requests
* Using Hugging Face API for getting datasets
* Use an API from a social platform (i.e. Strava, Twitter)
* Use the PubMed API
* [maybe] Collect sensor data from a Raspberry Pi (temperature sensor may be the easiest, but you can use any sensor)

## Rubric
### Code (30 points)
* Code is a script, not a notebook
* Code is clean and well organized
* Code is documented with docstrings and comments 
* Code is free of commented out code (ie debug print statements)
* Script has a clear name
* Branching and PRs were done appropriately
* Requirements are included in the text of the PR and are correct and versioned
* The code runs as documented

### Video (15 points)
* < 5 minutes
* The video is of mid-high production quality and doesn’t contain significant background noise 
* Video is well organized and clear
* Video documents topic and code effectively

