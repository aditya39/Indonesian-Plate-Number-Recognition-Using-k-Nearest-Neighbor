# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'database.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from insertData import Ui_InsertData
from Sqlitehelper import SqliteHelper
import sqlite3

class Ui_DataKendaraan(object):

    def showMessageBox2(self,title,message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        msgBox.exec_()
        if msgBox == QtWidgets.QMessageBox.Yes:
            self.deleteData()


    def welcomeWindowShow(self):
        self.welcomeWindow = QtWidgets.QMainWindow()
        self.ui = Ui_InsertData()
        self.ui.setupUi(self.welcomeWindow)
        self.ui.addButton.clicked.connect(self.addData)
        self.welcomeWindow.show()


    def loadData(self):
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0)
        conn = sqlite3.connect('Kendaraan.db')
        helper = SqliteHelper("Kendaraan.db")
        dataKendaraan = helper.select("Select * FROM datakendaraan")
        count=0
        dataKendaraan2 = helper.select("Select * FROM datakendaraan WHERE NO_POLISI = 'B1543EFQ'")
        data = dataKendaraan2[0]
        print(data[2])
        for row_number, row_data in enumerate(dataKendaraan):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_number, column_number, cell)
        conn.close()


        self.labelUser.setText("Total Users : "+str(self.tableWidget.rowCount()))
        return

    def addData(self):
        helper = SqliteHelper("Kendaraan.db")
        Id = self.ui.idLine.text()
        Name = self.ui.namaLine.text()
        noPlate = self.ui.nomorpolisiLine.text()
        Vehicle = self.ui.kendaraanLine.text()
        Type = self.ui.jenisLine.text()
        Year = self.ui.tahunLine.text()
        City = self.ui.kotaLine.text()
        Status = self.ui.statusLine.text()
        data = (Id, Name, noPlate, Vehicle, Type, Year, City, Status)
        helper.insert("INSERT INTO datakendaraan (ID,NAMA,NO_POLISI,KENDARAAN,JENIS,TAHUN,KOTA,STATUS) VALUES(?,?,?,?,?,?,?,?)", data)
        self.clearData()
        self.loadData()
        self.ui.clear()
        self.ui.showMessageBox("Success !!", "Data Sukses dimasukkan !")

    def clearData(self):
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0)


    def refresh(self):
        self.clearData()
        self.loadData()

    def deleteData(self):
        ret = QtWidgets.QMessageBox.Yes
        confirmBox = QtWidgets.QMessageBox()
        confirmBox.setText("Apakah anda yakin ingin menghapus record tersebut ?")
        confirmBox.setWindowTitle("Konfirmasi")
        confirmBox.setIcon(QtWidgets.QMessageBox.Warning)
        confirmBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        confirmBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        ret = confirmBox.exec_()
        if ret == QtWidgets.QMessageBox.Yes:
            conn = sqlite3.connect("Kendaraan.db")
            content = 'SELECT * FROM datakendaraan'
            c = conn.cursor()
            res = c.execute(content)
            for row_number in enumerate(res):
                if row_number[0] == self.tableWidget.currentRow():
                    data = row_number[1]
                    Id = data[0]
                    Name = data[1]
                    noPlate = data[2]
                    Vehicle = data[3]
                    Type = data[4]
                    Year = data[5]
                    City = data[6]
                    Status = data[7]
                    print(Id)
                    print(row_number[0])
                    c.execute("DELETE FROM datakendaraan WHERE ID=? AND NAMA=? AND NO_POLISI=? AND KENDARAAN=? AND JENIS=? AND TAHUN=? AND KOTA=? AND STATUS=? ",
                              (Id,Name,noPlate,Vehicle,Type,Year,City,Status,))
                    conn.commit()
                    self.loadData()






    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.editButton = QtWidgets.QPushButton(self.centralwidget)
        self.editButton.setMinimumSize(QtCore.QSize(0, 30))
        self.editButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.editButton.setSizeIncrement(QtCore.QSize(0, 0))
        self.editButton.setObjectName("editButton")
        self.horizontalLayout_2.addWidget(self.editButton)
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setMinimumSize(QtCore.QSize(0, 30))
        self.deleteButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout_2.addWidget(self.deleteButton)
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setMinimumSize(QtCore.QSize(0, 30))
        self.addButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_2.addWidget(self.addButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.searchButton = QtWidgets.QLabel(self.centralwidget)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout_3.addWidget(self.searchButton)
        self.lineSearch = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineSearch.setFont(font)
        self.lineSearch.setObjectName("lineSearch")
        self.horizontalLayout_3.addWidget(self.lineSearch)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)
        self.labelUser = QtWidgets.QLabel(self.centralwidget)
        self.labelUser.setObjectName("labelUser")
        self.gridLayout_2.addWidget(self.labelUser, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.addButton.clicked.connect(self.welcomeWindowShow)
        self.loadData()

        self.deleteButton.clicked.connect(self.deleteData)

        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Database"))
        self.label.setText(_translate("MainWindow", "Database"))
        self.editButton.setText(_translate("MainWindow", "Edit"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
        self.addButton.setText(_translate("MainWindow", "Add"))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Nama Pemilik"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Nomor Polisi"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Kendaraan"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Jenis "))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Tahun"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Kota"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Status"))




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_DataKendaraan()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())

