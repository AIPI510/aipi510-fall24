# Team Assignment #1
## Data Sourcing

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

---

### Open Trivia API

#### Team Impasta - Dayeon Kang, Shaunak Badani

How to use:
Install requirements in virtual env outside of root folder:
```
python3 -m venv ../ta1
source ../ta1/bin/activate
pip install -r requirements.txt
```

Running the program:
```
usage: python3 api_trivia.py [-h] [--category {9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32}] [-n N]

Get questions from the Open Trivia API

options:
  -h, --help            show this help message and exit
  --category {9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32}
                        {"9": "General Knowledge", "10": "Entertainment: Books", "11": "Entertainment: Film", "12": "Entertainment: Music", "13": "Entertainment: Musicals & Theatres",
                        "14": "Entertainment: Television", "15": "Entertainment: Video Games", "16": "Entertainment: Board Games", "17": "Science & Nature", "18": "Science: Computers",
                        "19": "Science: Mathematics", "20": "Mythology", "21": "Sports", "22": "Geography", "23": "History", "24": "Politics", "25": "Art", "26": "Celebrities", "27":
                        "Animals", "28": "Vehicles", "29": "Entertainment: Comics", "30": "Science: Gadgets", "31": "Entertainment: Japanese Anime & Manga", "32": "Entertainment: Cartoon &
                        Animations"}
  -n N                  Number of questions to fetch
```

Parameters:
-n : Number of questions to fetch, default 10
--category: Category to fetch questions from, ranges from 9 to 32, default is None (questions from all categories are fetched)

Saves the questions to a csv file "trivia_questions.csv"