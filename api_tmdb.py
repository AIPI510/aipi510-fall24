# Contribution:
# By Akhil Chintalapati and John Rohan Ernest in the Context of AIPI510: Sourcing Data for Analytics Course.
# 
# Citations and Imp Stuff:
#  1. Data: "This product uses the TMDB API but is not endorsed or certified by TMDB. 
#            This is a simple project created as part of an educational assignment, and 
#            it is not intended for commercial purposes. For more information, visit 
#            The Movie Database (TMDB) at https://www.themoviedb.org/ [accessed last on August 30th 2024]."
# 
#  2. Images: "Movie images provided by The Movie Database (TMDB)."
# 
#  3. Reuse: "Feel free to reuse or modify this project for your own 'educational' purposes."

#**********************************************************************************************************************************************#
#**********************************************************************************************************************************************#

# 1. Setting Up the Environment

# Load the essentials
# %pip --quiet install requests numpy pandas matplotlib seaborn sklearn io PIL
import requests  # The web's best friend for making HTTP requests to the TMDB API
import numpy as np  # Because what’s data science without some numerical magic?
import pandas as pd  # The go-to for data manipulation and making sense of tabular data
import matplotlib.pyplot as plt  # Your canvas for painting beautiful visualizations
import seaborn as sns  # Adding flair to your plots with advanced visualizations
from sklearn.model_selection import train_test_split  # A tool to ensure your model isn't too clingy (a.k.a. avoids overfitting)
from sklearn.linear_model import LinearRegression  # The classic algorithm for predicting the future... or at least movie ratings
from sklearn.metrics import mean_squared_error  # For quantifying how far off our model is (so we can make it better!)
from io import BytesIO  # Handling image data like a pro
from PIL import Image  # Image processing at its finest, courtesy of TMDB
# from config import your_api_key_goes_here -- Ignore this completely
import os

api_key = "your_api_key_goes_here" # Your golden ticket to the TMDB API. ""Replace this with your own API key!""
# Generate your own API key at https://developer.themoviedb.org/docs/getting-started

#**********************************************************************************************************************************************#
#**********************************************************************************************************************************************#

