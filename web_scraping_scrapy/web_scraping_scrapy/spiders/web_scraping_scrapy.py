# USAGE
# cd web_scraping_scrapy
# scrapy crawl QuoteScraper

# EXPORT RESULTS as a csv, xml or json
# scrapy crawl QuoteScraper -o results.csv 
# scrapy crawl QuoteScraper -o results.xml
# scrapy crawl QuoteScraper -o results.json

# Import necessary libraries and modules
import scrapy
from ..items import WebScrapingScrapyItem

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