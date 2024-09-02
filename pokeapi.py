#Haochen Li & Jesse Warren Team Assignment 1
import requests
import csv
import sys
import os
import pandas as pd
# import from other module
from PyQt5.QtWidgets import QLineEdit, QLabel, QMainWindow, QPushButton, QMessageBox, QApplication
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from io import BytesIO

''' Copilot helped to generate the code for main window structure and 
the code to get the pokemon img; modifications are applied thereafter
'''

def file_check():
    file_path = 'data'+'/'+'pokemon_data.csv'

    if(os.path.exists(file_path)):
        return True
    return False

def fetch():
    #initialize client
    api_client = PokeAPI()

    try:
        print("Extracting Pokemon data from api")
        #create headers for csv file
        headers = ['Name', 'Types', 'Abilities', 'Sprite', "Hp", "Attack", 'Special Attack', 'Defense', 'Special Defense', 'Speed']
        #only using relevant data from the api
        all_pokemon_data = []
        api_client.get_all_data(all_pokemon_data) #created function to retrieve the data of the original 151 pokemon
        with open('data/pokemon_data.csv', mode='w', newline='') as file: #open file
            writer = csv.writer(file)
            writer.writerow(headers)  #write the headers
            for pokemon in all_pokemon_data:
                writer.writerow(pokemon)  #write each Pokémon data
        print("All data extracted")

        #call data visualization functions on clean data

    except requests.exceptions.RequestException as e:
        api_client.error_handling(e) #handle errors
    
class PokeAPI():
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

class MainWindow(QMainWindow):
    def __init__(self, pokemon_list:list):
        super().__init__()

        # set the pokemon list
        self.pokemon_list = pokemon_list
        # initialize the main window 
        self.set_main_window()

    '''Function to set the main window of the application'''
    def set_main_window(self):
        self.setWindowTitle("Pokemon Comparison")
        screen_geometry = QApplication.desktop().screenGeometry() # dim of screen
        screen_witdh = screen_geometry.width()
        screen_height = screen_geometry.height()

        width = screen_witdh // 2 # half of screen width
        height = screen_height // 2 

        left_up_x = screen_witdh // 4
        left_up_y = screen_height // 4
        self.setGeometry(left_up_x, left_up_y, width, height)

        ''' add widgets '''
        # add a plain text label
        self.plain_text_label = QLabel("Choose your Pokemon to compare", self)
        ## set font
        font = self.plain_text_label.font()
        font.setPointSize(20)
        font.setBold(True)
        self.plain_text_label.setFont(font)
        self.plain_text_label.setGeometry(400, 60, 1000, 60)

        # an input textbox and prompt info
        self.prompt1 = QLabel("Pokemon 1", self)
        self.prompt1.setGeometry(50, 150, 180, 30)

        self.input_box1 = QLineEdit(self)
        self.input_box1.setGeometry(50, 180, 200, 40)
        self.input_box1.setPlaceholderText("Enter here")

        # an input textbox and prompt info 
        self.prompt2 = QLabel("Pokemon 2", self)
        self.prompt2.setGeometry(50, 240, 180, 30)

        self.input_box2 = QLineEdit(self)
        self.input_box2.setGeometry(50, 270, 200, 40)
        self.input_box2.setPlaceholderText("Enter here")

        # set the comparation button
        self.button = QPushButton("Compare!", self)
        self.button.setGeometry(50, 330, 180, 40)
        self.button.clicked.connect(self.comparison)

        # set the exit button
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setGeometry(50, 500, 180, 40)
        self.exit_button.clicked.connect(self.exit_app)

        '''This area would be used to show the comparison result'''
        self.table = QTableWidget(self)
        self.table.setGeometry(400, 200, 800, 600)
        self.table.setRowCount(10)
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setRowHeight(3, 50)
        self.table.setVerticalHeaderLabels([
            "Name", "Types", "Abilities", "Sprite", "HP", 
            "Attack", "Special Attack", "Defense", "Special Defense", "Speed"
        ])
        

    '''First function, to make sure the input is correct'''
    def comparison(self):
        pokemon1 = self.input_box1.text().lower().replace(" ", "")
        pokemon2 = self.input_box2.text().lower().replace(" ", "")
        
        if pokemon1 in self.pokemon_list and pokemon2 in self.pokemon_list:
            QMessageBox.information(self, "Information", f"Comparing {pokemon1} and {pokemon2}...")
            self.show_comparison(pokemon1, pokemon2)
        elif pokemon1 == "" or pokemon2 == "":
            QMessageBox.warning(self, "Warning: empty input", "Please enter the pokemon names")
        else:
            QMessageBox.warning(self, "Warning: wrong name(s)", "Please enter the pokemon names correctly")

    '''If the input is correct, show the comparison result'''
    def show_comparison(self, pokemon1:str, pokemon2:str):
        # clear message box
        self.input_box1.clear()
        self.input_box2.clear()

        # to be replaced by the api interface
        info_list1 = find_pokemon_info(pokemon1)
        info_list2 = find_pokemon_info(pokemon2)

        # add info to the table
        item_list = ["Name", "Types", "Abilities", "Sprite", "Hp", 
            "Attack", "Special Attack", "Defense", "Special Defense", "Speed"]
        for i in range(10):
            # special case for img
            if i == 3:
                response1 = requests.get(info_list1[0][item_list[i]])
                response2 = requests.get(info_list2[0][item_list[i]])
                img1 = QLabel(self)
                img2 = QLabel(self)
                pixmap1 = QPixmap()
                pixmap2 = QPixmap()
                pixmap1.loadFromData(BytesIO(response1.content).read())
                pixmap2.loadFromData(BytesIO(response2.content).read())
                img1.setPixmap(pixmap1)
                img2.setPixmap(pixmap2)
                img1.setAlignment(Qt.AlignCenter)
                img2.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i, 0, img1)
                self.table.setCellWidget(i, 1, img2)
            # special case for sound
            else:
                # row, col, item
                item1 = QTableWidgetItem(str(info_list1[0][item_list[i]]))
                item2 = QTableWidgetItem(str(info_list2[0][item_list[i]]))
                item1.setTextAlignment(Qt.AlignCenter)
                item2.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, 0, item1)
                self.table.setItem(i, 1, item2)
                    
    '''Function to exit the application'''
    def exit_app(self):
        self.close()

def find_pokemon_info(pokemon_name:str):
    df = pd.read_csv("data/pokemon_data.csv")
    pokemon_info = df.query(f"Name == '{pokemon_name}'").to_dict("records")
    # an example of the return value
    '''[{'Name': 'pikachu', 
    'Types': 'electric', 
    'Abilities': 'static, lightning-rod', 
    'Sprite': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png', 
    'Cry': 'https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/25.ogg', 
    'Hp': 35, 
    'Attack': 55, 
    'Special Attack': 40, 
    'Defense': 50, 
    'Special Defense': 50, 
    'Speed': 90}]'''
    return pokemon_info

def main():

    if not file_check():
        fetch() #fetch the Pokemon from PokeAPI
    app = QApplication(sys.argv)
    df = pd.read_csv("data/pokemon_data.csv")
    pokemon_list = df["Name"].to_list()
    
    window = MainWindow(pokemon_list)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()