# 2. Building the backbone for interacting with the TMDB API
class TMDBAPIClient:
    """
    A client to interact with The Movie Database (TMDB) API.

    Attributes:
        api_key (str): The API key required to authenticate with the TMDB API.
        base_url (str): The base URL for the TMDB API.
        image_base_url (str): The base URL for fetching movie images from TMDB.
    """
    def __init__(self, api_key):
        """
        Initialize the TMDBAPIClient with the provided API key.

        Args:
            api_key (str): The API key for TMDB.
        """
        self.api_key = api_key  # Safeguarding your API key for all requests
        self.base_url = "https://api.themoviedb.org/3"  # The hub for all TMDB API endpoints
        self.image_base_url = "https://image.tmdb.org/t/p/w500"  # Where all the movie posters live

    # Fetching the top-rated movies from TMDB
    def get_top_rated_movies(self, page=1):
        """
        Fetch the top-rated movies from TMDB.

        Args:
            page (int): The page number to retrieve. Default is 1.

        Returns:
            list: A list of dictionaries containing information about top-rated movies.
        """
        endpoint = f"{self.base_url}/movie/top_rated"  # The specific endpoint for top-rated movies
        params = {"api_key": self.api_key, "page": page}  # Essential parameters: your API key and the desired page
        response = requests.get(endpoint, params=params)  # Sending the request to TMDB
        response.raise_for_status()  # Ensuring the request was successful
        return response.json()['results']  # Returning a list of the top-rated movies

    # Fetching detailed information about a specific movie
    def get_movie_details(self, movie_id):
        """
        Fetch detailed information about a specific movie.

        Args:
            movie_id (int): The ID of the movie to retrieve details for.

        Returns:
            dict: A dictionary containing detailed information about the movie.
        """
        endpoint = f"{self.base_url}/movie/{movie_id}"  # The endpoint for movie details, keyed by movie ID
        params = {"api_key": self.api_key}  # Including the API key in the request
        response = requests.get(endpoint, params=params)  # Sending the request to TMDB
        response.raise_for_status()  # Making sure there are no errors in the response
        return response.json()  # Returning the detailed movie data

    # Searching for movies based on a keyword
    def search_movies(self, query, page=1):
        """
        Search for movies based on a keyword.

        Args:
            query (str): The keyword to search for.
            page (int): The page number to retrieve. Default is 1.

        Returns:
            list: A list of dictionaries containing information about the search results.
        """
        endpoint = f"{self.base_url}/search/movie"  # The endpoint for searching movies
        params = {"api_key": self.api_key, "query": query, "page": page}  # Search parameters: API key, search query, and page number
        response = requests.get(endpoint, params=params)  # Sending the search request
        response.raise_for_status()  # Checking for HTTP errors
        return response.json()['results']  # Returning the search results

    # Fetching movies based on their genre
    def get_movies_by_genre(self, genre_id, page=1):
        """
        Fetch movies based on their genre.

        Args:
            genre_id (int): The ID of the genre to filter by.
            page (int): The page number to retrieve. Default is 1.

        Returns:
            list: A list of dictionaries containing information about movies in the specified genre.
        """
        endpoint = f"{self.base_url}/discover/movie"  # The endpoint for discovering movies by genre
        params = {"api_key": self.api_key, "with_genres": genre_id, "page": page}  # Parameters: API key, genre ID, and page number
        response = requests.get(endpoint, params=params)  # Sending the request to discover movies by genre
        response.raise_for_status()  # Ensuring the request is successful
        return response.json()['results']  # Returning a list of movies within the specified genre

    # Fetching and displaying movie posters
    def get_movie_poster(self, poster_path, save_path=None):
        """
        Fetch and display or save a movie poster.

        Args:
            poster_path (str): The path to the movie poster.
            save_path (str, optional): The path to save the poster image locally. Defaults to None.

        Returns:
            None
        """
        if poster_path:  # Ensuring that a poster path is provided
            image_url = f"{self.image_base_url}{poster_path}"  # Constructing the full URL for the movie poster
            response = requests.get(image_url)  # Requesting the image from TMDB
            image = Image.open(BytesIO(response.content))  # Opening the image data using PIL

            if save_path:  # If a save path is provided
                image.save(save_path)  # Save the poster locally
            else:
                image.show()  # Otherwise, display the poster

        else:
            print("No poster path provided.")  # Log a message if there's no poster path to work with

#**********************************************************************************************************************************************#
#**********************************************************************************************************************************************#

# 3. Performing Exploratory Data Analysis (EDA)

import numpy as np

