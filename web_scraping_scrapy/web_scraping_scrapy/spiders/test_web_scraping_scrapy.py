# Import necessary modules
import pytest
from web_scraping_scrapy.spiders.web_scraping_scrapy import ScrapeQuotesSpider
from scrapy.http import HtmlResponse, Request

def generate_fake_response(url, body):
    "Method to simulate a fake HTTP response to test scrapy functionality"
    request = Request(url)
    response = HtmlResponse(url=url, request=request, body=body, encoding = 'utf-8')

    return response

@pytest.fixture
def spider():
    return ScrapeQuotesSpider()

def test_parse(spider):

    # Copied an element from the source code of the original website for testing
    html_content = """<div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">"The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking."</span>
        <span>by <small class="author" itemprop="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="change,deep-thoughts,thinking,world"> 
            
            <a class="tag" href="/tag/change/page/1/">change</a>
            
            <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
            
            <a class="tag" href="/tag/thinking/page/1/">thinking</a>
            
            <a class="tag" href="/tag/world/page/1/">world</a>
            
        </div>
    </div>"""

    response = generate_fake_response(url="https://quotes.toscrape.com/", body=html_content)

    # Run the spiders parse method and convert to a list of dictionaries 
    results = list(spider.parse(response))

    # Assert results
    assert len(results) == 1
    assert results[0]['titles'] == ['"The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking."']
    assert results[0]['authors'] == ['Albert Einstein']
    assert results[0]['tags'] == ['change', 'deep-thoughts', 'thinking', 'world']


