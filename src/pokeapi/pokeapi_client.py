import requests

class pokeAPI():
    def __init__(self, base_url='https://pokeapi.co/api/v2/'): #set base url for simple calling
        self.base_url = base_url

    """
    Retrieves the data of the specified pokemon from the PokeAPI.

    Args:
        pokemon: The pokemon whos data is desired
    """
    #we were originally going to retrive each pokemon to be compared but changed strategy. 
    #this function is no longer used.
    def get_data(self, pokemon): 
        url = f"{self.base_url}/pokemon/{pokemon.lower()}"
        response = requests.get(url)
        if response.status_code == 200: #ensure successful retrieval
            return response.json()
        else:
            response.raise_for_status()            

    """
    Error handling function.

    Args:
        e: The error which occured
    """
    def error_handling(self, e):
        print(f"An error occured retrieving the data: {e}")

    """
    This function extracts the relevant information from the Pokemon's json data and
        stores it in a list to be added to the csv file.

    Args:
        json: The json file containing the pokemon's data
    Return:
        simplified_data: A list containing the relevant data in the json file
    """
    def clean_data(self, json):
        #extrating the relevant pokemon information from the json 
        #and storing it in a list to be added to the csvg
        stats = {
            stat['stat']['name']: stat['base_stat']
            for stat in json['stats']
        }
        csv_row = [
                json['name'],  #name
                ', '.join([type['type']['name'] for type in json['types']]),  #types as a comma-separated string
                ', '.join([ability['ability']['name'] for ability in json['abilities']]),  #abilities as a comma-separated string
                json['sprites']['front_default'],  #sprite URL
                json['cries']['latest'],  #cry URL
                stats['hp'],  #hp
                stats['attack'],  #attack
                stats['defense'],  #defense
                stats['special-attack'],  #special Attack
                stats['special-defense'],  #special Defense
                stats['speed']  #speed
            ]
        #storing extracted data in list and returning to store in csv
        return csv_row
    
    """
    Retrieves the data of all original 151 pokemon from the PokeAPI.

    Args:
        csv: The csv file which to append each pokemons data too
    """
    def get_all_data(self, csv):
        i = 1
        #loops through the original 151 pokemon
        for i in range(1,152):
            url = f"{self.base_url}/pokemon/{i}" #the pokemons id can be a substitute for its name (1 = bulbasaur, 2 = ivysaur, etc.)
            response = requests.get(url)
            if response.status_code != 200: #if status does not indicate successful retrieval raise error
                response.raise_for_status() 
            pokemon_data = self.clean_data(response.json()) #send json to data cleaning function
            csv.append(pokemon_data)