# A comprehensive function to perform Exploratory Data Analysis (EDA) on movie data,
# including outlier detection and essential preprocessing steps.
def perform_eda(movies):
    """
    Perform exploratory data analysis (EDA) on movie data, including outlier detection
    and essential preprocessing steps.

    Args:
        movies (list): A list of dictionaries, each containing data about a movie.

    Returns:
        pd.DataFrame: A processed DataFrame ready for analysis.
    """
    df = pd.DataFrame(movies)  # Transform the list of movies into a well-structured DataFrame.

    # Ensure the data types are correct for analysis.
    df['release_date'] = pd.to_datetime(df['release_date'])  # Convert release dates to datetime for time-based analysis.
    df['vote_average'] = df['vote_average'].astype(float)  # Ensure ratings are floats for accurate calculations.
    df['popularity'] = df['popularity'].astype(float)  # Convert popularity scores to floats for consistency.

    # Handle any missing data to maintain the integrity of our dataset.
    # We fill missing numeric values with the median, a robust measure against outliers.
    numeric_columns = df.select_dtypes(include=[np.number]).columns  # Select all numeric columns for this operation.
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())  # Fill in missing values with medians.
    df.dropna(inplace=True)  # Drop rows where categorical data is missing, to keep things clean.

    # Outlier detection and removal to ensure our analysis isn't skewed.
    # We use the z-score method to identify outliers that fall beyond 3 standard deviations from the mean.
    z_scores = np.abs((df[['vote_average', 'popularity']] - df[['vote_average', 'popularity']].mean()) 
                      / df[['vote_average', 'popularity']].std())  # Calculate z-scores to spot outliers.
    df = df[(z_scores <= 3).all(axis=1)]  # Filter out outliers to keep the data robust.

    # Scaling our numeric features so they play nicely with machine learning models.
    # This ensures that all features contribute equally to the model, without one dominating the others.
    # scaler = StandardScaler()
    # df[['vote_average', 'popularity']] = scaler.fit_transform(df[['vote_average', 'popularity']])

    # Let’s create a 2x2 grid of visualizations to explore the processed data.
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))  # Set up a 2x2 grid for our plots.

    # Visualize the distribution of movie ratings after preprocessing.
    sns.histplot(df['vote_average'], bins=10, kde=True, ax=axes[0, 0])  # Top-left: Distribution of ratings.
    axes[0, 0].set_title('Distribution of Movie Ratings (Processed)')  # Give the plot a descriptive title.
    axes[0, 0].set_xlabel('Scaled Rating')  # Label the x-axis.
    axes[0, 0].set_ylabel('Number of Movies')  # Label the y-axis.

    # Analyze the number of movies released each year.
    df['year'] = df['release_date'].dt.year  # Extract the year from the release date for year-wise grouping.
    movies_per_year = df.groupby('year').size()  # Count the number of movies released each year.
    movies_per_year.plot(kind='bar', ax=axes[0, 1])  # Top-right: Number of movies by release year.
    axes[0, 1].set_title('Number of Movies Released Per Year')  # Title the plot for clarity.
    axes[0, 1].set_xlabel('Year')  # Label the x-axis.
    axes[0, 1].set_ylabel('Number of Movies')  # Label the y-axis.

    # Visualize the distribution of movie popularity after preprocessing.
    sns.histplot(df['popularity'], bins=10, kde=True, color='green', ax=axes[1, 0])  # Bottom-left: Popularity distribution.
    axes[1, 0].set_title('Distribution of Movie Popularity (Processed)')  # Title the plot.
    axes[1, 0].set_xlabel('Scaled Popularity')  # Label the x-axis.
    axes[1, 0].set_ylabel('Number of Movies')  # Label the y-axis.

    # Examine the relationship between popularity and rating.
    sns.scatterplot(x='popularity', y='vote_average', data=df, ax=axes[1, 1], color='orange')  # Bottom-right: Popularity vs Rating.
    axes[1, 1].set_title('Movie Ratings vs Popularity (Processed)')  # Title the plot.
    axes[1, 1].set_xlabel('Scaled Popularity')  # Label the x-axis.
    axes[1, 1].set_ylabel('Scaled Rating')  # Label the y-axis.

    # Ensure our plots are neatly arranged without overlapping.
    plt.tight_layout()  # Adjust the layout for a clean, organized presentation.
    save_path = os.path.join("basic_eda.png")
    plt.savefig(save_path) # Display the grid of plots.

    return df  # Return the cleaned and preprocessed DataFrame for further analysis.

# Example usage to fetch and analyze top-rated movies
client = TMDBAPIClient(api_key)  # Initialize the TMDB API client

# Fetch top-rated movies and perform EDA with preprocessing
top_rated_movies = client.get_top_rated_movies(page=1)  # Get the first page of top-rated movies
movies_df = perform_eda(top_rated_movies)  # Dive into EDA on the fetched movie data

# Let's showcase the top 10 most popular movies

