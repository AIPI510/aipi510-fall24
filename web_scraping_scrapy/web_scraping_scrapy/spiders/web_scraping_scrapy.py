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

    def start_requests(self):
        # Start with page 1
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'page_number': 1})

    def parse(self, response):
        """
        Parse the HTML response from the start URL.

        This method extracts product titles and prices using CSS selectors, stores them in an HMScrapingScrapyItem object, and yields them as output.

        params:
            response : The HTTP response object containing the HTML content of the page to be parsed.
        """
        page_number = response.meta.get('page_number', 1)  # Retrieve the page number from meta

        # Inspect the webpage and extract relevant CSS tags from the source code captured in the response argument
        titles = response.css(".a04ae4::text").extract()
        prices = response.css(".b19650::text").extract()

        # Iterate through each product to extract the corresponding title and price from the webpage
        for title, price in zip(titles, prices):
            
             # Instantiate the class to store scraped data in scrapy item containers for better organization
            item = HMScrapingScrapyItem()  

            item['title'] = title.strip()
            item['price'] = price.strip()
            item['page_number'] = page_number

            yield item  # Yield the individual item

        # Since the source code is updated dynamically as one scrolls through the pages, we are currently extracting all pages available on the current screen as opposed to all pages available
        next_pages = response.css("ul.ed2eb5 li a.acae11::attr(href)").extract()

        # Remove duplicates to avoid revisiting the same page
        next_pages = list(set(next_pages))

        # Follow each page in the list
        for next_page in next_pages:
            if next_page:
                next_page_url = response.urljoin(next_page)  # Ensure URL is absolute

                yield scrapy.Request(
                    next_page_url,
                    callback=self.parse,
                    meta={'page_number': page_number + 1}  # Increment page number
                )
