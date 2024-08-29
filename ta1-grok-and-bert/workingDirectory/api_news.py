import os
import requests
from dotenv import load_dotenv
import pandas as pd
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def fetch_articles():
    # load env
    load_dotenv()
    # get apikey from env
    api_key = os.getenv('API_KEY')
    # base URL
    base_url = "https://newsapi.org/v2/everything"
    # init param
    params = {
        'q': 'artificial intelligence',
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
    # ensure the description column exists
    if 'description' in df.columns:
        df['description'] = df['description'].fillna('')
    else:
        df['description'] = ''

    # drop any rows that are completely empty if necessary
    df.dropna( inplace=True)

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

def main():
    articles = fetch_articles()
    df = convert_and_save_dataframe(articles, "articles.csv")
    df = preprocess_df(df, "preprocessed_articles.csv")
    df = sentiment_analysis(df, "final_articles_with_sentiment.csv")
    
    print(df.head())

if __name__ == "__main__":
    main()
