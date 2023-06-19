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
    QStackedWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(900, 800)
        self.setWindowTitle("Anki Card Generator")

        self.stacked_widget = QStackedWidget()
        self.scroll_area1 = QScrollArea()
        self.scroll_area2 = QScrollArea()

        self.setup_ui()


    #def initGUI(self):



        # change settings for scrolling
        #self.scroll1.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        #self.scroll1.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        #self.scroll1.setWidgetResizable(True)

      

        # setting the central widget to show it 
        #self.setCentralWidget(self.scroll)

    def setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        widget1 = QWidget()
        layout1 = self.initLayout1(widget1)
        self.scroll_area1.setWidget(widget1)

        widget2 = QWidget()
        layout2 = self.initLayout2(widget2)
        self.scroll_area2.setWidget(widget2)

        self.stacked_widget.addWidget(self.scroll_area1)
        self.stacked_widget.addWidget(self.scroll_area2)

        layout.addWidget(self.stacked_widget)
        self.setCentralWidget(central_widget)

        button1 = QPushButton("Scroll Area 1")
        button2 = QPushButton("Scroll Area 2")
        layout.addWidget(button1)
        layout.addWidget(button2)

        # Подключаем кнопки к слотам переключения scroll area
        button1.clicked.connect(self.show_scroll_area1)
        button2.clicked.connect(self.show_scroll_area2)

    def show_scroll_area1(self):
        self.stacked_widget.setCurrentWidget(self.scroll_area1)

    def show_scroll_area2(self):
        self.stacked_widget.setCurrentWidget(self.scroll_area2)

    def initLayout1(self, widget):
        label = QLabel("Введите слово или словосочетание для поиска:")
        input = QLineEdit()
        button = QPushButton("Поиск!")
 
        layout = QGridLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(10)
        layout.addWidget(input, 1, 0)
        layout.addWidget(label, 0, 0)
        layout.addWidget(button, 1, 1)

        for i in range(35):
            radio = QRadioButton(f"Банк, у которого был «актив» (в форме займа клиенту) в размере $100,000 в июне, к июлю может получить ноль.{i}", self)
            radio.toggled.connect(self.showDetails)
            layout.addWidget(radio, i+2, 0)

        return layout

        # if last one checked - create another one lineedit for my own text

    def initLayout2(self, widget):
        label = QLabel("Введите слово или словосочетание для поиска:")
        input = QLineEdit()
        button = QPushButton("Поиск!")

        layout = QGridLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(10)
        layout.addWidget(input, 1, 0)
        layout.addWidget(label, 0, 0)
        layout.addWidget(button, 1, 1)

        return layout


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