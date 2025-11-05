# Form implementation generated from reading ui file 'house_price_ui.ui'
from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 400)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.title = QtWidgets.QLabel("🏠 House Price Prediction", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.title.setFont(font)
        self.verticalLayout.addWidget(self.title)

        self.formLayout = QtWidgets.QFormLayout()
        self.area_income = QtWidgets.QLineEdit()
        self.formLayout.addRow("Avg. Area Income:", self.area_income)

        self.house_age = QtWidgets.QLineEdit()
        self.formLayout.addRow("Avg. Area House Age:", self.house_age)

        self.num_rooms = QtWidgets.QLineEdit()
        self.formLayout.addRow("Avg. Area Number of Rooms:", self.num_rooms)

        self.num_bedrooms = QtWidgets.QLineEdit()
        self.formLayout.addRow("Avg. Area Number of Bedrooms:", self.num_bedrooms)

        self.population = QtWidgets.QLineEdit()
        self.formLayout.addRow("Area Population:", self.population)

        self.verticalLayout.addLayout(self.formLayout)

        self.predict_button = QtWidgets.QPushButton("Predict Price")
        self.verticalLayout.addWidget(self.predict_button)

        self.result_label = QtWidgets.QLabel("Result: ...")
        self.result_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.result_label)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("House Price Prediction")
