from pubmed_utils.pubmed import PubMed
from pprint import pprint
import requests

'''
References Used:
* https://ualibweb.github.io/UALIB_ScholarlyAPI_Cookbook/src/python/pubmed.html
* https://www.ncbi.nlm.nih.gov/books/NBK25500/
'''
class PubMed:
    # Base URL for querying the PubMed API
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'

    def get_summary(self, id: str):
        '''
        Gets the summary for an article of a given id from the PubMed database.

        Parameters:
            id (string) - Unique identifier of an article in the PubMed database.
        '''
        return requests.get(f'{self.base_url}/esummary.fcgi?db=pubmed&id={id}&retmode=json').json()

pubmed = PubMed()

def example():
    '''
    An example of using PubMed's summary API in order to fetch an article summary,
    to verify connectivity to the API.
    '''
    pprint(pubmed.get_summary('27933103'))

def main():
    '''
    Entry-point for the script.
    '''
    example()

if __name__ == '__main__':
    main()