def visualize_top_movies_by_popularity(movies):
    """
    Visualize the top 10 most popular movies using a bar plot.

    Args:
        movies (list): A list of dictionaries, each containing data about a movie.

    Returns:
        None
    """
    # Transform the movie data into a DataFrame and grab the top 10 based on popularity
    df = pd.DataFrame(movies).sort_values(by='popularity', ascending=False).head(10)

    # Create a bar plot to highlight these crowd-pleasers
    plt.figure(figsize=(12, 6))
    sns.barplot(x='popularity', y='title', data=df, palette="dark")
    plt.title('Top 10 Movies by Popularity', fontsize=18)
    plt.xlabel('Popularity')
    plt.ylabel('Movie Title')
    save_path = os.path.join("top_10_popular_movies.png")
    plt.savefig(save_path) # Display the grid of plots. 
# Example usage:
visualize_top_movies_by_popularity(top_rated_movies)

# Let's dive into the connection between popularity and rating with a scatter plot
def visualize_popularity_vs_rating(movies):
    """
    Visualize the relationship between movie popularity and average rating using a scatter plot.

    Args:
        movies (list): A list of dictionaries, each containing data about a movie.

    Returns:
        None
    """
    # Transform the movie data into a DataFrame for easy handling
    df = pd.DataFrame(movies)

    # Create a scatter plot to reveal the relationship between a movie's popularity and its average rating
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='popularity', y='vote_average', data=df, hue='vote_average', size='popularity', 
                    palette="coolwarm", sizes=(20, 200))
    plt.title('Popularity vs. Rating', fontsize=18)
    plt.xlabel('Popularity')
    plt.ylabel('Average Rating')
    plt.legend(title='Rating', loc='best')
    save_path = os.path.join("pop_vs_ratings.png")
    plt.savefig(save_path) # Display the grid of plots. 
# Example usage:
visualize_popularity_vs_rating(top_rated_movies)

#**********************************************************************************************************************************************#
#**********************************************************************************************************************************************#

# 4. Bringing the Fun Factor!

#### a.  Fetching and Showcasing Movie Posters 

import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

def display_movie_posters_grid(movies, client, num_posters=5):
    """
    Display a grid of movie posters for the specified number of top movies.

    Args:
        movies (list): A list of dictionaries, each containing data about a movie.
        client (TMDBAPIClient): An instance of TMDBAPIClient to fetch movie posters.
        num_posters (int): The number of posters to display. Default is 5.

    Returns:
        None
    """
    # Roll out the red carpet for our movie posters!
    fig, axes = plt.subplots(1, num_posters, figsize=(15, 5))  # Set up a 1x5 grid, just like at the cinema

    # Step right up and enjoy the show! We're about to unveil the top `num_posters` movies.
    for i, movie in enumerate(movies[:num_posters]):
        poster_path = movie['poster_path']  # Get the path to the movie's glamorous poster
        if poster_path:
            image_url = f"{client.image_base_url}{poster_path}"  # Build the URL to fetch the poster
            response = requests.get(image_url)  # Grab that poster from the web
            img = Image.open(BytesIO(response.content))  # Open the image like the curtain at a premiere

            # Showtime! Display each poster in its very own subplot
            axes[i].imshow(img)
            axes[i].set_title(movie['title'], fontsize=10)  # Add the movie title, because every star deserves credit
            axes[i].axis('off')  # Turn off the axis so the poster can shine without distractions

    plt.tight_layout()  # Make sure our grid looks as polished as the Hollywood Walk of Fame
    save_path = os.path.join("movie_posters_grid.png")
    plt.savefig(save_path) # And... action! Let's see those posters

# Example usage:
client = TMDBAPIClient(api_key)  # Get ready to roll with the TMDB API client

# Fetch top-rated movies
top_rated_movies = client.get_top_rated_movies(page=1)  # Get the latest hits from the top-rated list

# Display the top 5 movie posters in a glorious grid
display_movie_posters_grid(top_rated_movies, client, num_posters=5)  # Lights, camera, posters!


