# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qi_rear.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(855, 725)
        font = QtGui.QFont()
        font.setPointSize(100)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidgetLog = QtWidgets.QListWidget(self.centralwidget)
        self.listWidgetLog.setGeometry(QtCore.QRect(5, 0, 340, 500))
        self.listWidgetLog.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidgetLog.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidgetLog.setObjectName("listWidgetLog")
        self.radioButton_1 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_1.setGeometry(QtCore.QRect(30, 510, 130, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_1.setFont(font)
        self.radioButton_1.setChecked(True)
        self.radioButton_1.setObjectName("radioButton_1")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(200, 510, 130, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(5, 540, 680, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.buttonTalk = QtWidgets.QPushButton(self.centralwidget)
        self.buttonTalk.setGeometry(QtCore.QRect(690, 540, 160, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.buttonTalk.setFont(font)
        self.buttonTalk.setObjectName("buttonTalk")
        self.labelResponce = QtWidgets.QLabel(self.centralwidget)
        self.labelResponce.setGeometry(QtCore.QRect(350, 300, 500, 200))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelResponce.setFont(font)
        self.labelResponce.setFrameShape(QtWidgets.QFrame.Box)
        self.labelResponce.setText("")
        self.labelResponce.setAlignment(QtCore.Qt.AlignCenter)
        self.labelResponce.setObjectName("labelResponce")
        self.labelShowImg = QtWidgets.QLabel(self.centralwidget)
        self.labelShowImg.setGeometry(QtCore.QRect(350, 10, 441, 251))
        self.labelShowImg.setText("")
        self.labelShowImg.setPixmap(QtGui.QPixmap(":/re/talk.gif"))
        self.labelShowImg.setObjectName("labelShowImg")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 855, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuClose = QtWidgets.QAction(MainWindow)
        self.menuClose.setObjectName("menuClose")
        self.menu.addAction(self.menuClose)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.buttonTalk.clicked.connect(MainWindow.buttonTalkSlot)
        self.radioButton_1.clicked.connect(MainWindow.showResponderName)
        self.radioButton_2.clicked.connect(MainWindow.showResponderName)
        self.menuClose.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.radioButton_1.setText(_translate("MainWindow", "Responderを表示"))
        self.radioButton_2.setText(_translate("MainWindow", "Responderを非表示"))
        self.buttonTalk.setText(_translate("MainWindow", "話す"))
        self.menu.setTitle(_translate("MainWindow", "ファイル"))
        self.menuClose.setText(_translate("MainWindow", "閉じる"))

