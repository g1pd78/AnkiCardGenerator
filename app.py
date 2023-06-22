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
    QCheckBox,
)

import parserText
import wordClass
import appSettings

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(900, 800)
        self.setWindowTitle("Anki Card Generator")

        self.stacked_widget = QStackedWidget()
        self.scroll_area1 = QScrollArea()
        self.scroll_area2 = QScrollArea()

        self.scroll_area1.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area1.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area1.setWidgetResizable(True)

        # make a function for this one
        self.scroll_area1.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area1.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area1.setWidgetResizable(True)

        self.setup_ui()


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
        
    ''' 
        Back and forward arrows ------
        button1 = QPushButton("Scroll Area 1")
        button2 = QPushButton("Scroll Area 2")
        layout.addWidget(button1)
        layout.addWidget(button2)

        # Подключаем кнопки к слотам переключения scroll area
        button1.clicked.connect(self.show_scroll_area1)
        button2.clicked.connect(self.show_scroll_area2)'''

    def show_scroll_area1(self):
        self.stacked_widget.setCurrentWidget(self.scroll_area1)

    def show_scroll_area2(self):
        self.stacked_widget.setCurrentWidget(self.scroll_area2)

    def initLayout1(self, widget) -> QGridLayout:
        label = QLabel("Введите слово или словосочетание для поиска:")
        input = QLineEdit()

        button = QPushButton("Поиск!")
        button.clicked.connect(self.show_scroll_area2)

        layout = QGridLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(10)
        layout.addWidget(input, 1, 0)
        layout.addWidget(label, 0, 0)
        layout.addWidget(button, 1, 1)

        word = wordClass.Word()
        word = parserText.cambridge_definition_parse('head')
        button2 = QPushButton("Загрузить еще примеры!")
        
        selfMadeText = QLineEdit()

        self.border = 5
        self.counter = 0
        self.counter2 = 0

        def raise_border():
            self.border += 1
            print(self.border)
            drawCheckBoxes()

        button2.clicked.connect(raise_border)
        
        def drawCheckBoxes():  

            for j, val in enumerate(word.examples.values(), self.counter2):
                if self.counter2 >= self.border:
                    break
                radio = QCheckBox(word.definitions[self.counter2], self)
                radio.toggled.connect(self.showDetails)
                layout.addWidget(radio, self.counter + appSettings.DefaultParams.ButtonAndLabelIndent + self.counter2, 0)
                self.counter2 += 1
                for i in val:
                    radio = QCheckBox(i, self)
                    radio.toggled.connect(self.showDetails)
                    radio.setStyleSheet("QCheckBox { margin-left: 20px; }")
                    layout.addWidget(radio, self.counter + appSettings.DefaultParams.ButtonAndLabelIndent + self.counter2, 0)
                    self.counter += 1
            layout.addWidget(button2, self.counter + appSettings.DefaultParams.ButtonAndLabelIndent + self.counter2, 0, Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(selfMadeText, self.counter + self.counter2 + appSettings.DefaultParams.ButtonAndLabelIndent + appSettings.DefaultParams.ButtonIndent, 0)


        drawCheckBoxes()

        return layout
    
    
    def initLayout2(self, widget) -> QGridLayout:
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