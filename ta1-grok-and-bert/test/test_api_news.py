import pandas as pd
import pytest
from workingDirectory.api_news import fetch_articles

@pytest.fixture
def getArticles():
    articles = fetch_articles()
    return articles

def test_fetch_articles(getArticles):
    assert len(getArticles) > 0, "Failed to fetch"