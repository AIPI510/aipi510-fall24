import sys
import os
import json
import requests
import argparse

def get_latest_action(endpoint, kwargs):
    action = endpoint + '/actions' + kwargs
    res = requests.get(action)
    dic = res.json()
    if len(dic['actions']) == 0:
        ## no recent actions recorded...
        return None
    if dic['actions'][0]['type'] in ['BecameLaw', 'Veto', 'Floor']:
        return dic['actions'][0]['text']
    return None

def get_subject(endpoint, kwargs):
    subject = endpoint + '/subjects' + kwargs
    res = requests.get(subject)
    dic = res.json()
    if 'policyArea' not in dic['subjects']: ##error handling, subject does not exist
        return None
    return dic['subjects']['policyArea']['name']
   
def get_title(endpoint, kwargs):
    title = endpoint + '/titles' + kwargs
    res = requests.get(title)
    dic = res.json()


def get_text(endpoint, kwargs):
    text = endpoint + '/text' + kwargs
    res = requests.get(text)
    dic = res.json()
    if dic['textVersions']:
        pdfNotFound = True 
        searchAt = 1
        while pdfNotFound and searchAt < len(dic['textVersions']): 
            texts = dic['textVersions'][searchAt * -1]['formats']
            pdf_query = [text['url'] for text in texts if text['type'] == 'PDF']
            if len(pdf_query) == 0: 
                searchAt += 1
            else:
                pdf_link = pdf_query[-1]
                pdf_name = pdf_link.split('/')[-1]
                return pdf_link, pdf_name
        return None, None
    else:
        return None, None
    
def main(args):
    # Check if directory exists
    if not os.path.exists(f'./{args.output_dir}'): 
        # Create the directory 
        os.makedirs(f'./{args.output_dir}')
    offset = 0
    docs_added = 0
    BASE = 'bill'
    CONGRESS = args.congress
    URL = 'https://api.congress.gov/v3'
    kwargs = f'?format=json&api_key={args.api_key}'

    while docs_added < args.num_documents:
        myCurEndpoint = f"{URL}/{BASE}/{CONGRESS}?offset={offset}&format=json&api_key={args.api_key}"
        res = requests.get(myCurEndpoint)
        dic = res.json()
        if not dic['bills']: ## no more bills exist
            break
        else:
            curBillsList = dic['bills']
            for bill in curBillsList:
                billEndpoint = f"{URL}/{BASE}/{CONGRESS}/{bill['type'].lower()}/{bill['number']}"
                print(f'fetching from {billEndpoint}')
                latestAction = get_latest_action(billEndpoint, kwargs)
                if not latestAction:
                    print('no previous action on this bill, contiuing to next')
                    continue
                subject = get_subject(billEndpoint, kwargs)
                if not subject:
                    print('no subject found for this document. continuing to next')
                    continue
                pdf, name = get_text(billEndpoint, kwargs)
                if not pdf:
                    print('no pdf found for this bill. continuing to next')
                    continue
                print(f'SUCCESS! fetched {name} with the following metadata:')
                print(f'subject: {subject}')
                print(f'latest action: {latestAction}')
                my_pdf = requests.get(pdf)
                with open(f"./{args.output_dir}/{name}", "wb") as file:
                    file.write(my_pdf.content)
                docs_added+=1
        offset += 20

    print('done!')


if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--congress", type=str, default='118', help='specify which congress you want to scrape data from')
    parser.add_argument("--api_key", type=str, help='the congress API key')
    parser.add_argument("--num_documents", type=int, default=100, help='the number of PDFs you want to scrape')
    parser.add_argument("--output_dir", type=str, default='congress_bills', help='the output directory you want to store results in')
    args = parser.parse_args()
    main(args)

