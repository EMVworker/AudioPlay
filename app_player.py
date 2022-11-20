# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:26:36 2022

@author: juergen
"""
import sys
sys.path.insert(0,'D:/Projekte/PyAudioPlay/AudioPlay_V0/')
#from ctrl_player import DirectPlay
#from ctrl_player import ListData
from ctrl_player import HmiPlay
import ctrl_player
import os
sys.path.insert(0,'D:/Projekte/PyAudioPlay/AudioPlay_V0/')
from gui_player import Ui_MainWindow
from form_image import Ui_FormImage
from diag_keyboard import Ui_DialogKeyboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtGui import QPixmap


class DlgKeyboard(QDialog):
    """ Dialog Keyboard """
    def __init__(self, parent=None):
        # super(DlgKeyboard, self).__init__(parent)
        super().__init__(parent)
        self.ui = Ui_DialogKeyboard() # Create an instance of the GUI
        self.ui.setupUi(self) # Run the .setupUi() method to show the GUI
        #--- Connect Widgets ---
        self.ui.pushButton_3.clicked.connect(self.form_close)

    def closeEvent(self, event):
        """ Close-Event """
        print('>>> close Dialog', event)
        event.accept()

    def form_close(self):
        """ Close-Methode """
        self.close()



class FormImage(QMainWindow):
    """ cover/bookled-viewer """
    def __init__(self, image, parent=None):
        """ Image Viewer
        image:  image-list (path + image-name)
        """
        #super(FormImage, self).__init__(parent)
        super().__init__(parent)
        self.ui = Ui_FormImage() # Create an instance of the GUI
        self.ui.setupUi(self) # Run the .setupUi() method to show the GUI
        #--- Connect Widgets ---
        self.zoom = 0
        self.index = 0
        self.image = image
        self.h_zoom = self.ui.graphicsView.height()
        self.w_zoom = self.ui.graphicsView.width()
        self.image_show(image[0])
        self.ui.pushButtonExit.clicked.connect(self.close)
        self.ui.pushButtonBack.clicked.connect(lambda: self.image_pager(False))#self.path1))
        self.ui.pushButtonNext.clicked.connect(lambda: self.image_pager(True))#self.path2))
        self.ui.pushButtonZoomN.clicked.connect(lambda: self.image_zoom(False))
        self.ui.pushButtonZoomP.clicked.connect(lambda: self.image_zoom(True))

    def closeEvent(self, event):
        """ Close-Event """
        print('>>> close Image', event)
        event.accept()

    def image_pager(self, page=True):
        """ browse through the pictures """
        len_ = len(self.image)
        if page is True:
            self.index += 1
        else:
            self.index -= 1
        self.index = min(self.index, len_-1)
        self.index = max(self.index, 0)
        self.image_show(self.image[self.index])

    def image_zoom(self, mode=True, step=5, zoom=100):
        """ zoom in to the pictures """
        height = self.ui.graphicsView.height()
        width = self.ui.graphicsView.width()
        if mode is True:
            self.h_zoom = self.h_zoom + zoom
            self.h_zoom = min(self.h_zoom, (height * step))
            self.w_zoom = self.w_zoom + zoom
            self.w_zoom = min(self.w_zoom, (width * step))
        else:
            self.h_zoom = self.h_zoom - zoom
            self.h_zoom = max(self.h_zoom, height)
            self.w_zoom = self.w_zoom - zoom
            self.w_zoom = max(self.w_zoom, width)
        self.image_show()

    def image_show(self, file=None):
        """ show the image
        file:   path + imagename
        """
        if file is not None:
            self.image_file = file
        if os.path.isfile(self.image_file):
            scene = QtWidgets.QGraphicsScene(self)
            pixmap = QPixmap(self.image_file)
            pixmap = pixmap.scaled(self.w_zoom, self.h_zoom,\
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene.addItem(item)
            self.ui.graphicsView.setScene(scene)


class GuiPlayer(QMainWindow):#, QDialog):#, Ui_MainWindow):
    """ GUI Input/Output for audioplayer """
    def __init__(self, parent=None):
        """ init GUI for QMainWindows
        data:   data-struct for app
        """
        #super(GuiPlayer, self).__init__(parent)
        super().__init__()
        self.img = None
        self.flag_undo = False
        #--- Init UI-MainWindow ---
        self.ui = Ui_MainWindow()# Init UI-MainWindow
        self.ui.setupUi(self)# INIT all widgets
        self.hmi = HmiPlay([self.on_end, self.on_pos,None]) #- remote plaxer & list (TCPIP)
        self.hmi.config_wgt(self.ui.listWidget, self.ui.progressBar, self.ui.labelAlbum,\
            self.ui.labelTitel, self.ui.labelStatus, self.ui.graphicsView)
        #--- Connect Widgets ---
        self.ui.pushButtonCD.clicked.connect(self.pb_cd)
        self.ui.pushButtonTrack.clicked.connect(self.pb_track)
        self.ui.pushButtonPlay.clicked.connect(self.pb_play)
        self.ui.pushButtonPause.clicked.connect(self.pb_pause)
        self.ui.pushButtonSearch.clicked.connect(self.pb_search)
        self.ui.pushButtonUp.clicked.connect(self.pb_up)
        self.ui.pushButtonDown.clicked.connect(self.pb_down)
        self.ui.pushButtonImage.clicked.connect(self.pb_image)
        self.ui.pushButtonBack.clicked.connect(self.pb_back)
        self.ui.pushButtonNext.clicked.connect(self.pb_next)
        self.ui.pushButtonUndo.clicked.connect(self.pb_undo)
        self.ui.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.listWidget.clicked.connect(self.lw_change)
        self.ui.listWidget.doubleClicked.connect(self.pb_play)
        self.ui.listWidget.setStyleSheet(self.hmi.style['titelAktiv'])

    def closeEvent(self, event):
        """ Event window close """
        self.hmi.auto = False
        self.hmi.stop()
        event.accept()

    def mousePressEvent(self, event):
        """ Event pressbutton mouse """
        self.hmi.bar_focus(event)
        self.hmi.clicked(event, self.ui.graphicsView, self.pb_image)
        self.hmi.clicked(event, self.ui.labelAlbum, self.pb_cd)
        self.hmi.clicked(event, self.ui.labelTitel, self.pb_track)

    def on_end(self):
        """ call at end of titel """
        self.hmi.end_run()

    def on_pos(self):
        """ call at position-change """
        self.hmi.bar_set()

    def lw_change(self):
        """ set titel if list change """
        self.hmi.list_ctrl('set')
        self.hmi.list_ctrl('load')
        self.hmi.show_infos()
        self.hmi.label_face(face='titel')

    def pb_down(self):
        """ browae down to the titel-list """
        self.hmi.list_ctrl('up')
        self.hmi.list_ctrl('set')
        self.hmi.show_infos()

    def pb_up(self):
        """ browae up to the titel-list """
        self.hmi.list_ctrl('down')
        self.hmi.list_ctrl('set')
        self.hmi.show_infos()

    def pb_undo(self):
        """ change to play /search -list """
        print('>>>> pb_undo', self.flag_undo)
        if self.flag_undo is True:
            self.flag_undo = False
            self.ui.pushButtonUndo.setText('a')
            self.hmi.list_switch('play')
        else:
            self.flag_undo = True
            self.ui.pushButtonUndo.setText('b')
            self.hmi.list_switch('search')

    def pb_back(self):
        """ play last titel in list """
        self.hmi.list_ctrl('back')
        self.hmi.start_play()

    def pb_next(self):
        """ play next titel in list """
        self.hmi.list_ctrl('next')
        self.hmi.start_play()

    def pb_play(self):
        """ start player/unpause """
        state = self.hmi.get_state()
        self.hmi.start_play()
        if state == 2:
            self.ui.pushButtonPause.setStyleSheet(self.hmi.style['buttonOff'])
        self.hmi.list_autoplay(True)

    def pb_pause(self):
        """ player pause """
        state = self.hmi.pause()
        if state == 2:
            self.ui.pushButtonPause.setStyleSheet(self.hmi.style['buttonOff'])
        else:
            self.ui.pushButtonPause.setStyleSheet(self.hmi.style['buttonOn'])

    def pb_cd(self):
        """ browse to CDs """
        self.hmi.vuw_cd.config()
        self.hmi.list_ctrl('set')
        self.hmi.show_infos()
        self.hmi.label_face(face='cd')

    def pb_track(self):
        """ browse to Titel """
        self.hmi.vuw_titel.config()
        self.hmi.list_ctrl('set')
        self.hmi.list_ctrl('load')
        self.hmi.show_infos()
        self.hmi.label_face(face='titel')

    def pb_search(self):
        """ search CD / Titel """
        # dlg = DlgKeyboard()
        # dlg.exec()
        self.hmi.list_build(['interpret', '', 'interpret', False])
        self.hmi.list_save('search')
        self.hmi.list_autoplay(False)

    def pb_image(self):
        """ start image-viewer """
        image_list = self.hmi.find_get('image')
        self.img = FormImage(image_list)
        self.img.show()

    def set_status(self, text):
        """ set descripten from image
        text:       description / text
        highlite:   highliting label
        """
        self.ui.labelStatus.setText(text)


# =================== Modul Test =======================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GuiPlayer()#DirectPlay._)
    gui.show()
    sys.exit(app.exec_())