#### b. Whipping Up a Vibrant Word Cloud of Movie Titles

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Generate a word cloud that's as colorful as the movies themselves
def generate_colored_wordcloud(movies):
    """
    Generate a colorful word cloud from the titles of the provided movies.

    Args:
        movies (list): A list of dictionaries, each containing data about a movie.

    Returns:
        None
    """
    # Mix all those movie titles into one big wordy smoothie
    titles = ' '.join([movie['title'] for movie in movies])
    
    # Blend up a word cloud with a splash of color and a dash of style
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='skyblue',  # Because who doesn't love a sky-blue day?
        colormap='rainbow',  # Rainbow colors for that extra pop
        contour_color='black',  # A sleek black contour to keep things classy
        contour_width=1
    ).generate(titles)

    # Serve up the word cloud for all to enjoy
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Axes? We don't need no stinkin' axes!
    plt.title('Word Cloud: Top-Rated Movie Titles', fontsize=20, color='navy')  # A title that says, "Look at me!"
    save_path = os.path.join("wordcloud.png")
    plt.savefig(save_path)

# Example usage:
top_rated_movies = client.get_top_rated_movies()  
generate_colored_wordcloud(top_rated_movies)  # Whip up and display that colorful word cloud


#### c. Uncover and flaunt the dominant colors from each movie poster

from PIL import Image  # Bringing in the big guns for image magic
import requests  # Because we need to fetch things from the internet
from io import BytesIO  # To handle image data like a pro
import matplotlib.pyplot as plt  # For when we want to show off our colorful findings
from sklearn.cluster import KMeans  # The mastermind behind finding dominant colors
import numpy as np  # The Swiss Army knife of array manipulation

# Function to extract and display dominant colors from movie posters
def extract_poster_colors(movies, client, num_colors=5):
    """
    Extract and display the dominant colors from the poster of the top movie.

    Args:
        movies (list): A list of dictionaries, each containing data about a movie.
        client (TMDBAPIClient): An instance of TMDBAPIClient to fetch movie posters.
        num_colors (int): The number of dominant colors to extract. Default is 5.

    Returns:
        None
    """
    for movie in movies[:1]:  # We're keeping it simple with the top movie
        poster_path = movie['poster_path']  # Get the golden ticket (poster path)
        if poster_path:  # No poster path? No problem... we just skip it
            image_url = f"{client.image_base_url}{poster_path}"  # Build the URL to fetch the poster
            response = requests.get(image_url)  # Make the internet work for us and get that poster
            img = Image.open(BytesIO(response.content))  # Open the image like a digital treasure map
            img = img.resize((100, 150))  # Shrink it down to make our lives easier (and faster)
            img_np = np.array(img).reshape(-1, 3)  # Turn the image into a bunch of colorful dots

            # Time to let KMeans do its thing and find the top N colors
            kmeans = KMeans(n_clusters=num_colors)  # KMeans: the color detective
            kmeans.fit(img_np)  # Find the color culprits hiding in the pixels
            colors = kmeans.cluster_centers_.astype(int)  # Get the list of suspects (top colors)

            # Now, let's show off those colors because they deserve the spotlight too!
            plt.figure(figsize=(8, 2))  # Set the stage for our color show
            plt.imshow([colors])  # Display the colorful suspects in a lineup
            plt.axis('off')  # Who needs axes? They just get in the way of our color parade
            plt.title(f"Dominant Colors in '{movie['title']}' Poster")  # Give our plot a fancy title
            save_path = os.path.join("extract_poster_colors.png")
            plt.savefig(save_path) # And... curtain! Time to unveil the masterpiece

# Example usage:
extract_poster_colors(top_rated_movies, client)  # Dive into the colorful world of top-rated movie posters


#### d. Dive into a random trending movie trailer on YouTube!

import webbrowser  # Import webbrowser to open URLs in the default browser
import requests  # Import requests to handle HTTP requests
import random  # Import random to make random selections

