import sys
import os
import json
import requests
import argparse

def get_subject(endpoint, kwargs):
    """
    fetches the bill's subject from the given endpoint

    Args:
        endpoint (str): the base endpoint for the bill
        kwargs (str): supplementary keyword arguments for the API call, should include the API key
    Returns:
        the name of the bill's subject, or None if it doesn't exist
    """
    subject = endpoint + '/subjects' + kwargs
    ## fetch subject
    res = requests.get(subject)
    dic = res.json()
    if 'policyArea' not in dic['subjects']: ## subject does not exist
        return None
    return dic['subjects']['policyArea']['name']

def get_text(endpoint, kwargs):
    """
    fetches the bill's PDF link and name from the given endpoint

    Args:
        endpoint (str): the base endpoint for the bill
        kwargs (str): supplementary keyword arguments for the API call, should include the API key
    Returns:
        the pdf link and name of the given bill, if they exist. Otherwise, returns None.
    """

    text = endpoint + '/text' + kwargs
    ## fetch text content
    res = requests.get(text)
    dic = res.json()
    if dic['textVersions']:
        pdfNotFound = True 
        searchAt = 1
        ## request returns a list of dictionaries, loop from the back to find the latest version of the bill with a valid PDF link
        while pdfNotFound and searchAt < len(dic['textVersions']): 
            texts = dic['textVersions'][searchAt * -1]['formats']
            pdf_query = [text['url'] for text in texts if text['type'] == 'PDF']
            ## PDF link doesn't exist at current index, search the next index in our response
            if len(pdf_query) == 0: 
                searchAt += 1
            ## PDF link exists at current index, fetch the link and name
            else:
                pdf_link = pdf_query[-1]
                pdf_name = pdf_link.split('/')[-1]
                return pdf_link, pdf_name
        ## no PDF link found for the given bill
        return None, None
    ## no text exists
    else:
        return None, None
    
def main(args):
    """
    the main function that scrapes congress bills and downloads them to a local directory

    Args:
        args (dic): a dictionary of argumenets passed by our argparser
    """

    # Check if output directory exists
    if not os.path.exists(f'./{args.output_dir}'): 
        # Create if it doesn't exist 
        os.makedirs(f'./{args.output_dir}')
    offset, docs_added = 0, 0
    BASE = 'bill' 
    CONGRESS = args.congress ##specifies which congress we want to pull data from
    URL = 'https://api.congress.gov/v3' ##base URL
    kwargs = f'?format=json&api_key={args.api_key}' ##kwargs with the api key for authentication

    while docs_added < args.num_documents:
        myCurEndpoint = f"{URL}/{BASE}/{CONGRESS}?offset={offset}&format=json&api_key={args.api_key}"
        res = requests.get(myCurEndpoint)
        dic = res.json()
        if not dic['bills']: ## no more bills exist
            print(f'no more bills to add from the {CONGRESS}th congress')
            break
        else:
            curBillsList = dic['bills']
            ## for each bill currently fetched
            for bill in curBillsList:
                ## obtain the base endpoint for that specific bill
                billEndpoint = f"{URL}/{BASE}/{CONGRESS}/{bill['type'].lower()}/{bill['number']}"
                print(f'fetching from {billEndpoint}')
                ## get the subject of the bill
                subject = get_subject(billEndpoint, kwargs)
                ## only add bills with a specified subject 
                if not subject:
                    print('no subject found for this document. continuing to next')
                    continue
                ## fetch the pdf link and name of the bill
                pdf, name = get_text(billEndpoint, kwargs)
                if not pdf:
                    print('no pdf found for this bill. continuing to next')
                    continue
                print(f'SUCCESS! fetched {name} with the following metadata:')
                print(f'subject: {subject}')
                ## fetch the content of the PDF and download it to our output directory
                my_pdf = requests.get(pdf)
                with open(f"./{args.output_dir}/{name}", "wb") as file:
                    file.write(my_pdf.content)
                docs_added+=1 ## increment counter
                if docs_added == args.num_documents:
                    break
        offset += 20 ## increment offset (fetch the next 20 bills)

    print(f'done! scraped PDFs can be found in the folder {args.output_dir}')


if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--congress", type=str, default='118', help='specify which congress you want to scrape data from')
    parser.add_argument("--api_key", type=str, help='the congress API key')
    parser.add_argument("--num_documents", type=int, default=10, help='the number of PDFs you want to scrape')
    parser.add_argument("--output_dir", type=str, default='congress_bills', help='the output directory you want to store results in')
    args = parser.parse_args()
    main(args)

