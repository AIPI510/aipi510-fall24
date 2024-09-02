# Team Assignment #1
## Data Sourcing

### Tejas Jyothi
### Hung Yin Chen

# aipi510-fall24-team-assignment1
## Features
- Search for an artist by name.
- Fetch and display the artist's details including followers and genres.
- Retrieve all albums and tracks of the artist.
- Display the popularity score of each track and calculate average popularity score of each album.
- Identify and display the top 5 most popular tracks of the artist.
- Plot a graph showing the average popularity of each album by release year.

## Set up
1. **Clone the Repository**:
     ```bash
     git clone https://github.com/KelllyChen/aipi510-fall24-team-assignment1.git
     cd aipi510-fall24-team-assignment1
     ```
2. **Create a Virtual Environment** (optional but recommended):
   - Create and activate a virtual environment to manage dependencies:
     ```bash
     pip install virtualenv
     virtualenv .venv
     activate .venv
     ```
3. **Install Dependencies**:
   - Install the required Python libraries using the `requirements.txt` file:

     ```bash
     pip install -r requirements.txt
     ```
4. **Get Spotify API Credentials**:
   - Register your application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) to obtain your `client_id` and `client_secret`.

5. **Update Credentials**:
   - Replace the placeholders in the script with your Spotify API `client_id` and `client_secret`:

     ```python
     client_id = 'YOUR_CLIENT_ID'
     client_secret = 'YOUR_CLIENT_SECRET'
     ```
## Usage

1. **Run the Script**:
   - Execute the script using Python:

     ```bash
     python web-scraping-spotify.py
     ```
2. **Input**:
   - When prompted, enter the name of the artist you want to analyze.
3. **Output**:
   - The script will display the artist's details(including number of followers and genres), each album name, release dates, popularity score of each song, and average popularity score of each album.
   - It will also print the top 5 most popular songs.
   - A plot will be shown, visualizing the average popularity of each album by release year.



