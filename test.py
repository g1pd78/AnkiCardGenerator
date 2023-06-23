from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QSizePolicy

if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()

    layout = QGridLayout()

    label1 = QLabel("Label 1")
    lineEdit1 = QLineEdit()

    label2 = QLabel("Label 2")
    lineEdit2 = QLineEdit()

    # Set the size policy of items to Minimum
    label1.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    lineEdit1.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    label2.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    lineEdit2.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    layout.addWidget(label1, 0, 0)
    layout.addWidget(lineEdit1, 0, 1)
    layout.addWidget(label2, 1, 0)
    layout.addWidget(lineEdit2, 1, 1)

    window.setLayout(layout)
    window.show()

    app.exec()
