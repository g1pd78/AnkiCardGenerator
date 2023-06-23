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

        self.word = wordClass.Word()
        self.border = 5
        self.counter = 0
        self.counter2 = 0

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

        # инициализация первой scroll area
        area_widget1 = QWidget()
        layout1 = self.initLayout1(area_widget1)
        self.scroll_area1.setWidget(area_widget1)

        # инициализация второй scroll area
        area_widget2 = QWidget()
        layout2 = self.initLayout2(area_widget2)
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
        last_block.addWidget(left_arrow_button, 0, 0)
        last_block.addWidget(right_arrow_button, 0, 1)
        self.main_layout.addWidget(arrows_container)

        # Подключаем кнопки к слотам переключения scroll area
        left_arrow_button.clicked.connect(self.show_scroll_area1)
        right_arrow_button.clicked.connect(self.show_scroll_area2)

    # инициализация страницы с информацией из кембриджского словаря
    def initLayout1(self, widget) -> QGridLayout:

        # инициализация объектов верхнего layout
        label = QLabel("Введите слово или словосочетание для поиска:")
        input_block = QLineEdit()
        input_block.setText('example')
        self.search_button = QPushButton("Поиск!")

        # помещаю эти объекты в контейнер и заливаю виджет в основной layout
        container = QWidget()
        buttonandtextlayout = QGridLayout(container)
        buttonandtextlayout.addWidget(input_block, 1, 0)
        buttonandtextlayout.addWidget(label, 0, 0)
        buttonandtextlayout.addWidget(self.search_button, 1, 1)
        self.main_layout.addWidget(container)
        
        # layout для определений и примеров
        self.definition_examples_layout = QGridLayout(widget)
        self.definition_examples_layout.setContentsMargins(40, 20, 40, 20)
        
        # инициализация кнопки и поля для пользовательского ввода
        self.more_examples_button = QPushButton("Загрузить еще примеры!")
        self.selfMadeText = QLineEdit()

        # при запросе показать еще примеры увеличивается предел отображаемых checkbox'ов
        def raise_border():
            self.border += 5
            self.drawCheckBoxes()
            self.buttonandtext()

        # цепляю функции к кнопкам
        self.more_examples_button.clicked.connect(raise_border)
        self.search_button.clicked.connect(lambda: self.get_word(input_block))
        
        return self.definition_examples_layout
    
    # инициализация и размещение checkbox'ов
    def drawCheckBoxes(self):  
        examples = list(self.word.examples.values())
        for j in range(self.counter2,  len(examples)):
            # проверка выхода за границу\можно добавить в for
            if self.counter2 >= self.border:
                break

            # инициализация checkbox для определения
            checkbox = QCheckBox(self.word.definitions[self.counter2], self)
            checkbox.toggled.connect(self.showDetails)
            self.definition_examples_layout.addWidget(checkbox, self.counter + appSettings.DefaultParams.ButtonAndLabelIndent + self.counter2, 0)

            self.counter2 += 1
            for i in examples[j]:

                # инициализация checkbox для примеров
                checkbox = QCheckBox(i, self)
                checkbox.toggled.connect(self.showDetails)
                checkbox.setStyleSheet("QCheckBox { margin-left: 20px; }")
                self.definition_examples_layout.addWidget(checkbox, self.counter + appSettings.DefaultParams.ButtonAndLabelIndent + self.counter2, 0)

                self.counter += 1
            self.userInputAndButton()

    # второй layout
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

    # информация о нажатом чекбоксе
    def showDetails(self):
        print("Selected: ", self.sender().isChecked(),
              "  Name: ", self.sender().text())
        
    # пепеключение на первую зону
    def show_scroll_area1(self):
        self.stacked_widget.setCurrentWidget(self.scroll_area1)

    # переключение на вторую зону
    def show_scroll_area2(self):
        self.stacked_widget.setCurrentWidget(self.scroll_area2)

    # при нажатии на кнопку запускается парсер
    def get_word(self, inputBlock):
                search_word = inputBlock.text()
                self.word = parserText.cambridge_definition_parse(search_word)
                self.drawCheckBoxes()
                self.userInputAndButton()

    # Последняя кнопка в layout и lineedit для пользовательского ввода
    def userInputAndButton(self):
        self.definition_examples_layout.addWidget(self.selfMadeText, self.counter + self.counter2 + appSettings.DefaultParams.ButtonAndLabelIndent, 0, Qt.AlignmentFlag.AlignTop)
        self.definition_examples_layout.addWidget(self.more_examples_button, self.counter + appSettings.DefaultParams.ButtonAndLabelIndent + self.counter2 + appSettings.DefaultParams.ButtonIndent, 0, Qt.AlignmentFlag.AlignBottom)


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