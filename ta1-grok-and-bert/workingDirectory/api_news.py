import os
import requests
from dotenv import load_dotenv
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import plotly.express as px


def fetch_articles():
    """
    Function to fetch articles from the news_api.py
    Input - a call from the main function
    Output - the data from the API in a list format
    """
    # load env
    load_dotenv()
    # get apikey from env
    api_key = os.getenv('API_KEY')
    # base URL
    base_url = "https://newsapi.org/v2/everything"
    # init param
    params = {
        'q': 'Artificial Intelligence' ,
        'apiKey': api_key,
        'language': 'en',
        'sortBy': 'relevancy'
    }

    try:
        # get request
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        # read json
        articles = response.json().get('articles', [])
        if articles:
            for i, article in enumerate(articles, start=1):
                print(f"Article {i}:")
                print(f"Title: {article['title']}")
                print(f"Description: {article['description']}")
                print(f"URL: {article['url']}\n")
                print(f"Published At: {article['publishedAt']}\n")
        else:
            print("No articles found.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return articles

def convert_and_save_dataframe(articles, name):
    """
    Function to convert the data from the api and return it in the dataframe format
    Input - all the data in the list format, name of the csv to be saved as
    Output - the data data in dataframe format
    """
    df = pd.DataFrame(articles)
    print("Printing out all our data from the from the API in the dataframe format")
    print(df.head())
    df.to_csv(name)
    return df

def preprocess_df(df, name):
    """
    Function to preprocess the dataframe, and drop the NAN values
    Input - unprocessed dataframe, name of the csv to be saved as
    Output - Dropped values which have NAN type
    """
    # ensure the description and date column exists
    if 'description' in df.columns:
        df['description'] = df['description'].fillna('')
    else:
        df['description'] = ''
    if 'publishedAt' in df.columns:
        df['publishedAt'] = pd.to_datetime(df['publishedAt']).fillna('')
    else:
        df['publishedAt'] = ''
    # drop any rows that are completely empty if necessary
    df.dropna( inplace=True)
    print("Printing out all our data from the dataframe after pre processing and removing NAN values")
    print(df)
    df.to_csv(name)
    return df


def sentiment_analysis(df, name):
    # init vader
    sia = SentimentIntensityAnalyzer()

    # compute sentiment score
    def get_sentiment_score(description):
        if description:
            score = sia.polarity_scores(description)['compound']
            return score
        else:
            return 0

    # apply sentiment score to each description
    df['sentiment_score'] = df['description'].apply(get_sentiment_score)
    df.to_csv(name)
    return df


def plot_sentiment(df):
    # handle publishAt class to conversion to dateTime
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])

    # create plot and add "hoverable" elements
    fig = px.scatter(
        df,
        x='publishedAt',
        y='sentiment_score',
        hover_name='title',
        hover_data={'url': True},
        labels={
            'publishedAt': 'Published Date',
            'sentiment_score': 'Sentiment Score'
        },
        title='Sentiment Analysis of AI Articles Over Time'
    )

    fig.show()


def main():
    articles = fetch_articles()
    df = convert_and_save_dataframe(articles, "articles.csv")
    df = preprocess_df(df, "preprocessed_articles.csv")
    df = sentiment_analysis(df, "final_articles_with_sentiment.csv")
    plot_sentiment(df)
    print(df.head())

if __name__ == "__main__":
    main()
