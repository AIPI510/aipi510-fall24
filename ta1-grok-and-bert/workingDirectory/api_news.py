import os
import requests
from dotenv import load_dotenv
import pandas as pd
import json

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
        print(type(articles))
        if articles:
            for i, article in enumerate(articles, start=1):
                print(f"Article {i}:")
                print(f"Title: {article['title']}")
                print(f"Description: {article['description']}")
                print(f"URL: {article['url']}\n")
                print(type({article['url']}))
        else:
            print("No articles found.")

    # handle type errors accordingly.
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

    

def convert_and_save_dataframe(articles):
    import pandas as pd
    df = pd.DataFrame(articles[1:], columns=articles[0])

    print(df.head())
    df.to_csv("articles.csv")
    return df

def preprocess_df(df):
    import pandas as pd
    print(df)
    #nan_rows = df[df.isna().any(axis=1)]
    df.dropna(inplace = True)

    nan_rows = df[df.isna().any(axis=1)]
    print(nan_rows)
    print(df)
    df.to_csv("preprocessed_articles.csv")


def main():
    articles = fetch_articles()
    df = convert_and_save_dataframe(articles)
    df = preprocess_df(df)
    print("Some code snippets were created using the help og the Grepper Google Chrome Extension")

if __name__ == "__main__":
    main()


