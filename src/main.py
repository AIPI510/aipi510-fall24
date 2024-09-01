import requests
import csv
from pokeapi.pokeapi_client import pokeAPI


def fetch():
    #initialize client
    api_client = pokeAPI()

    try:
        print("Extracting Pokemon data from api")
        #create headers for csv file
        headers = ['Name', 'Types', 'Abilities', 'Sprite', 'Cry', "Hp", "Attack", 'Special Attack', 'Defense', 'Special Defense', 'Speed']
        #only using relevant data from the api
        all_pokemon_data = []
        api_client.get_all_data(all_pokemon_data) #created function to retrieve the data of the original 151 pokemon
        with open('src/pokeapi/pokemon_data.csv', mode='w', newline='') as file: #open file
            writer = csv.writer(file)
            writer.writerow(headers)  #write the headers
            for pokemon in all_pokemon_data:
                writer.writerow(pokemon)  #write each Pokémon data
        print("All data extracted")

        #call data visualization functions on clean data

    except requests.exceptions.RequestException as e:
        api_client.error_handling(e) #handle errors
    

def main():

    fetch() #fetch the Pokemon from PokeAPI


if __name__ == "__main__":
    main()