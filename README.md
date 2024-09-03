# Team Assignment #1 Tony Wang, Bill Yang
## Data Sourcing

# Reddit Scraper

## Description

`api_reddit.py` uses the PRAW library to scrape Reddit posts. It retrieves the title, text body, and comments from a specified Reddit post and saves the data to a CSV file. The script accepts a Reddit post URL as an argument from the command line.

## Features

- Scrapes Reddit post title, content, and comments.
- Outputs the data to a CSV file named `reddit.csv`.
- Simple command-line interface to specify the Reddit post URL.

## Requirements
- numpy==1.24.3
- praw==7.7.1
- pandas==2.0.3

## Install the dependencies
`pip install -r requirements.txt`

## Eg:
`python api_reddit.py "https://www.reddit.com/r/EngineeringStudents/comments/1f53a5b/finally_left_my_company_is_this_normal/"`
- this will output a csv file name 'reddit.csv' which contains the post's title, text body, and all comments.