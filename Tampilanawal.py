# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Tampilanawal.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Tampilanutama import Ui_MainWindow
from PyQt5.QtGui import QIcon, QPixmap
import sqlite3

class Ui_Login(object):
    def showMessageBox(self,title,message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()
    def welcomeWindowShow(self):
        self.welcomeWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.welcomeWindow)
        self.welcomeWindow.show()

    def loginCheck(self):
        username = self.lineUsername.text()
        password = self.linePassword.text()

        connection = sqlite3.connect("Admin.db")
        result = connection.execute("SELECT * FROM dataadmin WHERE USERNAME = ? AND PASSWORD = ?", (username, password))
        if (len(result.fetchall()) > 0):
            print("User Found ! ")
            self.welcomeWindowShow()

        else:
            print("User Not Found !")
            self.showMessageBox('Warning', 'Invalid Username And Password')
        connection.close()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter:
            self.loginCheck()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(498, 435)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 10, 392, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setToolTipDuration(0)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(100, 360, 301, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 80, 441, 231))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelUsername = QtWidgets.QLabel(self.layoutWidget)
        self.labelUsername.setObjectName("labelUsername")
        self.horizontalLayout.addWidget(self.labelUsername)
        self.lineUsername = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineUsername.setObjectName("lineUsername")
        self.lineUsername.setFixedSize(QtCore.QSize(150, 20))

        self.horizontalLayout.addWidget(self.lineUsername)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelPassword = QtWidgets.QLabel(self.layoutWidget)
        self.labelPassword.setObjectName("labelPassword")
        self.horizontalLayout_2.addWidget(self.labelPassword)
        self.linePassword = QtWidgets.QLineEdit(self.layoutWidget)
        self.linePassword.setObjectName("linePassword")
        self.linePassword.setFixedSize(QtCore.QSize(150,20))
        self.horizontalLayout_2.addWidget(self.linePassword)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.loginButton = QtWidgets.QPushButton(self.layoutWidget)
        self.loginButton.setObjectName("loginButton")
        self.verticalLayout.addWidget(self.loginButton)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 498, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        self.linePassword.setEchoMode(self.linePassword.Password)
        self.loginButton.clicked.connect(self.loginCheck)
        self.linePassword.returnPressed.connect(self.loginCheck)
        pixmap = QtGui.QPixmap('Logo Gundar.png')
        self.label_3.setPixmap(pixmap.scaled(200,250,QtCore.Qt.KeepAspectRatio))


        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Welcome"))
        self.label.setText(_translate("MainWindow", "DETEKSI PELAT NOMOR KENDARAAN"))
        self.label_2.setText(_translate("MainWindow", "UNIVERSITAS GUNADARMA"))

        self.label_4.setText(_translate("MainWindow", "Log In"))
        self.labelUsername.setText(_translate("MainWindow", "USERNAME"))
        self.labelPassword.setText(_translate("MainWindow", "PASSWORD"))
        self.loginButton.setText(_translate("MainWindow", "LogIn"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Login()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

