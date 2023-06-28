import sys

from PyQt6 import QtGui
import parserText
import wordClass
import appSettings
import collections


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

class LayoutUniqueParams:
    layout: QGridLayout
    parser = print()
    checkboxList = []
    label: QLabel
    button: QPushButton
    userText: QLineEdit
    definition_counter: int
    example_counter: int
    border: int
    word_container: wordClass.WordContainer
    word = ''


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # настройка основного окна приложения
        self.resize(900, 800)
        self.setWindowTitle("Anki Card Generator")

        # основной стак виджет, в котором переключаюсь между двумя скролл эреа
        self.stacked_widget = QStackedWidget()
        self.scroll_area1 = QScrollArea()
        self.scroll_area2 = QScrollArea()

        # функция настройки ScrollArea
        self.setup_scroll_area(self.scroll_area1)
        self.setup_scroll_area(self.scroll_area2)

        self.current_page = 0

        self.setup_ui()

    # настройка ScrollArea, enable scroll option
    @staticmethod        
    def setup_scroll_area(area):
        area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        area.setWidgetResizable(True)

    # отрисовка интерфейса
    def setup_ui(self):
        # инициализирую главные widget и layout
        main_widget = QWidget()
        self.main_layout = QVBoxLayout(main_widget)
        self.layout_list = collections.defaultdict(LayoutUniqueParams)

        # инициализация объектов верхнего layout
        label = QLabel("Введите слово или словосочетание для поиска:")
        self.input_block = QLineEdit()
        self.input_block.setText('example')
        self.search_button = QPushButton("Поиск!")

        # помещаю эти объекты в контейнер и заливаю виджет в основной layout
        container = QWidget()
        buttonandtextlayout = QGridLayout(container)
        buttonandtextlayout.addWidget(self.input_block, 1, 0)
        buttonandtextlayout.addWidget(label, 0, 0)
        buttonandtextlayout.addWidget(self.search_button, 1, 1)
        self.main_layout.addWidget(container)

        self.search_button.clicked.connect(self.getWord)

        # инициализация первой scroll area
        area_widget1 = QWidget()
        layout1 = self.cambridgeDictionarySearch(area_widget1)
        self.scroll_area1.setWidget(area_widget1)

        # инициализация второй scroll area
        area_widget2 = QWidget()
        layout2 = self.collinsDictionarySearch(area_widget2)
        self.scroll_area2.setWidget(area_widget2)

        # помещаю scroll area в stacked widget
        self.stacked_widget.addWidget(self.scroll_area1)
        self.stacked_widget.addWidget(self.scroll_area2)
        
        # заливаю главный widget в основной layout, центрирование по main_widget
        self.main_layout.addWidget(self.stacked_widget)
        self.setCentralWidget(main_widget)

        # последний блок с кнопками        
        arrows_container = QWidget()
        last_block = QGridLayout(arrows_container)

        # добавление последних двух кнопок в главный layout
        left_arrow_button = QPushButton("Previous options")
        right_arrow_button = QPushButton("Next options")
        last_block.addWidget(left_arrow_button, 2, 0)
        last_block.addWidget(right_arrow_button, 2, 1)
        self.main_layout.addWidget(arrows_container)

        # Подключаем кнопки к слотам переключения scroll area
        left_arrow_button.clicked.connect(self.showScrollArea1)
        right_arrow_button.clicked.connect(self.showScrollArea2)

    # инициализация страницы с информацией из кембриджского словаря
    def cambridgeDictionarySearch(self, widget) -> QGridLayout:
       
        # layout для определений и примеров
        self.cambridger_definition_examples_layout = QGridLayout(widget)
        #self.definition_examples_layout.setContentsMargins(40, 40, 40, 40)
        self.cambridger_definition_examples_layout.setSpacing(20)

        # инициализация кнопки и поля для пользовательского ввода
        self.cambridger_more_examples_button = QPushButton("Загрузить еще примеры!")
        self.cambridger_selfMadeText = QLineEdit()

        # label в layout с примерами
        self.cambridger_labelDefinitionsExamples = QLabel("Примеры и определения из Cambridge Dictionary:", None)      
        self.cambridger_labelDefinitionsExamples.setMaximumHeight(20)
        self.cambridger_labelDefinitionsExamples.setStyleSheet("color: black; font: bold 15px; background: transparent; border: none; margin: 0px; padding: 0px;")

        # цепляю функции к кнопкам
        self.cambridger_more_examples_button.clicked.connect(self.raiseBorder)

        self.layout_list[0].layout = self.cambridger_definition_examples_layout
        self.layout_list[0].parser = parserText.cambridge_parse
        self.layout_list[0].label = self.cambridger_labelDefinitionsExamples
        self.layout_list[0].button = self.cambridger_more_examples_button
        self.layout_list[0].userText = self.cambridger_selfMadeText
        self.layout_list[0].definition_counter = 0
        self.layout_list[0].example_counter = 0
        self.layout_list[0].border = appSettings.DefaultParams.defaultDefinitionCount
        
        return self.cambridger_definition_examples_layout
    
    # при запросе показать еще примеры увеличивается предел отображаемых checkbox'ов
    def raiseBorder(self):
            self.layout_list[self.current_page].border += appSettings.DefaultParams.borderIncreaseValue
            self.drawCheckBoxes() # add current layout for drawing
            self.userInputAndButton()

    # инициализация и размещение checkbox'ов
    def drawCheckBoxes(self):  
        currentLayoutParams = self.layout_list[self.current_page]
        examples = list(currentLayoutParams.word_container.examples.values())

        for j in range(currentLayoutParams.definition_counter,  len(examples)):
            # проверка выхода за границу\можно добавить в for
            if currentLayoutParams.definition_counter >= currentLayoutParams.border:
                break

            # инициализация checkbox для определения
            checkbox = QCheckBox(currentLayoutParams.word_container.definitions[currentLayoutParams.definition_counter], self)
            checkbox.toggled.connect(self.showDetails)
            currentLayoutParams.layout.addWidget(checkbox, currentLayoutParams.example_counter + appSettings.DefaultParams.LabelIndent + currentLayoutParams.definition_counter, 0, Qt.AlignmentFlag.AlignTop)
            currentLayoutParams.checkboxList.append(checkbox)
            currentLayoutParams.definition_counter += 1
            for i in examples[j]:
                # инициализация checkbox для примеров
                checkbox = QCheckBox(i, self)
                checkbox.toggled.connect(self.showDetails)
                checkbox.setStyleSheet("QCheckBox { margin-left: 20px; }")
                currentLayoutParams.layout.addWidget(checkbox, currentLayoutParams.example_counter + appSettings.DefaultParams.LabelIndent + currentLayoutParams.definition_counter, 0, Qt.AlignmentFlag.AlignTop)
                currentLayoutParams.checkboxList.append(checkbox)

                currentLayoutParams.example_counter += 1
            self.userInputAndButton()

    # второй layout
    def collinsDictionarySearch(self, widget) -> QGridLayout:
       
        # layout для определений и примеров
        self.collins_definition_examples_layout = QGridLayout(widget)
        self.collins_definition_examples_layout.setSpacing(20)


        # инициализация кнопки и поля для пользовательского ввода
        self.collins_more_examples_button = QPushButton("Загрузить еще примеры!")
        self.collins_selfMadeText = QLineEdit()

        # label в layout с примерами
        self.collins_labelDefinitionsExamples = QLabel("Примеры и определения из Collins Dictionary:", None)      
        self.collins_labelDefinitionsExamples.setMaximumHeight(20)
        self.collins_labelDefinitionsExamples.setStyleSheet("color: black; font: bold 15px; background: transparent; border: none; margin: 0px; padding: 0px;")

        # цепляю функции к кнопкам
        self.collins_more_examples_button.clicked.connect(self.raiseBorder)
        
        self.layout_list[1].layout = self.collins_definition_examples_layout
        self.layout_list[1].parser = parserText.collins_parse
        self.layout_list[1].label = self.collins_labelDefinitionsExamples
        self.layout_list[1].button = self.collins_more_examples_button
        self.layout_list[1].userText = self.collins_selfMadeText
        self.layout_list[1].definition_counter = 0
        self.layout_list[1].example_counter = 0
        self.layout_list[1].border = appSettings.DefaultParams.defaultDefinitionCount

        return self.collins_definition_examples_layout

    # информация о нажатом чекбоксе
    def showDetails(self):
        print("Selected: ", self.sender().isChecked(),
              "  Name: ", self.sender().text())
        
    # пепеключение на первую зону
    def showScrollArea1(self):
        self.stacked_widget.setCurrentWidget(self.scroll_area1)
        self.current_page = 0

    # переключение на вторую зону
    def showScrollArea2(self):
        self.stacked_widget.setCurrentWidget(self.scroll_area2)
        self.current_page = 1

    # при нажатии на кнопку запускается парсер
    def getWord(self):
        currentLayoutParams = self.layout_list[self.current_page]
        search_word = self.input_block.text()
        if search_word != currentLayoutParams.word:
            currentLayoutParams.border = appSettings.DefaultParams.defaultDefinitionCount
            currentLayoutParams.definition_counter = 0
            currentLayoutParams.example_counter = 0
            self.getCheckedBoxes()
            self.removeAllCheckboxes()
            currentLayoutParams.word_container = currentLayoutParams.parser(search_word)
            self.word = search_word
        self.drawCheckBoxes()
        self.userInputAndButton()
        print(self.current_page)

    # Последняя кнопка в layout и lineedit для пользовательского ввода
    def userInputAndButton(self):
        currentLayoutParams = self.layout_list[self.current_page]
        currentLayoutParams.layout.addWidget(currentLayoutParams.label, 0, 0, Qt.AlignmentFlag.AlignTop)
        currentLayoutParams.layout.addWidget(currentLayoutParams.userText, currentLayoutParams.example_counter + currentLayoutParams.definition_counter + appSettings.DefaultParams.LabelIndent, 0, Qt.AlignmentFlag.AlignTop)
        currentLayoutParams.layout.addWidget(currentLayoutParams.button, currentLayoutParams.example_counter + appSettings.DefaultParams.LabelIndent + currentLayoutParams.definition_counter + appSettings.DefaultParams.ButtonIndent, 0, Qt.AlignmentFlag.AlignBottom)

    def removeAllCheckboxes(self):
        for checkbox in self.layout_list[self.current_page].checkboxList:
            self.layout_list[self.current_page].layout.removeWidget(checkbox)
            checkbox.deleteLater()
            checkbox = None
        self.layout_list[self.current_page].checkboxList.clear()
        
    def getCheckedBoxes(self):
        finalCard = []
        for checkbox in self.layout_list[self.current_page].checkboxList:
            if checkbox.isChecked():
                finalCard.append(checkbox.text())

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Return.value:
            self.getWord()

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