import json
import requests
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # HuggingFace API setup
        HF_TOKEN = "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"
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Accept": "application/json"
        }
        
        # Using the correct dataset API endpoint with fewer records
        dataset_name = "neuralwork/arxiver"
        api_url = f"https://datasets-server.huggingface.co/rows"
        params = {
            "dataset": dataset_name,
            "config": "default",
            "split": "train",
            "offset": 0,
            "length": 3  # Reduced to 3 papers to stay within size limit
        }
        
        logger.info(f"Fetching dataset: {dataset_name}")
        response = requests.get(api_url, headers=headers, params=params)
        
        response.raise_for_status()
        data = response.json()
        
        # Extract paper data with trimmed content
        papers = []
        for row in data.get('rows', []):
            row_data = row.get('row', {})
            # Trim long text fields
            abstract = row_data.get('abstract', '')[:500] if row_data.get('abstract') else ''
            markdown = row_data.get('markdown', '')[:1000] if row_data.get('markdown') else ''
            
            paper = {
                'id': row_data.get('paper_id', '')[:50],
                'title': row_data.get('title', '')[:200],
                'abstract': abstract,
                'authors': row_data.get('authors', [])[:5],  # Limit number of authors
                'publication_date': row_data.get('published', '')[:10],
                'url': f"https://arxiv.org/abs/{row_data.get('paper_id', '')}"[:100],
                'markdown_content': markdown
            }
            papers.append(paper)
        
        logger.info(f"Successfully processed {len(papers)} papers")
        
        # Log size of response for debugging
        response_size = len(json.dumps(papers))
        logger.info(f"Response size: {response_size} bytes")
        
        return {
            "statusCode": 200,
            "body": json.dumps(papers)
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        error_response = {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Failed to fetch data from Hugging Face API",
                "details": str(e)
            })
        }
        return error_response
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        error_response = {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Internal server error",
                "details": str(e)
            })
        }
        return error_response