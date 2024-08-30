# Import necessary modules
import pytest
from web_scraping_scrapy.spiders.web_scraping_scrapy import ScrapeHMSpider
import pandas as pd

@pytest.fixture
def spider():
    return ScrapeHMSpider()

def test_parse(spider):
    # read the results file generated
    df_results = pd.read_json(r"web_scraping_scrapy/results.json")

    # Assert that the correct columns are present
    assert "title" in df_results.columns
    assert "price" in df_results.columns

    # Assert that there is at least one item scraped
    assert len(df_results) >= 1

    # Check specific values if you know what to expect
    assert df_results.iloc[0]["title"] == "Knit Bodycon Dress"
    assert df_results.iloc[0]["price"] == "$ 49.99"


