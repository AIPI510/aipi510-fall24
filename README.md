# Team Assignment #1
## Data Sourcing

## Overview

Welcome to the Team BadDataBusters repository! This project was collaboratively developed by Akhil Chintalapati and John Rohit Ernest Jayaraj as part of the data sourcing assignment (TA1). The project focuses on interacting with The Movie Database (TMDB) API, allowing users to fetch and analyze movie data.

## Team Members 
* Akhil Chintalapati
* John Rohit Ernest Jayaraj

## Functionality

This repository includes a set of Python scripts designed to interact with the TMDB API. The primary class TMDBAPIClient provides various methods to fetch and handle movie data from the API.

## Key Features

* get_top_rated_movies(page=1): Fetches a list of top-rated movies with details including ID, title, release date, popularity, vote average, and genre IDs.
* get_movie_details(movie_id): Retrieves detailed information about a specific movie by its ID, such as title, language, overview, popularity, release date, revenue, runtime, status, vote average, and vote count.
* search_movies(query, page=1): Searches for movies based on a provided query. Returns a list of matching movies with relevant details.
* get_movies_by_genre(genre_id, page=1): Fetches movies by a specific genre ID, returning a list that includes the movie's title, release date, popularity, and vote average.
* get_movie_poster(poster_path, save_path=None): Retrieves and displays or saves a movie poster image based on the provided poster path.

## Setup and Installation

1. Clone the Repository:

```bash
git clone https://github.com/AIPI510/aipi510-fall24/tree/ta1-BadDataBusters.git
cd ta1-BadDataBusters
```

2. Make Sure you Install all Requirements:

```bash
pip install -r requirements.txt
```

3. API Configuration: 

Add your TMDB API key to line 34 in "tmdb-api-scraping.py" script, generate yours at https://developer.themoviedb.org/docs/getting-started

```bash
api_key = "YOUR_TMDB_API_KEY"
```

4. Run the script:

```bash
python tmdb-api-scraping.py
```

5. View the Plots and Other Outputs:

After running the script, multiple plots will be saved directly to your working directory. Additionally, a YouTube link will automatically open in your default browser.

## Citations and Imp Stuff:
  1. Data: "This product uses the TMDB API but is not endorsed or certified by TMDB. 
            This is a simple project created as part of an educational assignment, and 
            it is not intended for commercial purposes. For more information, visit 
            The Movie Database (TMDB) at https://www.themoviedb.org/ [accessed last on August 30th 2024]."
 
  2. Images: "Movie images provided by The Movie Database (TMDB)."
 
  3. Reuse: "Feel free to reuse or modify this project for your own 'educational' purposes."

Thank you for your time!

With best regards,
Akhil & John

Default Information -->

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





