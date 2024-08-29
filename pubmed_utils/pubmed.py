'''
References Used:
* https://ualibweb.github.io/UALIB_ScholarlyAPI_Cookbook/src/python/pubmed.html
* https://www.ncbi.nlm.nih.gov/books/NBK25500/
'''

import requests

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
