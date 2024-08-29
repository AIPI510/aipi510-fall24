import click
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

# import from other module
from pokeapi.datacvisualization import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    pokemon_list = ["Pikachu", "Charmander", "Bulbasaur", "Squirtle"]
    window = MainWindow(pokemon_list)
    window.show()
    app.exec_()