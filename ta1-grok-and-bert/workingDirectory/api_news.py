import os
import requests
from dotenv import load_dotenv
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import plotly.express as px


def fetch_articles():
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
    df = pd.DataFrame(articles)
    print(df.head())
    df.to_csv(name)
    return df

def preprocess_df(df, name):
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

    print(df)
    df.to_csv(name)
    return df


def sentiment_analysis(df, name):
    """
     The following function is used to analyse the sentiment of the articles. It uses the NLTK toolkit followed by vader
     tool to compute the sentiment score given the description of each new article.

     Param: Preprocessed Dataframe

     Return: DataFrame with calculated sentiment scores.
    """
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
    """
     The following function takes in a df, specifically one that contains preprocessed information containing a sentiment,
      publishedAt, url and title class to provide a high-level analysis through a scatter plot.

     Param: Preprocessed Dataframe with calculated sentiment scores.

     Return: Interactive Scatter Plot
    """
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
    """
    This is a function that handles the processes of each function, calling them synchronously through the run.
    """
    articles = fetch_articles()
    df = convert_and_save_dataframe(articles, "articles.csv")
    df = preprocess_df(df, "preprocessed_articles.csv")
    df = sentiment_analysis(df, "final_articles_with_sentiment.csv")
    plot_sentiment(df)
    print(df.head())

if __name__ == "__main__":
    main()
