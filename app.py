# импорт
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLabel, QApplication, QWidget, QVBoxLayout, QLineEdit, QMainWindow, QMenu, QRadioButton


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(600, 300)
        self.setWindowTitle("Anki Card Generator")

        self.label = QLabel("Text")
        self.input = QLineEdit()
        

        layout = QGridLayout()
        layout.setContentsMargins(50, 80, 50, 80)
        layout.setSpacing(10)
        layout.addWidget(self.input, 0, 0)
        layout.addWidget(self.label, 1, 0)
        for i in range(5):
            self.radio = QRadioButton(f"asdsad{i}", self)
            self.radio.toggled.connect(self.showDetails)
            layout.addWidget(self.radio, i, 1)


        container = QWidget()
        container.setLayout(layout)
        

        self.setCentralWidget(container)


    def show_state(self, s):
        print("adfasdf")

    def showDetails(self):
        print("Selected: ", self.sender().isChecked(),
              "  Name: ", self.sender().text())

# создаю экземпляр QApplication
app = QApplication(sys.argv)

# создаю окно
window = MainWindow()
window.show()

# запускаю цикл событий
app.exec()