from PyQt5.QtWidgets import QLabel, QComboBox, QMainWindow, QPushButton, QMessageBox, QApplication

class MainWindow(QMainWindow):
    def __init__(self, pokemon_list:list):
        super().__init__()

        # initialize the main window 
        self.set_main_window(pokemon_list)

    '''Function to set the main window of the application'''
    def set_main_window(self, pokemon_list:list):
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
        
        self.plain_text_label.setGeometry(50, 60, width//2, 30)

        # add a pull-down selector
        self.combo_box = QComboBox(self)
        self.combo_box.setGeometry(50, 150, 180, 30)
        self.combo_box.addItems(pokemon_list)

        # add a pull-down selector
        self.combo_box = QComboBox(self)
        self.combo_box.setGeometry(50, 240, 180, 30)
        self.combo_box.addItems(pokemon_list)

        # set the comparation button
        self.button = QPushButton("Compare!", self)
        self.button.setGeometry(50, 330, 180, 40)
        self.button.clicked.connect(self.show_message)

        return self

    def show_message(self):
        QMessageBox.information(self, "Message", "Hello, PyQt!")