"""
This script uses selenium to scrape the website www.allmusic.com containing information 
about new releases. It collects the information about the albums released in August 2024 and runs analysis on the data.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import textwrap

def set_up_chrome_driver():
    """
    Downloads and sets up the correct chrome driver for the designated computer

    Returns: 
    object: Webdriver for Chrome to be used to initiate the scraping
    """
    
    # Download the correct ChromeDriver
    chromeDriver = ChromeDriverManager().install()

    # Create an options for specifications on how to run the driver
    chromeOptions = Options()

    # Add an option for Chrome to run in the background instead of opening a physical window
    chromeOptions.add_argument("--headless=new")

    # return Chrome
    return webdriver.Chrome(service=Service(chromeDriver), options=chromeOptions)


def create_df(driver):
    """
    Performs webscraping on www.allmusic.com and creates a dataframe of newly released albums

    Parameters:
    driver (webdriver): the driver used to perform webscraping

    Returns: 
    object: The dataframe object to be used for processing and analysis
    """

    #link format for dates yy-month-day
    BASE_URL = "https://www.allmusic.com/newreleases/all/"

    #list of all the dates that will be scraped. Corresponds to the releases in August 2024
    august_release_dates = ["20240802","20240809", "20240816","20240823", "20240830"]

    #lists representing each column to be added to the created dataframe
    artists_list = []
    album_names_list = []
    labels_list = []
    genres_list = []
    ratings_list = []

    # Open the url to be scraped 
    for release_date in august_release_dates:
        driver.get(BASE_URL + release_date)

        #select the "Just Released" option from the dropdown in order to exclude any re-issued albums
        dropdown = driver.find_elements(By.ID, 'type-filter')
        select = Select(dropdown[0])
        select.select_by_value('NEW')

        #Get all the artists in the page
        artists = driver.find_elements(By.XPATH, "//td[@class='artist']")
        albums = driver.find_elements(By.XPATH, "//td[@class='album']")
        labels = driver.find_elements(By.XPATH, "//td[@class='label']")
        genres = driver.find_elements(By.XPATH, "//td[@class='genre']")
        ratings = driver.find_elements(By.XPATH, "//td[@class='rating']")

        #assign each value found from the website to the appropriate list
        for entry in range(len(artists)):
            artists_list.append(artists[entry].text)
            album_names_list.append(albums[entry].text)
            labels_list.append(labels[entry].text)
            genres_list.append(genres[entry].text)
            try:
                #convert the rating to an int if it's a text
                rating = float(ratings[entry].text)
            except ValueError:
                #convert the rating to a NaN value if the text is empty
                rating = np.nan
            
            ratings_list.append(rating)

    #created this list of tuples to comply with pandas documentation for creating a df
    data_tuples = list(zip(artists_list[1:], album_names_list[1:], labels_list[1:], genres_list[1:], ratings_list[1:]))

    #create base dataframe
    df = pd.DataFrame(data_tuples, columns=['Artist','Album', 'Label', 'Genre', 'Rating'])

    #return the dataframe
    return df

def create_and_show_bar_plot(column_name, plot_name, df):
    """
    creates and shows a bar graph given a column name, plot name, and the dataframe.
    The x-axis being the column name and y-axis number of albums released 

    Parameters:
    column_name (str): name of the column to include in the x-axis
    plot_name (str): name of the plot to be displayed
    df (object): dataframe object from which the plot will be created
    """
    #get the top 10 most common genres
    top_genres = df[column_name].value_counts().nlargest(10)

    #create the bar plot
    top_genres.plot(kind='bar')

    #set a label for the x and y axes and a title
    plt.xlabel(column_name, labelpad=20)
    plt.ylabel("# of Albums", labelpad=20)
    plt.title(plot_name)

    #get the current axis
    ax = plt.gca()

    #make the x-axis labels horizontal for easier readability and apply a textwrap so labels don't overlap
    ax.set_xticklabels([textwrap.fill(label, 15) for label in top_genres.index], rotation=0)

    # Adjust layout to prevent clipping
    plt.tight_layout()

    #show the plot
    plt.show()

def drop_duplicates(df):
    """
    drops any duplicate rows from the dataframe. Duplicates here indicate rows that have 
    the same value for Artist and Album

    Parameters:
    df (object): the dataframe with duplicated rows

    Returns:
    object: dataframe object with no duplicated rows
    """
    return df.drop_duplicates(subset=['Artist', 'Album'])

def drop_rows_with_no_rating(df):
    """
    Drop rows that don't have a 'Rating' value or a NaN value

    Parameters:
    df (object): the dataframe with empty cells or NaN cells in the 'Rating' column

    Returns:
    object: dataframe object with values in every cell of the 'Rating' column
    """
    temp_df = df.drop(df[df["Rating"]==''].index) 
    return temp_df.dropna(subset=['Rating'])

def drop_rows_with_no_artist_name(df):
    """
    Drop rows with empty "Artist" cell

    Parameters:
    df (object): the dataframe with empty cells in the 'Artist' column

    Returns:
    object: dataframe object with values in every cell of the 'Artist' column
    """
    return df.dropna(subset=['Artist']) 

def fill_empty_label_column(df):
    """
    Fill any empty cells in the 'Label' column with 'Other'

    Parameters:
    df (object): the dataframe with empty cells in the 'Label' column

    Returns:
    object: dataframe object with values in every cell of the 'Label' column
    """
    df.loc[:, 'Label'] = df['Label'].fillna('Other')
    df.loc[:, 'Label'] = df['Label'].replace('', 'Other')
    return df

def drop_no_rating_or_artist(df):
    """
    This function cleans the dataset by dropping any rows without an artist name, 
    or rating.

    Parameters: 
    df (Dataframe object): the dataframe to be cleaned

    Returns:
    object: The cleaned dataframe

    """
    temp_df = drop_rows_with_no_rating(df)
    return drop_rows_with_no_artist_name(temp_df)

def save_top_albums(df, num_rankings):
    """
    This function gets the top albums and saves them to an excel file named 'top_albums.xlsx'

    Parameters: 
    df (Dataframe object): the dataframe to be cleaned
    num_rankings (int): the number of albums to be saved to the excel file
    """
    #create the album recommendations for August (top 20 albums)
    top_albums = df.nlargest(num_rankings, 'Rating')

    #Prepend a column that shows the ranking of each album
    top_albums.insert(0, "Ranking", list(range(1, num_rankings+1)))

    #save the ranked albums to an excel file
    top_albums.to_excel('top_albums.xlsx',index=False)

def main():
    # get and start chrome driver
    driver = set_up_chrome_driver()

    # scrape the website and create the dataframe
    df = create_df(driver)

    # quit Chrome since we are done scraping
    driver.quit()

    #drop duplicate rows
    df_no_dups = drop_duplicates(df)
    
    #Fill in the empty label column before making the bar plot to avoid missing values in the x-axis
    df_cleaned = fill_empty_label_column(df_no_dups)

    # Create and show plot of album releases by genre
    create_and_show_bar_plot('Genre', 'Album Releases By Genre August 2024', df_cleaned)

    # Create and show plot of number of album releases by record labels
    create_and_show_bar_plot('Label', 'Album Releases By Record Labels August 2024', df_cleaned)

    #drop rows that don't have a rating or an artist name to generate album recommendations
    df_cleaned = drop_no_rating_or_artist(df_cleaned)

    #save the top 20 albums to an excel file
    save_top_albums(df_cleaned, 20)
    
#ensure main is only run when the script is executed directly
if __name__ == "__main__":
    main()