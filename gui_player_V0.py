# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Projekte\PyAudioPlay\AudioPlay_V0\QT_GUI\gui_player_V0.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButtonCD = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonCD.sizePolicy().hasHeightForWidth())
        self.pushButtonCD.setSizePolicy(sizePolicy)
        self.pushButtonCD.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonCD.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(25)
        self.pushButtonCD.setFont(font)
        self.pushButtonCD.setObjectName("pushButtonCD")
        self.gridLayout_2.addWidget(self.pushButtonCD, 0, 0, 1, 1)
        self.labelAlbum = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelAlbum.sizePolicy().hasHeightForWidth())
        self.labelAlbum.setSizePolicy(sizePolicy)
        self.labelAlbum.setMinimumSize(QtCore.QSize(253, 60))
        self.labelAlbum.setMaximumSize(QtCore.QSize(400, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelAlbum.setFont(font)
        self.labelAlbum.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.labelAlbum.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.labelAlbum.setScaledContents(True)
        self.labelAlbum.setObjectName("labelAlbum")
        self.gridLayout_2.addWidget(self.labelAlbum, 0, 1, 1, 1)
        self.pushButtonRadio = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonRadio.sizePolicy().hasHeightForWidth())
        self.pushButtonRadio.setSizePolicy(sizePolicy)
        self.pushButtonRadio.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonRadio.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(25)
        self.pushButtonRadio.setFont(font)
        self.pushButtonRadio.setObjectName("pushButtonRadio")
        self.gridLayout_2.addWidget(self.pushButtonRadio, 4, 4, 1, 1)
        self.pushButtonAmp = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAmp.sizePolicy().hasHeightForWidth())
        self.pushButtonAmp.setSizePolicy(sizePolicy)
        self.pushButtonAmp.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonAmp.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(25)
        self.pushButtonAmp.setFont(font)
        self.pushButtonAmp.setObjectName("pushButtonAmp")
        self.gridLayout_2.addWidget(self.pushButtonAmp, 5, 4, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 8, 0, 1, 5)
        self.pushButtonSearch = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSearch.sizePolicy().hasHeightForWidth())
        self.pushButtonSearch.setSizePolicy(sizePolicy)
        self.pushButtonSearch.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonSearch.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(25)
        self.pushButtonSearch.setFont(font)
        self.pushButtonSearch.setObjectName("pushButtonSearch")
        self.gridLayout_2.addWidget(self.pushButtonSearch, 2, 4, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonBack = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonBack.sizePolicy().hasHeightForWidth())
        self.pushButtonBack.setSizePolicy(sizePolicy)
        self.pushButtonBack.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonBack.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(22)
        self.pushButtonBack.setFont(font)
        self.pushButtonBack.setObjectName("pushButtonBack")
        self.gridLayout.addWidget(self.pushButtonBack, 0, 0, 1, 1)
        self.pushButtonRec = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonRec.sizePolicy().hasHeightForWidth())
        self.pushButtonRec.setSizePolicy(sizePolicy)
        self.pushButtonRec.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonRec.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(22)
        self.pushButtonRec.setFont(font)
        self.pushButtonRec.setObjectName("pushButtonRec")
        self.gridLayout.addWidget(self.pushButtonRec, 0, 1, 1, 1)
        self.pushButtonPause = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonPause.sizePolicy().hasHeightForWidth())
        self.pushButtonPause.setSizePolicy(sizePolicy)
        self.pushButtonPause.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonPause.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(22)
        self.pushButtonPause.setFont(font)
        self.pushButtonPause.setObjectName("pushButtonPause")
        self.gridLayout.addWidget(self.pushButtonPause, 0, 2, 1, 1)
        self.pushButtonPlay = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonPlay.sizePolicy().hasHeightForWidth())
        self.pushButtonPlay.setSizePolicy(sizePolicy)
        self.pushButtonPlay.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonPlay.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(22)
        self.pushButtonPlay.setFont(font)
        self.pushButtonPlay.setObjectName("pushButtonPlay")
        self.gridLayout.addWidget(self.pushButtonPlay, 0, 3, 1, 1)
        self.pushButtonNext = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonNext.sizePolicy().hasHeightForWidth())
        self.pushButtonNext.setSizePolicy(sizePolicy)
        self.pushButtonNext.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonNext.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(22)
        self.pushButtonNext.setFont(font)
        self.pushButtonNext.setObjectName("pushButtonNext")
        self.gridLayout.addWidget(self.pushButtonNext, 0, 4, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 7, 0, 1, 2)
        self.pushButtonUp = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonUp.sizePolicy().hasHeightForWidth())
        self.pushButtonUp.setSizePolicy(sizePolicy)
        self.pushButtonUp.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonUp.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Wingdings 3")
        font.setPointSize(25)
        self.pushButtonUp.setFont(font)
        self.pushButtonUp.setObjectName("pushButtonUp")
        self.gridLayout_2.addWidget(self.pushButtonUp, 0, 4, 1, 1)
        self.pushButtonUndo = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonUndo.sizePolicy().hasHeightForWidth())
        self.pushButtonUndo.setSizePolicy(sizePolicy)
        self.pushButtonUndo.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonUndo.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(28)
        self.pushButtonUndo.setFont(font)
        self.pushButtonUndo.setObjectName("pushButtonUndo")
        self.gridLayout_2.addWidget(self.pushButtonUndo, 7, 3, 1, 1)
        self.pushButtonTrack = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonTrack.sizePolicy().hasHeightForWidth())
        self.pushButtonTrack.setSizePolicy(sizePolicy)
        self.pushButtonTrack.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonTrack.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(25)
        self.pushButtonTrack.setFont(font)
        self.pushButtonTrack.setObjectName("pushButtonTrack")
        self.gridLayout_2.addWidget(self.pushButtonTrack, 1, 0, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 2, 0, 5, 2)
        self.pushButtonImage = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonImage.sizePolicy().hasHeightForWidth())
        self.pushButtonImage.setSizePolicy(sizePolicy)
        self.pushButtonImage.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonImage.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Webdings")
        font.setPointSize(25)
        self.pushButtonImage.setFont(font)
        self.pushButtonImage.setObjectName("pushButtonImage")
        self.gridLayout_2.addWidget(self.pushButtonImage, 6, 4, 1, 1)
        self.labelStatus = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelStatus.sizePolicy().hasHeightForWidth())
        self.labelStatus.setSizePolicy(sizePolicy)
        self.labelStatus.setMinimumSize(QtCore.QSize(310, 60))
        self.labelStatus.setObjectName("labelStatus")
        self.gridLayout_2.addWidget(self.labelStatus, 7, 2, 1, 1)
        self.pushButtonDown = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonDown.sizePolicy().hasHeightForWidth())
        self.pushButtonDown.setSizePolicy(sizePolicy)
        self.pushButtonDown.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonDown.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Wingdings 3")
        font.setPointSize(25)
        self.pushButtonDown.setFont(font)
        self.pushButtonDown.setObjectName("pushButtonDown")
        self.gridLayout_2.addWidget(self.pushButtonDown, 1, 4, 1, 1)
        self.pushButtonLoop = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonLoop.sizePolicy().hasHeightForWidth())
        self.pushButtonLoop.setSizePolicy(sizePolicy)
        self.pushButtonLoop.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButtonLoop.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Wingdings 3")
        font.setPointSize(25)
        self.pushButtonLoop.setFont(font)
        self.pushButtonLoop.setObjectName("pushButtonLoop")
        self.gridLayout_2.addWidget(self.pushButtonLoop, 3, 4, 1, 1)
        self.labelTitel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTitel.sizePolicy().hasHeightForWidth())
        self.labelTitel.setSizePolicy(sizePolicy)
        self.labelTitel.setMinimumSize(QtCore.QSize(253, 60))
        self.labelTitel.setMaximumSize(QtCore.QSize(400, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.labelTitel.setFont(font)
        self.labelTitel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.labelTitel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.labelTitel.setScaledContents(True)
        self.labelTitel.setObjectName("labelTitel")
        self.gridLayout_2.addWidget(self.labelTitel, 1, 1, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setMinimumSize(QtCore.QSize(384, 475))
        self.listWidget.setSizeIncrement(QtCore.QSize(0, 0))
        self.listWidget.setObjectName("listWidget")
        self.gridLayout_2.addWidget(self.listWidget, 0, 2, 7, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionRun = QtWidgets.QAction(MainWindow)
        self.actionRun.setObjectName("actionRun")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MultiSound V1.0 (Audio Player/Radio/Pre-Amplifier)"))
        self.pushButtonCD.setText(_translate("MainWindow", "³"))
        self.labelAlbum.setText(_translate("MainWindow", "TextLabel"))
        self.pushButtonRadio.setText(_translate("MainWindow", "»"))
        self.pushButtonAmp.setText(_translate("MainWindow", "X"))
        self.pushButtonSearch.setText(_translate("MainWindow", "L"))
        self.pushButtonBack.setText(_translate("MainWindow", "9"))
        self.pushButtonRec.setText(_translate("MainWindow", "="))
        self.pushButtonPause.setText(_translate("MainWindow", ";"))
        self.pushButtonPlay.setText(_translate("MainWindow", "4"))
        self.pushButtonNext.setText(_translate("MainWindow", ":"))
        self.pushButtonUp.setText(_translate("MainWindow", "ã"))
        self.pushButtonUndo.setText(_translate("MainWindow", "q"))
        self.pushButtonTrack.setText(_translate("MainWindow", "¯"))
        self.pushButtonImage.setText(_translate("MainWindow", "¶"))
        self.labelStatus.setText(_translate("MainWindow", "TextLabel"))
        self.pushButtonDown.setText(_translate("MainWindow", "ä"))
        self.pushButtonLoop.setText(_translate("MainWindow", "P"))
        self.labelTitel.setText(_translate("MainWindow", "TextLabel"))
        self.actionRun.setText(_translate("MainWindow", "Run"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
