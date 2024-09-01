import click
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
import pandas as pd
# import from other module
from pokeapi.datacvisualization import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # todo: link this list to a csv file indicating the pokemon names
    df = pd.read_csv("src/pokeapi/pokemon_data.csv")
    pokemon_list = df["Name"].to_list()
    
    # todo: may need to add a instance for handling the api interface
    window = MainWindow(pokemon_list)
    window.show()
    app.exec_()
    