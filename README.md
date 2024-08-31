# Team Assignment #1
## Data Sourcing

This is Team BadDataBusters - Akhil Chintalapati and John Rohit Ernest Jayaraj

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

### TMDB Movie Data Exploration and Visualization

This repository contains a set of Python scripts and functions designed to interact with The Movie Database (TMDB) API, perform data analysis, and visualize movie data. The primary focus is on fetching movie details, displaying movie posters, generating word clouds of movie titles etc.

### Contents

* TMDB API Client: A class for interacting with the TMDB API.

  get_top_rated_movies(page=1): Fetches the top-rated movies.
  get_movie_details(movie_id): Retrieves detailed information about a specific movie.
  search_movies(query, page=1): Searches for movies based on a keyword.
  get_movies_by_genre(genre_id, page=1): Fetches movies based on their genre.
  get_movie_poster(poster_path, save_path=None): Fetches and optionally saves a movie poster.
  
* Exploratory Data Analysis (EDA): Preliminary analysis of the movie data to gain insights.

* Visualizations: Included to explore the distribution of movie ratings, identify patterns, and understand relationships within the data.




