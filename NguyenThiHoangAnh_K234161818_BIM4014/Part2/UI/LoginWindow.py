# Form implementation generated from reading ui file 'LoginWindow.ui'
#
# Created by ChatGPT based on Qt Designer structure
# Compatible with: PyQt6

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(400, 280)
        LoginWindow.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        
        self.verticalLayout = QtWidgets.QVBoxLayout(LoginWindow)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setContentsMargins(30, 30, 30, 30)
        self.verticalLayout.setObjectName("verticalLayout")
        
        # Title
        self.lblTitle = QtWidgets.QLabel(parent=LoginWindow)
        self.lblTitle.setObjectName("lblTitle")
        self.lblTitle.setText("ĐĂNG NHẬP")
        self.lblTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lblTitle.setStyleSheet("font-weight: bold; font-size: 16pt;")
        self.verticalLayout.addWidget(self.lblTitle)
        
        # Form Layout
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSpacing(15)
        self.formLayout.setObjectName("formLayout")
        
        # Email field
        self.lblEmail = QtWidgets.QLabel(parent=LoginWindow)
        self.lblEmail.setObjectName("lblEmail")
        self.lblEmail.setText("Email:")
        self.txtEmail = QtWidgets.QLineEdit(parent=LoginWindow)
        self.txtEmail.setObjectName("txtEmail")
        self.txtEmail.setMinimumSize(QtCore.QSize(0, 35))
        self.txtEmail.setPlaceholderText("Nhập email của bạn")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.lblEmail)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.txtEmail)
        
        # Password field
        self.lblPassword = QtWidgets.QLabel(parent=LoginWindow)
        self.lblPassword.setObjectName("lblPassword")
        self.lblPassword.setText("Mật khẩu:")
        self.txtPassword = QtWidgets.QLineEdit(parent=LoginWindow)
        self.txtPassword.setObjectName("txtPassword")
        self.txtPassword.setMinimumSize(QtCore.QSize(0, 35))
        self.txtPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txtPassword.setPlaceholderText("Nhập mật khẩu")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.lblPassword)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.txtPassword)
        
        self.verticalLayout.addLayout(self.formLayout)
        
        # Buttons
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.btnLogin = QtWidgets.QPushButton(parent=LoginWindow)
        self.btnLogin.setObjectName("btnLogin")
        self.btnLogin.setMinimumSize(QtCore.QSize(0, 40))
        self.btnLogin.setText("Đăng nhập")
        self.btnLogin.setStyleSheet("""
            QPushButton {
                background-color: #9CAFAA;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7A9A8A;
            }
            QPushButton:pressed {
                background-color: #6A8A7A;
            }
        """)
        
        self.btnCancel = QtWidgets.QPushButton(parent=LoginWindow)
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.setMinimumSize(QtCore.QSize(0, 40))
        self.btnCancel.setText("Hủy")
        self.btnCancel.setStyleSheet("""
            QPushButton {
                background-color: #CCCCCC;
                color: black;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #BBBBBB;
            }
        """)
        
        self.horizontalLayout.addWidget(self.btnLogin)
        self.horizontalLayout.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        # Attempts label
        self.lblAttempts = QtWidgets.QLabel(parent=LoginWindow)
        self.lblAttempts.setObjectName("lblAttempts")
        self.lblAttempts.setText("")
        self.lblAttempts.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lblAttempts.setStyleSheet("color: red; font-size: 10pt;")
        self.verticalLayout.addWidget(self.lblAttempts)
        
        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)
    
    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Đăng nhập - Employee Management System"))

