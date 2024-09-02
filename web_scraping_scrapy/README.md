# Web Scraping with Scrapy
## H&M Dresses Scraper

This repository contains a Scrapy spider designed to crawl the first 6 pages of H&M's dresses section and extract the name and price of each item. The output is saved in a json file. 

### Prerequisites

All the required libraries are listed in the file requirements.txt .

```
pip install -r requirements.txt
```

### Usage

The spider navigates the first initial url: www.hm.com/dresses and retrives the name and price of each dress. Then it iterates through the next 5 pages automatically.

To run the spider and scrape the data:

```
cd web_scraping_scrapy
scrapy crawl HMScraper -o results.json
```

This command will execute the spider and store the extracted data (name and price of each dress with the page number it was extarcted from) in a JSON file named results.json.