# Fetch what's hot: Grab the trending movies from TMDB
def fetch_trending_movies(client, time_window='day'):
    """
    Fetch trending movies from TMDB based on the specified time window.

    Args:
        client (TMDBAPIClient): An instance of TMDBAPIClient to interact with TMDB API.
        time_window (str): The time window to fetch trending movies for. Default is 'day'.

    Returns:
        list: A list of dictionaries containing information about trending movies.
    """
    endpoint = f"{client.base_url}/trending/movie/{time_window}"  # Construct the API endpoint URL for trending movies
    params = {"api_key": client.api_key}  # Set up the parameters with the API key
    response = requests.get(endpoint, params=params)  # Send a GET request to the TMDB API
    response.raise_for_status()  # Raise an error if the request was unsuccessful
    return response.json()['results']  # Return the list of trending movies from the API response

# Ready for a surprise? Open a random trending movie trailer
def open_random_trending_trailer(client):
    """
    Open a random trending movie trailer on YouTube in the default web browser.

    Args:
        client (TMDBAPIClient): An instance of TMDBAPIClient to fetch trending movies.

    Returns:
        None
    """
    trending_movies = fetch_trending_movies(client)  # Fetch the latest buzz in movies
    if trending_movies:  # Check if there are any trending movies returned
        random_movie = random.choice(trending_movies)  # Randomly select one movie from the list
        movie_title = random_movie['title']  # Extract the movie's title
        print(f"Selected random trending movie: {movie_title}")  # Print the selected movie title
        print("Opening on YouTube... Sit back, relax, and enjoy the trailer!")  # Inform the user that the trailer is opening

        # Send you straight to the YouTube search results for this movie's trailer
        search_query = f"{movie_title} official trailer"  # Construct the search query for the movie trailer
        webbrowser.open(f"https://www.youtube.com/results?search_query={requests.utils.quote(search_query)}")  # Open YouTube search results in the browser
    else:  # If no trending movies are found
        print("No trending movies found. Maybe Hollywood's on a break?")  # Inform the user that no movies were found, sad :(!

# Example usage:
open_random_trending_trailer(client)  # Hit the button and let the randomness bring you a trending trailer!

#**********************************************************************************************************************************************#
#**********************************************************************************************************************************************#

# 5. Simple Unit-testing Data Imports – Catching those Inevitable Glitches during Data Importing

# Importing the necessary tools for testing – let's make sure everything works as intended.
import unittest

# Bringing in mocking capabilities – so we can simulate API interactions with precision.
from unittest.mock import patch, MagicMock

