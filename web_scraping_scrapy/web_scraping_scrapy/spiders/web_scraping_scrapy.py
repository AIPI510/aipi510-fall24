# USAGE
# cd web_scraping_scrapy
# scrapy crawl HMScraper

# EXPORT RESULTS as a csv, xml or json
# scrapy crawl HMScraper -o results.csv 
# scrapy crawl HMScraper -o results.xml
# scrapy crawl HMScraper -o results.json

# Import necessary libraries and modules
import scrapy
from ..items import HMScrapingScrapyItem

class ScrapeHMSpider(scrapy.Spider):
    """
    A Scrapy Spider to scrape product titles and prices from the H&M dresses page.
    """
    
    # Name of the spider to run for scraping the website
    name = "HMScraper"

    # List of websites to scrape
    start_urls = [
        "https://www2.hm.com/en_us/women/products/dresses.html"
    ]

    def parse(self, response):
        """
        Parse the HTML response from the start URL.

        This method extracts product titles and prices using CSS selectors, stores them in an HMScrapingScrapyItem object, and yields them as output.

        params:
            response : The HTTP response object containing the HTML content of the page to be parsed.
        """
        
        # Instantiate the class to store scraped data in scrapy item containers for better organization
        items = HMScrapingScrapyItem()

        # Inspect the webpage and extract relevant CSS tags from the source code captured in the response argument
        titles = response.css(".a04ae4::text").extract()
        prices = response.css(".b19650::text").extract()

        # Iterate through each product to extract the corresponding title and price from the webpage
        for title, price in zip(titles, prices):

            items['title'] = title
            items['price'] = price
            
            # Yield items from the Python generator as expected by Scrapy
            yield items
