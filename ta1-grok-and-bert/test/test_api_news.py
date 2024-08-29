import pandas as pd
import pytest
from workingDirectory.api_news import fetch_articles,convert_and_save_dataframe, preprocess_df, sentiment_analysis

@pytest.fixture
def getArticles():
    articles = fetch_articles()
    return articles

def test_fetch_articles(getArticles):
    assert len(getArticles) > 0, "Failed to fetch"

def test_createDF(getArticles):
    import os
    convert_and_save_dataframe(getArticles,"test/articles.csv")
    assert os.path.exists('test/articles.csv'), "Failed to create and save dataframe"


def test_preprocessDF(getArticles):
    import os
    df = convert_and_save_dataframe(getArticles,"test/articles.csv")
    df = preprocess_df(df,"test/preprocessed_articles.csv")
    assert os.path.exists('test/preprocessed_articles.csv'), "Failed to pre process and save dataframe"

def test_sentiment_analysis(getArticles):
    import os
    df = convert_and_save_dataframe(getArticles,"test/articles.csv")
    df = preprocess_df(df,"test/preprocessed_articles.csv")
    df = sentiment_analysis(df,"test/final_articles_with_sentiment.csv")
    assert os.path.exists('test/final_articles_with_sentiment.csv'), "Failed to pre process and save dataframe"

