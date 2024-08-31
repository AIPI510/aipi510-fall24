
import requests

def get_author_works(author_id):
    url = f"https://openlibrary.org/authors/{author_id}/works.json"
    
    response = requests.get(url)    
    data = response.json()        
    works = data.get('entries', [])
        
    return [work['title'] for work in works]

def get_author_id(author_name):
    url = "https://openlibrary.org/search/authors.json"
    
    params = {
        'q': author_name
    }
    
    response = requests.get(url, params=params)
    data = response.json()    
    author_id = data['docs'][0]['key']

    return author_id
    

# Example checked JK Jowling, Jane Austin, David Gerard, 

author_name = "Nancy Pearl"

works = get_author_works(get_author_id(author_name))

print(f"Works by {author_name}:")
for i, w in enumerate(works, start=1):
    print(f"{i}. {w}")
