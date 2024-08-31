import requests
import pandas as pd
import json

def handling_data():
    
    data = requests.get("https://openlibrary.org/search/authors.json?q=j%20k%20rowling")
    data = data.json()

    with open('data.json','w') as file:
        json.dump(data,file,indent=4,sort_keys=True)

    
    

    

    

        
    

if __name__ == "__main__":
   handling_data()
    