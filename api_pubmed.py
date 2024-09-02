'''
References used for development:
* https://ualibweb.github.io/UALIB_ScholarlyAPI_Cookbook/src/python/pubmed.html
* https://www.ncbi.nlm.nih.gov/books/NBK25500/
* https://www.ncbi.nlm.nih.gov/books/NBK25497/
* https://stackoverflow.com/questions/54783160/x-axis-tick-labels-are-too-dense-when-drawing-plots
'''

from time import sleep
from argparse import ArgumentParser
import requests
import pandas as pd
import matplotlib.pyplot as plt
import math

class PubMed:
    '''
    References Used:
    * https://ualibweb.github.io/UALIB_ScholarlyAPI_Cookbook/src/python/pubmed.html
    * https://www.ncbi.nlm.nih.gov/books/NBK25500/
    '''
    
    # Base URL for querying the PubMed API
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'

    def query(self, term):
        return requests.get(f'{self.base_url}/esearch.fcgi?db=pubmed&term={term}&retmode=json').json()

pubmed = PubMed()

def get_args():
    '''
    Constructs an ArgumentParser with the supported arguments for this script.
    '''
    parser = ArgumentParser(
        prog='api_pubmed',
        description='Scatter plots number of articles about specific diseases from PubMed over time.')
    parser.add_argument('--disease', dest='disease', default='polio', help='Disease/topic to be analyzed for research interest (default: polio)')
    parser.add_argument('--start', dest='start', default='1954', help='Start year (inclusive) (default: 1954)')
    parser.add_argument('--end', dest='end', default='1961', help='End year (exclusive) (default: 1961)')
    return parser.parse_args() 

def construct_term(year, month, disease):
    '''
    Constructs the search term for the PubMed search API.

    Parameters:
        year (int) - year of the month's worth of articles we're fetching.
        month (int) - month number of the month's worth of articles we're fetching.
        disease (str) - disease that should be mentioned in the article title or abstract.
    '''
    return f'%28%28"{year}%2F{month}%2F01"%5BDate+-+Publication%5D+%3A+"{year if month < 12 else year + 1}%2F{month + 1 % 12}%2F01"%5BDate+-+Publication%5D%29%29+AND+%28{disease}%5BTitle%2FAbstract%5D%29'


def create_dataframe(data):
    '''
    Creating dataframe of scraped PubMed data for visualization
    '''
    return pd.DataFrame(data)


class DataAggregator:
    '''
    Takes in raw data from PubMed api query and aggregates data in dictionary
    Creates constructor for data with columns year & month, count, and disease. 
    '''
    def __init__(self):
      
        self.year_month=[]
        self.count=[]

    def add_raw_data(self,rawdata,year,month):
        '''
        Rawdata is aggregated into columns: year & month, count, and disease. 
        '''
        self.count.append(int(rawdata["esearchresult"]["count"]))  
        self.year_month.append(str(year) + "/" + str(month))

    def build_data_dictionary(self):
        '''
        Data is passed into a dictionary. 
        '''
        return {"year_month":self.year_month, "count": self.count}

data_aggregator = DataAggregator()

def main():
    '''
    Entry-point for the script.
    '''
    args = get_args()
    disease = args.disease
    for year in range(int(args.start), int(args.end)):
        for month in range(1, 13):
            print(f'Sourcing data for year {year}, month {month}...')
            rawdata=pubmed.query(construct_term(year, month, disease))
            data_aggregator.add_raw_data(rawdata, year, month)
            # Maximum of 3 requests per second without an API key:
            # https://www.ncbi.nlm.nih.gov/books/NBK25497/
            sleep(0.34)

    data_dictionary = data_aggregator.build_data_dictionary()
    df = create_dataframe(data_dictionary)
    print(df.head())

    df.plot.bar(x = 'year_month', y = 'count')

    # How to set spacing of labels/ticks
    # https://stackoverflow.com/questions/54783160/x-axis-tick-labels-are-too-dense-when-drawing-plots
    skip = math.ceil(len(df) / 12)
    ax = plt.gca()
    ax.set_xticks(ax.get_xticks()[::skip])

    plt.show()

if __name__ == '__main__':
    main()
