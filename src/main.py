import requests
import csv
import sys
import pandas as pd
from PyQt5.QtWidgets import QLineEdit, QLabel, QMainWindow, QPushButton, QMessageBox, QApplication
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from io import BytesIO

'''Class and function to fetch data'''

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


if __name__ == "__main__":

    app = QApplication(sys.argv)
    # todo: link this list to a csv file indicating the pokemon names
    df = pd.read_csv("src/pokeapi/pokemon_data.csv")
    pokemon_list = df["Name"].to_list()
    
    # todo: may need to add a instance for handling the api interface
    window = MainWindow(pokemon_list)
    window.show()
    app.exec_()
    