# Defining the test suite for TMDBAPIClient – time to put our code through its paces.
class TestTMDBAPIClient(unittest.TestCase):
    """
    Unit test suite for the TMDBAPIClient class.

    Methods:
        setUp: Initializes the TMDBAPIClient with a test API key.
        test_get_top_rated_movies: Tests the retrieval of top-rated movies.
        test_get_movie_details: Tests the retrieval of movie details by ID.
        test_search_movies: Tests the search functionality for movies.
        test_get_movies_by_genre: Tests the retrieval of movies filtered by genre.
    """

    # Setting up the test environment – initializing the API client with a test key.
    def setUp(self):
        """
        Set up the test environment by initializing the API client with a test key.
        """
        self.api_key = "test_api_key"
        self.client = TMDBAPIClient(self.api_key)

    # Testing the retrieval of top-rated movies – ensuring our client communicates properly with the API.
    @patch('requests.get')
    def test_get_top_rated_movies(self, mock_get):
        """
        Test the retrieval of top-rated movies from TMDB.
        Ensures the correct API endpoint is called and the expected data is returned.

        Args:
            mock_get (Mock): The mock object for requests.get.

        Returns:
            None
        """
        # Mocking the API response – setting up a controlled environment for our test.
        mock_response = MagicMock()
        mock_response.json.return_value = {'results': ['movie1', 'movie2']}
        mock_response.raise_for_status = MagicMock()  # Simulating a successful API call.
        mock_get.return_value = mock_response

        # Calling the method to fetch top-rated movies – using our mocked data.
        movies = self.client.get_top_rated_movies()

        # Verifying that the correct API endpoint was called with the right parameters.
        mock_get.assert_called_once_with(f"{self.client.base_url}/movie/top_rated", params={"api_key": self.api_key, "page": 1})
        # Asserting the returned data matches our expectations – quality control in action.
        self.assertEqual(movies, ['movie1', 'movie2'])

    # Testing the retrieval of movie details – ensuring accuracy and reliability in fetching data.
    @patch('requests.get')
    def test_get_movie_details(self, mock_get):
        """
        Test the retrieval of movie details by movie ID.
        Ensures the correct API endpoint is called and the expected data is returned.

        Args:
            mock_get (Mock): The mock object for requests.get.

        Returns:
            None
        """
        # Mocking the API response for movie details – keeping our tests isolated and predictable.
        mock_response = MagicMock()
        mock_response.json.return_value = {'title': 'Example Movie'}
        mock_response.raise_for_status = MagicMock()  # Simulating a flawless API interaction.
        mock_get.return_value = mock_response

        # Using a specific movie ID to test the details retrieval – focusing on precision.
        movie_id = 12345
        details = self.client.get_movie_details(movie_id)

        # Confirming the correct API endpoint was accessed with the appropriate parameters.
        mock_get.assert_called_once_with(f"{self.client.base_url}/movie/{movie_id}", params={"api_key": self.api_key})
        # Ensuring the data returned is exactly what we expected – maintaining high standards.
        self.assertEqual(details, {'title': 'Example Movie'})

    # Testing the search functionality – verifying that queries yield accurate results.
    @patch('requests.get')
    def test_search_movies(self, mock_get):
        """
        Test the search functionality for movies based on a query.
        Ensures the correct API endpoint is called and the expected data is returned.

        Args:
            mock_get (Mock): The mock object for requests.get.

        Returns:
            None
        """
        # Mocking the API response for a movie search – setting the stage for a focused test.
        mock_response = MagicMock()
        mock_response.json.return_value = {'results': ['movie1', 'movie2']}
        mock_response.raise_for_status = MagicMock()  # Simulating an error-free API response.
        mock_get.return_value = mock_response

        # Executing a search query – testing the client’s ability to handle user input.
        query = "Inception"
        results = self.client.search_movies(query)

        # Verifying that the search API endpoint was called correctly with the proper query.
        mock_get.assert_called_once_with(f"{self.client.base_url}/search/movie", params={"api_key": self.api_key, "query": query, "page": 1})
        # Checking that the search results are as expected – ensuring reliability in search operations.
        self.assertEqual(results, ['movie1', 'movie2'])

    # Testing movie retrieval by genre – making sure our client can filter results efficiently.
    @patch('requests.get')
    def test_get_movies_by_genre(self, mock_get):
        """
        Test the retrieval of movies filtered by genre.
        Ensures the correct API endpoint is called and the expected data is returned.

        Args:
            mock_get (Mock): The mock object for requests.get.

        Returns:
            None
        """
        # Mocking the API response for genre-specific movies – keeping our tests focused and precise.
        mock_response = MagicMock()
        mock_response.json.return_value = {'results': ['movie1', 'movie2']}
        mock_response.raise_for_status = MagicMock()  # Simulating smooth API communication.
        mock_get.return_value = mock_response

        # Using a specific genre ID to fetch movies – testing genre-based filtering.
        genre_id = 28
        results = self.client.get_movies_by_genre(genre_id)

        # Confirming that the genre-specific API endpoint was accessed with the correct parameters.
        mock_get.assert_called_once_with(f"{self.client.base_url}/discover/movie", params={"api_key": self.api_key, "with_genres": genre_id, "page": 1})
        # Verifying that the returned movie list matches our expectations – ensuring dependable results.
        self.assertEqual(results, ['movie1', 'movie2'])

# Running the tests – time to validate our work!
unittest.main(argv=[''], exit=False)
