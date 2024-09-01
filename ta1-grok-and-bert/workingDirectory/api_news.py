# 1. https://newsapi.org/register

# 2. Enter personal information

# 3. Retrieve key and insert into into #"Enter API KEY" String inside the news_api.py file located on line _____

# 4. create a virtual environment 

# Step 1 - clone the github repo -  git clone 
# Step 2 - navigate to your directory
# Step 3 - python -m venv venv
# Step 4 - source venv/bin/activate

# 5. Install the following python packages via PIP -
# pip install pip install annotated-types==0.7.0 anyio==4.4.0 beautifulsoup4==4.12.3 boto3==1.34.149 botocore==1.34.149 bs4==0.0.2 certifi==2024.7.4 charset-normalizer==3.3.2 click==8.1.7 distro==1.9.0 filelock==3.15.4 frozendict==2.4.4 fsspec==2024.6.1 h11==0.14.0 html5lib==1.1 httpcore==1.0.5 httpx==0.27.0 huggingface-hub==0.24.5 idna==3.7 iniconfig==2.0.0 Jinja2==3.1.4 jmespath==1.0.1 joblib==1.4.2 lxml==5.2.2 MarkupSafe==2.1.5 mpmath==1.3.0 multitasking==0.0.11 networkx==3.3 nltk==3.9.1 numpy==2.0.1 openai==1.37.1 packaging==24.1 pandas==2.2.2 peewee==3.17.6 platformdirs==4.2.2 plotly==5.24.0 pluggy==1.5.0 pydantic==2.8.2 pydantic_core==2.20.1 pytest==8.3.2 python-dateutil==2.9.0.post0 python-dotenv==1.0.1 pytz==2024.1 PyYAML==6.0.2 regex==2024.7.24 requests==2.32.3 s3transfer==0.10.2 safetensors==0.4.4 sec-api==1.0.18 sentencepiece==0.2.0 setuptools==72.1.0 six==1.16.0 sniffio==1.3.1 soupsieve==2.5 sympy==1.13.1 tenacity==9.0.0 tokenizers==0.19.1 torch==2.4.0 tqdm==4.66.4 transformers==4.44.0 typing_extensions==4.12.2 tzdata==2024.1 urllib3==2.2.2 webencodings==0.5.1 yfinance==0.2.41



def download_nltk():
    """
    Function to fetch articles from the news_api.py
    Input - a call from the main function
    Output - The NLTK vader lexicon is downloaded
    """
    import ssl
    import nltk

    # Bypass SSL certificate verification
    ssl._create_default_https_context = ssl._create_unverified_context

    # Download the VADER lexicon
    nltk.download('vader_lexicon')
    return

def fetch_articles():
    """
    Function to fetch articles from the news_api.py
    Input - a call from the main function
    Output - the data from the API in a list format
    """
    import os
    from dotenv import load_dotenv
    import requests

    # load env
    load_dotenv()
    # get apikey from env
    # TODO: Paste API key from https://newsapi.org/register
    api_key = os.getenv('API_KEY') #Enter your api key here
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
            for i, article in enumerate(articles, start=0):
                if (i < 6):
                    print(f"Article {i}:")
                    print(f"Title: {article['title']}")
                    print(f"Description: {article['description']}")
                    print(f"URL: {article['url']}\n")
                    print(f"Published At: {article['publishedAt']}\n")
                else:
                    break
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
    import pandas as pd
    df = pd.DataFrame(articles)
    print("Printing out all our data from the from the API in the dataframe format")
    print(df)
    df.to_csv(name)
    return df

def preprocess_df(df, name):
    """
    Function to preprocess the dataframe, and drop the NAN values
    Input - unprocessed dataframe, name of the csv to be saved as
    Output - Dropped values which have NAN type
    """
    import pandas as pd
    print("\n\n\n")
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
    """
     The following function is used to analyse the sentiment of the articles. It uses the NLTK toolkit followed by vader
     tool to compute the sentiment score given the description of each new article.

     Param: Preprocessed Dataframe

     Return: DataFrame with calculated sentiment scores.
    """
    import pandas as pd
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
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
    import pandas as pd
    import plotly.express as px
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
    download_nltk()
    articles = fetch_articles()
    df = convert_and_save_dataframe(articles, "articles.csv")
    df = preprocess_df(df, "preprocessed_articles.csv")
    df = sentiment_analysis(df, "final_articles_with_sentiment.csv")
    plot_sentiment(df)
    print(df.head())

if __name__ == "__main__":
    main()
