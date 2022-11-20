# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 23:35:41 2022

@author: juergen
"""

from gui_player import Ui_MainWindow, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPixmap
import os
import sys
from PyQt5 import QtCore

class gui_player(QDialog):
    
    def __init__(self):
        super().__init__()
        self.image_path1 = 'D:/Projekte/PyAudioPlay/AudioPlay_V0/files/cover1.jpg'
        self.image_path2 = 'D:/Projekte/PyAudioPlay/AudioPlay_V0/files/Book002.jpg'
        self.image_path = ''
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda: self.check_path(2))
        self.ui.pushButton_2.clicked.connect(lambda: self.check_path(1))
        #print(self.checkPath())

    def check_path(self, num=1):
        if num == 1 :
            #image_path = self.ui.lineEdit.text()
            self.image_path = 'D:/Projekte/PyAudioPlay/AudioPlay_V0/files/cover1.jpg'
        else:
            if num == 2 :
                self.image_path = 'D:/Projekte/PyAudioPlay/AudioPlay_V0/files/Book002.jpg'
        print ( self.image_path )
        self.ui.label.text='hallo'#(str(self.image_path))
        if os.path.isfile(self.image_path):
            scene = QtWidgets.QGraphicsScene(self)
            pixmap = QPixmap(self.image_path)
            height = self.ui.graphicsView.height()
            width = self.ui.graphicsView.width()
            pixmap = pixmap.scaled(width, height, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene.addItem(item)
            self.ui.graphicsView.setScene(scene)
            print(height, width)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    class_instance = gui_player()
    class_instance.show()
    sys.exit(app.exec_())