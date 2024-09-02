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

api_key = "6b6862278df7f34cb5577fe79565d2d9"  # Your golden ticket to the TMDB API. Replace this with your own API key!
# Generate your own API key at https://developer.themoviedb.org/docs/getting-started


# Building the backbone for interacting with the TMDB API
class TMDBAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key  # Safeguarding your API key for all requests
        self.base_url = "https://api.themoviedb.org/3"  # The hub for all TMDB API endpoints
        self.image_base_url = "https://image.tmdb.org/t/p/w500"  # Where all the movie posters live

    # Fetching the top-rated movies from TMDB
  
    def get_top_rated_movies(self, page=1):
        endpoint = f"{self.base_url}/movie/top_rated"  # The specific endpoint for top-rated movies
        params = {"api_key": self.api_key, "page": page}  # Essential parameters: your API key and the desired page
        response = requests.get(endpoint, params=params)  # Sending the request to TMDB
        response.raise_for_status()  # Ensuring the request was successful
        top_rated_movies = response.json()['results']
    
        # Extracting only the required fields
        filtered_movies = [
        {
            "id": movie["id"],
            "title": movie["title"],
            # "overview": movie["overview"],
            "vote_average": movie["vote_average"],
           
        }
        for movie in top_rated_movies
    ]
    
        return filtered_movies  # Returning the filtered list of movies


    # Fetching detailed information about a specific movie
    def get_movie_details(self, movie_id):
        endpoint = f"{self.base_url}/movie/{movie_id}"  # The endpoint for movie details, keyed by movie ID
        params = {"api_key": self.api_key}  # Including the API key in the request
        response = requests.get(endpoint, params=params)  # Sending the request to TMDB
        response.raise_for_status()  # Making sure there are no errors in the response
    
        # Extracting only the specific fields 
        movie_data = response.json()
        filtered_data = {
        "id": movie_data.get("id"),
        "title": movie_data.get("title"),
        "overview": movie_data.get("overview"),
        "popularity": movie_data.get("popularity"),
        "release_date": movie_data.get("release_date"),
        "revenue": movie_data.get("revenue"),
        "runtime": movie_data.get("runtime"),
        "status": movie_data.get("status"),
        "vote_average": movie_data.get("vote_average"),
        "vote_count": movie_data.get("vote_count")
    }
    
        return filtered_data  # Returning only the filtered data

    def search_movies(self, query, page=1):
        endpoint = f"{self.base_url}/search/movie" # The endpoint for searching movies based on a query
        params = {"api_key": self.api_key, "query": query, "page": page} # Including the API key, search query, and page number
        response = requests.get(endpoint, params=params)  # Sending the request to TMDB
        response.raise_for_status() # Making sure there are no errors in the response
    
        results = response.json()['results']
        filtered_results = []  # Extracting only the specific fields 
        for movie in results:
            filtered_movie = {
            "id": movie.get("id"),
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date")
                 
        }
        filtered_results.append(filtered_movie)
    
        return filtered_results    # Return the list of filtered movie details

    # Fetching movies based on their genre
    def get_movies_by_genre(self, genre_id, page=1):
        endpoint = f"{self.base_url}/discover/movie"  # The endpoint for discovering movies by genre
        params = {"api_key": self.api_key, "with_genres": genre_id, "page": page}  # Parameters: API key, genre ID, and page number
        response = requests.get(endpoint, params=params)  # Sending the request to discover movies by genre
        response.raise_for_status()  # Ensuring the request is successful
    
        results = response.json()['results']  # Extracting the list of movies from the JSON response
    
        filtered_results = []  # Extarcting only specific fields
        for movie in results:
            filtered_movie = {
            "genre_ids": movie.get("genre_ids"),
            "title": movie.get("title"),
            "release_date": movie.get("release_date"),
            "popularity": movie.get("popularity"),
            "vote_average": movie.get("vote_average"),
            
        }
        filtered_results.append(filtered_movie)  # Add the filtered movie dictionary to the list
    
        return filtered_results  # Return the list of filtered movies


    # Fetching and displaying movie posters
    def get_movie_poster(self, poster_path, save_path=None):
        if poster_path:  # Ensuring that a poster path is provided
            image_url = f"{self.image_base_url}{poster_path}"  # Constructing the full URL for the movie poster
            response = requests.get(image_url)  # Requesting the image from TMDB
            image = Image.open(BytesIO(response.content))  # Opening the image data using PIL

            if save_path:  # If a save path is provided
                image.save(save_path)  # Save the poster locally
            else:
                image.show()  # Otherwise, display the poster

        else:
            print("No poster path provided.")  # Log a message if there's no poster path to work wit

if __name__ == "__main__":
    client = TMDBAPIClient(api_key="6b6862278df7f34cb5577fe79565d2d9")  # Initialize the TMDBAPIClient with your API key

    # Test the get_top_rated_movies function
    print("Fetching top-rated movies...")
    top_rated_movies = client.get_top_rated_movies(page=1)
    print(f"Top-rated movies (Page 1):\n{pd.DataFrame(top_rated_movies)}\n")

    # Test the get_movie_details function with the movie ID 
    if top_rated_movies:
        first_movie_id = top_rated_movies[0]['id']
        print(f"Fetching details for the movie with ID {first_movie_id}...")
        movie_details = client.get_movie_details(first_movie_id)
        print(f"Movie Details:\n{movie_details}\n")

    # Test the search_movies function
    search_query = "Inception" # Example Search Query
    print(f"Searching for movies with the keyword '{search_query}'...")
    search_results = client.search_movies(query=search_query, page=1)
    print(f"Search Results for '{search_query}':\n{pd.DataFrame(search_results)}\n")  # Display the results in a clean tabular format using pandas DataFrame

    # Test the get_movies_by_genre function

    genre_id = 80 # Example genre ID 
    all_movies = []
    for page_num in range(1, 4):  #   # Loop through the first few pages to gather more results
        movies_by_genre = client.get_movies_by_genre(genre_id, page=page_num)
        all_movies.extend(movies_by_genre)  # Add movies from each page to the list
    if all_movies:
        print(f"Found {len(all_movies)} movies in the genre.")
        movies_df = pd.DataFrame(all_movies)  # Display the results in a clean tabular format using pandas DataFrame
        print(f"Movies in the speciified genre:\n{movies_df}\n")
    else:
        print("No movies found for the specified genre.")

    # Test the get_movie_poster function

    poster_path = "/xRWht48C2V8XNfzvPehyClOvDni.jpg"  # Example poster path
    client.get_movie_poster(poster_path) # Display the poster
    client.get_movie_poster(poster_path, save_path="movie_poster.jpg")# Save the poster to a local file
