# USAGE
# cd web_scraping_scrapy
# scrapy crawl QuoteScraper

# EXPORT RESULTS as a csv, xml or json
# scrapy crawl QuoteScraper -o results.csv 
# scrapy crawl QuoteScraper -o results.xml
# scrapy crawl QuoteScraper -o results.json

# Import necessary libraries and modules
import scrapy
from ..items import WebScrapingScrapyItem, AmazonScrapingScrapyItem

class ScrapeQuotesSpider(scrapy.Spider):
    # name of the spider to run for scraping the website
    name = "QuoteScraper"

    # list of websites to scrape
    start_urls = [
        "https://quotes.toscrape.com/"
    ]

    def parse(self, response):
        # instantiate the class to store scraped data in scrapy item containers for better organization
        items = WebScrapingScrapyItem()

        # inspect the webpage and extract `div.quote` tag from the source code captured in the response argument
        all_div_quotes = response.css("div.quote")

        # Iterate through each quote to extract the corresponding title, author and associated tags from the webpage
        for quote in all_div_quotes:
            title = quote.css("span.text::text").extract()
            author = quote.css(".author::text").extract()
            tag = quote.css(".tag::text").extract()

            items['titles'] = title
            items['authors'] = author
            items['tags'] = tag
            
            # yield items from the python generator as expected by scrapy
            yield items

class ScrapeAmazonSpider(scrapy.Spider):
    # name of the spider to run for scraping the website
    name = "AmazonScraper"

    # list of websites to scrape
    start_urls = [
        "https://www.amazon.com/s?k=women+fashion&crid=3B1XVPEQR4EUE&sprefix=women+fashion%2Caps%2C108&ref=nb_sb_noss_1"
    ]

    def parse(self, response):
        # instantiate the class to store scraped data in scrapy item containers for better organization
        items = AmazonScrapingScrapyItem()

        # inspect the webpage and extract relevant css tags from the source code captured in the response argument
        brands = response.css(".s-line-clamp-1 .a-color-base::text").extract()
        descriptions = response.css(".a-color-base.a-text-normal::text").extract()
        prices = response.css(".a-price-whole::text").extract()

        # Iterate through each quote to extract the corresponding title, author and associated tags from the webpage
        for brand, desc, price in zip(brands, descriptions, prices):

            items['brand'] = brand
            items['description'] = desc
            items['price'] = price
            
            # yield items from the python generator as expected by scrapy
            yield items