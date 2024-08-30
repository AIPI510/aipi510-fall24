# Import necessary modules
import pytest
from web_scraping_scrapy.spiders.web_scraping_scrapy import ScrapeHMSpider
import pandas as pd

@pytest.fixture
def spider():
    return ScrapeHMSpider()

def test_parse(spider):
    df_results = pd.read_json(r"web_scraping_scrapy/results.json")

    # Assert results
    assert "title" in df_results.columns
    assert "price" in df_results.columns
    assert len(df_results) >= 1


