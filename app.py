# импорт
import sys
import parserText
import wordClass
import appSettings

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
    QRadioButton,
    QStackedWidget,
    QCheckBox,
    QSizePolicy,
)


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
        self.scroll_area2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area2.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area2.setWidgetResizable(True)

        self.setup_ui()


    def setup_ui(self):
        central_widget = QWidget()
        self.main_layout = QVBoxLayout(central_widget)

        widget1 = QWidget()
        layout1 = self.initLayout1(widget1)
        self.scroll_area1.setWidget(widget1)

        widget2 = QWidget()
        layout2 = self.initLayout2(widget2)
        self.scroll_area2.setWidget(widget2)

        self.stacked_widget.addWidget(self.scroll_area1)
        self.stacked_widget.addWidget(self.scroll_area2)

        self.main_layout.addWidget(self.stacked_widget)
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
        inputBlock = QLineEdit()
        inputBlock.setText('example')

        self.button = QPushButton("Поиск!")
        #button.clicked.connect(self.show_scroll_area2)

        container = QWidget()
        buttonandtextlayout = QGridLayout(container)
        self.definition_examples_layout = QGridLayout(widget)
        
        self.definition_examples_layout.setContentsMargins(40, 40, 40, 40)
        self.definition_examples_layout.setSpacing(40)

        buttonandtextlayout.addWidget(inputBlock, 1, 0)
        buttonandtextlayout.addWidget(label, 0, 0)
        buttonandtextlayout.addWidget(self.button, 1, 1)
        self.definition_examples_layout.setVerticalSpacing(10)  # Set size constraint for label
        self.main_layout.addWidget(container)
        
        
        
        self.word = wordClass.Word()
        

        self.button2 = QPushButton("Загрузить еще примеры!")
        
        self.selfMadeText = QLineEdit()

        self.border = 1
        self.counter = 0
        self.counter2 = 0

        def raise_border():
            self.border += 1
            self.drawCheckBoxes()
            self.buttonandtext()

        self.button2.clicked.connect(raise_border)
        self.button.clicked.connect(lambda: self.get_word(inputBlock))
        

        return self.definition_examples_layout
    
    def drawCheckBoxes(self):  
        examples = list(self.word.examples.values())
        for j in range(self.counter2,  len(examples)):
            if self.counter2 >= self.border:
                break
            radio = QCheckBox(self.word.definitions[self.counter2], self)
            #radio.setStyleSheet("")
            radio.toggled.connect(self.showDetails)
            self.definition_examples_layout.addWidget(radio, self.counter + appSettings.DefaultParams.ButtonAndLabelIndent + self.counter2, 0)
            #self.definition_examples_layout.setRowStretch(0, 0)
            self.counter2 += 1
            for i in examples[j]:
                radio = QCheckBox(i, self)
                radio.toggled.connect(self.showDetails)
                #radio.setStyleSheet("")
                radio.setStyleSheet("QCheckBox { margin-left: 20px; }")
                self.definition_examples_layout.addWidget(radio, self.counter + appSettings.DefaultParams.ButtonAndLabelIndent + self.counter2, 0)
                #self.definition_examples_layout.setRowStretch(0, 0)
                self.counter += 1
            self.buttonandtext()

    
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

    def get_word(self, inputBlock):
                search_word = inputBlock.text()
                self.word = parserText.cambridge_definition_parse(search_word)
                self.drawCheckBoxes()
                self.buttonandtext()

    def buttonandtext(self):
        self.definition_examples_layout.addWidget(self.selfMadeText, self.counter + self.counter2 + appSettings.DefaultParams.ButtonAndLabelIndent, 0, Qt.AlignmentFlag.AlignTop)
        self.definition_examples_layout.addWidget(self.button2, self.counter + appSettings.DefaultParams.ButtonAndLabelIndent + self.counter2 + appSettings.DefaultParams.ButtonIndent, 0, Qt.AlignmentFlag.AlignBottom)


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