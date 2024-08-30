import requests
import pandas as pd

def main():
    
    data = requests.get("https://openlibrary.org/search.json?q=the+lord+of+the+rings").text
    
    
    
    
    file = open('data.json', 'w')
    file.write(data)

    data2 = pd.read_json('data.json')
    dataframe = pd.DataFrame(data2)
    return(dataframe)
        
    

if __name__ == "__main__":
    main()
    