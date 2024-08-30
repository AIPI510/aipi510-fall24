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
    # name of the spider to run for scraping the website
    name = "HMScraper"

    # list of websites to scrape
    start_urls = [
        "https://www2.hm.com/en_us/women/products/dresses.html"
    ]

    def parse(self, response):
        # instantiate the class to store scraped data in scrapy item containers for better organization
        items = HMScrapingScrapyItem()

        # inspect the webpage and extract relevant css tags from the source code captured in the response argument
        titles = response.css(".a04ae4::text").extract()
        prices = response.css(".b19650::text").extract()

        # Iterate through each quote to extract the corresponding title, author and associated tags from the webpage
        for title, price in zip(titles, prices):

            items['title'] = title
            items['price'] = price
            
            # yield items from the python generator as expected by scrapy
            yield items