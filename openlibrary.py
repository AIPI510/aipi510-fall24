
# Import Necessary Libraries 
import requests



# Function That Uses Author Name And Returns The Corresponding Author ID 
def get_author_id(author_name):
    
    search_url = "https://openlibrary.org/search/authors.json" 
    search_param = {'q': author_name} 
    response = requests.get(search_url, params=search_param) 
    search_data = response.json() 
    author_id = search_data['docs'][0]['key'] 

    return author_id


# Function That Uses Author ID And Returns A List Of Works By The Corresponding Author 
def get_author_works(author_id):
    
    works_url = f"https://openlibrary.org/authors/{author_id}/works.json" 
    response = requests.get(works_url) 
    works_data = response.json()      
    works = works_data.get('entries', []) 
    work_titles = [work['title'] for work in works] 

    return work_titles


# Main Function That Uses Author Name From Input And Prints List of Works By That Author
def main(author_name):

    author_id = get_author_id(author_name) 
    works = get_author_works(author_id) 
    
    print(f"Works by {author_name}:")
    for number, title in enumerate(works, start=1):
        print(f"{number}. {title}")
        if number == 10:
            break



# Main Entry Point Of The Script 
if __name__ == '__main__':
    
    author_name = input('Enter Author Name: ')
    main(author_name)
