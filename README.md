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

### TMDB Movie Database

This repository contains a set of Python scripts and functions designed to interact with The Movie Database (TMDB) API.

### Functionality

## TMDBAPIClient

The TMDBAPIClient class provides methods to interact with the TMDB API.

## *  get_top_rated_movies(page=1): Fetches a list of top-rated movies. Returns movie details including ID, title, release date, popularity, vote average, and genre IDs.<br><br>

get_movie_details(movie_id): Retrieves detailed information about a specific movie by its ID. Returns data including ID, title, language, overview, popularity, release date, revenue, runtime, status, vote average, and vote count.<br><br>

search_movies(query, page=1): Searches for movies based on a query. Returns a list of movies with details such as ID, title, overview, release date, popularity, vote average, vote count, original language, and genre IDs.<br><br>

get_movies_by_genre(genre_id, page=1): Fetches movies by a specific genre ID. Returns a list of movies including ID, title, release date, popularity, vote average, and genre IDs.<br><br>

get_movie_poster(poster_path, save_path=None): Retrieves and displays or saves a movie poster image based on its path.

  
* Exploratory Data Analysis (EDA): Preliminary analysis of the movie data to gain insights.

* Visualizations: Included to explore the distribution of movie ratings, identify patterns, and understand relationships within the data.




