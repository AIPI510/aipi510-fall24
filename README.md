# Team Assignment #1
This is Team Davis: Dave and Siddarth
## Data Sourcing
## Step 1
Navigate to https://dev.twitch.tv/console . Log in to your Twitch account, creating one if you don't have one. 

## Step 2
If you have not done already, verify your email address. Additionally you will have to enable Two-Factor Authentication, so navigate to Security and Privacy (Click on your profile icon in the top right, click the drop down to get to Account Settings, Click on the Security and Privacy tab, and navigate and click to enable 2FA). Be sure to refresh your console.

## Step 3
Select the Applications tab and click Register Your Application. Use this information to fill it out:
Name: Your choice
OAuth Redirect URLs: http://localhost:3000
Category: Your choice

## Step 4
Save two pieces of information. The first is your ClientID. The second is a secret, which can be aquired by clicking "New Secret". Add these pieces of information to your .env file.

## Step 5
Make sure the packages are installed in requirements.txt

## Step 6
With the command line, run the python file, and add a query to your argument. If everything works, you should have a list of all Twitch channels that belong in your query.

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

