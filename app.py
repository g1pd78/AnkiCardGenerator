# импорт
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QPushButton, 
    QScrollArea, 
    QGridLayout, 
    QLabel, 
    QApplication, 
    QWidget, 
    QVBoxLayout, 
    QLineEdit, 
    QMainWindow, 
    QMenu, 
    QRadioButton,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initGUI()

    def initGUI(self):
        # area for scrolling option
        self.scroll = QScrollArea()

        self.resize(900, 800)
        self.setWindowTitle("Anki Card Generator")

        # 

    
        self.label = QLabel("Введите слово или словосочетание для поиска:")
        self.input = QLineEdit()
        self.button = QPushButton("Поиск!")

        layout = QGridLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(10)
        layout.addWidget(self.input, 1, 0)
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.button, 1, 1)

        for i in range(35):
            self.radio = QRadioButton(f"Банк, у которого был «актив» (в форме займа клиенту) в размере $100,000 в июне, к июлю может получить ноль.{i}", self)
            self.radio.toggled.connect(self.showDetails)
            layout.addWidget(self.radio, i+2, 0)

        # if last one checked - create another one lineedit for my own text

        # change settings for scrolling
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)

        # create a widget to set it as central
        container = QWidget()
        container.setLayout(layout)
        self.scroll.setWidget(container)

        # setting the central widget to show it 
        self.setCentralWidget(self.scroll)


    def show_state(self, s):
        print("adfasdf")

    def showDetails(self):
        print("Selected: ", self.sender().isChecked(),
              "  Name: ", self.sender().text())


def main():
    
    # создаю экземпляр QApplication
    app = QApplication(sys.argv)

    # создаю окно
    window = MainWindow()
    window.show()

    # запускаю цикл событий
    app.exec()

if __name__ == '__main__':
    main()