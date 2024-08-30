from pubmed_utils.pubmed import PubMed
from pprint import pprint

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
