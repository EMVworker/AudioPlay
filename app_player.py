# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:26:36 2022

@author: juergen
"""
import sys
sys.path.insert(0,'D:/Projekte/PyAudioPlay/AudioPlay_V0/')
from ctrl_player import HmiPlay #- import class
from ctrl_player import show_msg #- import function
import os
import time
from json_data import JsonData
from json_data import json_show
from vlc_player import VlcPlayer
sys.path.insert(0,'D:/Projekte/PyAudioPlay/AudioPlay_V0/')
from gui_player_V1 import Ui_MainWindow
from form_image_V1 import Ui_DialogImage
from diag_rds_V1 import Ui_DialogRds
from diag_keyboard_V0 import Ui_Keyboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtGui import QPixmap


class DlgKeyboard(QDialog):
    """ Dialog Keyboard """
    def __init__(self, text='', parent=None):
        # super(DlgKeyboard, self).__init__(parent)
        super().__init__(parent)
        self.ui = Ui_Keyboard() # Create an instance of the GUI
        self.ui.setupUi(self) # Run the .setupUi() method to show the GUI
        #--- Variable ---
        self.key_flag = 1
        self.charc = {'small':['a','b','c','d','e','f','g','h','i','j','k','l','m',\
                   'n','o','p','q','r','s','t','u','v','w','x','y','z','ä','ö','ü'],
                 'big':['A','B','C','D','E','F','G','H','I','J','K','L','M',\
                   'N','O','P','Q','R','S','T','U','V','W','X','Y','Z','Ä','Ö','Ü'],
                 'num':['1','2','3','4','5','6','7','8','9','0','ß','!','"',\
                   '§','$','%','/','(',')','=','?','+','-','*','/','_','#','.',',']
                 }
        #--- Connect Widgets ---
        self.ui.leIn_text.setText(text)
        self.ui.pbKey_cr.clicked.connect(self.form_close)
        self.ui.pbKey_num.clicked.connect(lambda:self.change_chr('keys'))
        self.ui.pbKey_clear.clicked.connect(lambda:self.ui.leIn_text.setText(''))
        self.ui.pbKey_del.clicked.connect(self.clear_chr)
        self.ui.pbKey_a.clicked.connect(lambda:self.add_chr(self.key_list[0]))
        self.ui.pbKey_b.clicked.connect(lambda:self.add_chr(self.key_list[1]))
        self.ui.pbKey_c.clicked.connect(lambda:self.add_chr(self.key_list[2]))
        self.ui.pbKey_d.clicked.connect(lambda:self.add_chr(self.key_list[3]))
        self.ui.pbKey_e.clicked.connect(lambda:self.add_chr(self.key_list[4]))
        self.ui.pbKey_f.clicked.connect(lambda:self.add_chr(self.key_list[5]))
        self.ui.pbKey_g.clicked.connect(lambda:self.add_chr(self.key_list[6]))
        self.ui.pbKey_h.clicked.connect(lambda:self.add_chr(self.key_list[7]))
        self.ui.pbKey_i.clicked.connect(lambda:self.add_chr(self.key_list[8]))
        self.ui.pbKey_j.clicked.connect(lambda:self.add_chr(self.key_list[9]))
        self.ui.pbKey_k.clicked.connect(lambda:self.add_chr(self.key_list[10]))
        self.ui.pbKey_l.clicked.connect(lambda:self.add_chr(self.key_list[11]))
        self.ui.pbKey_m.clicked.connect(lambda:self.add_chr(self.key_list[12]))
        self.ui.pbKey_n.clicked.connect(lambda:self.add_chr(self.key_list[13]))
        self.ui.pbKey_o.clicked.connect(lambda:self.add_chr(self.key_list[14]))
        self.ui.pbKey_p.clicked.connect(lambda:self.add_chr(self.key_list[15]))
        self.ui.pbKey_q.clicked.connect(lambda:self.add_chr(self.key_list[16]))
        self.ui.pbKey_r.clicked.connect(lambda:self.add_chr(self.key_list[17]))
        self.ui.pbKey_s.clicked.connect(lambda:self.add_chr(self.key_list[18]))
        self.ui.pbKey_t.clicked.connect(lambda:self.add_chr(self.key_list[19]))
        self.ui.pbKey_u.clicked.connect(lambda:self.add_chr(self.key_list[20]))
        self.ui.pbKey_v.clicked.connect(lambda:self.add_chr(self.key_list[21]))
        self.ui.pbKey_w.clicked.connect(lambda:self.add_chr(self.key_list[22]))
        self.ui.pbKey_x.clicked.connect(lambda:self.add_chr(self.key_list[23]))
        self.ui.pbKey_y.clicked.connect(lambda:self.add_chr(self.key_list[24]))
        self.ui.pbKey_z.clicked.connect(lambda:self.add_chr(self.key_list[25]))
        self.ui.pbKey_ae.clicked.connect(lambda:self.add_chr(self.key_list[26]))
        self.ui.pbKey_oe.clicked.connect(lambda:self.add_chr(self.key_list[27]))
        self.ui.pbKey_ue.clicked.connect(lambda:self.add_chr(self.key_list[28]))
        self.ui.pbKey_sp.clicked.connect(lambda:self.add_chr(None, ' '))
        #--- List-Objekt ---
        self.key_list = [
            self.ui.pbKey_a, self.ui.pbKey_b, self.ui.pbKey_c, self.ui.pbKey_d, self.ui.pbKey_e, self.ui.pbKey_f,
            self.ui.pbKey_g, self.ui.pbKey_h, self.ui.pbKey_i, self.ui.pbKey_j, self.ui.pbKey_k, self.ui.pbKey_l,
            self.ui.pbKey_m, self.ui.pbKey_n, self.ui.pbKey_o, self.ui.pbKey_p, self.ui.pbKey_q, self.ui.pbKey_r,
            self.ui.pbKey_s, self.ui.pbKey_t, self.ui.pbKey_u, self.ui.pbKey_v, self.ui.pbKey_w, self.ui.pbKey_x,
            self.ui.pbKey_y, self.ui.pbKey_z, self.ui.pbKey_ae, self.ui.pbKey_oe, self.ui.pbKey_ue]

    def closeEvent(self, event):
        """ Close-Event """
        print('>>> close Dialog', event)
        event.accept()

    def form_close(self):
        """ Close-Methode """
        self.close()

    def change_chr(self, mode):
        """ change characters of keyboard\n
        mode: change characters betwen text-small, text-big, num/symbol
        """
        if self.key_flag <= 0:
            self.key_flag = 1
            mode = 'small'
        else:
            if self.key_flag == 1:
                self.key_flag = 2
                mode = 'big'
            else:
                if self.key_flag >= 2:
                    self.key_flag = 0
                    mode = 'num'
        for i,key in enumerate(self.key_list):
            key.setText(self.charc[mode][i])

    def clear_chr(self):
        """ delete character from input-text """
        text = self.ui.leIn_text.text()
        text = text[0:len(text)-1]
        self.ui.leIn_text.setText(text)

    def add_chr(self, key, charac=''):
        """ add clicked charactaer to input_text 
        key:    current clicked button-text
        charac: set character (key=None)
        """
        text =  self.ui.leIn_text.text()
        if key is not None:
            text = text + key.text()
        else:
            text = text + charac
        self.ui.leIn_text.setText(text)


class DialogRds(QDialog):
    """ play internet radio-station """
    def __init__(self, parent=None):
        """ Image Viewer
        """
        super().__init__(parent)
        self.ui = Ui_DialogRds() # Create an instance of the GUI
        self.ui.setupUi(self) # Run the .setupUi() method to show the GUI
        self.ui.pushButtonExit.clicked.connect(self.close)
        self.ui.pushButtonUp.clicked.connect(self.up)
        self.ui.pushButtonDown.clicked.connect(self.down)
        self.ui.listWidgetRds.clicked.connect(self.play)
        self.ui.pushButtonDel.clicked.connect(self.del_tools)
        self.ui.pushButtonRec.clicked.connect(self.add_record)
        self.ui.pushButtonMode.clicked.connect(self.change_mode)
        self._init = JsonData('RdsPlay.ini')
        self.rds_nr = 0
        self.time_change = -1
        self.enable = 'rds' #- rds(Internet-Radio) or rec(record)
        self.data = ['url', 'name', 'genre', 'interpret', 'titel', 'info','time']
        self.player = VlcPlayer([None, self.call_pos, None])
        json_show(self._init.data)
        self.show_rds()
        
    def closeEvent(self, event):
        """ Close-Event """
        self.player.stop()
        print('>>> close RDS-Player', event)
        event.accept()

    def del_tools(self):
        """ mode "rds" = show Infos, mode "rec" del item """
        if self.enable == 'rds': #- show infos
            if self.data[5] == '':
                self.data[5] = '"Keine Infos verfügbar"'
            text = '[ URL: ]\n ' + self.data[0] + '\n\n[ Infos: ]\n' + self.data[5]
            show_msg(text, 'Infos Internet-Radio')
        if self.enable == 'rec': #- del item from reclist
            if show_msg('Listen-Eintrag wirklich löschen ?', 'Lösche Listen-Eintrag') == 'yes':
                del self._init.data['record'][self.ui.listWidgetRds.currentRow()]
                self.ui.listWidgetRds.setCurrentRow(0)
                self._init.save()
                self.show_record()
                self.info_clear()

    def show_rds(self):
        """ show radiostation """
        self.ui.listWidgetRds.clear()
        for item in self._init.data['station']:
            item = item['name'] + ' [' + item['genre'] + ']'
            self.ui.listWidgetRds.addItem(item)
        self.ui.listWidgetRds.setCurrentRow(0)

    def show_record(self):
        """ show record-List """
        self.ui.listWidgetRds.clear()
        for item in self._init.data['record']:
            item = item['interpret'] + ': \n -"' + item['titel'] + '"'
            self.ui.listWidgetRds.addItem(item)
        self.ui.listWidgetRds.setCurrentRow(0)

    def change_mode(self):
        """ change between Radio-Station and Record 
            - Webdings: »(RDS), ¤(Sample), s(Info), @(Bearbeiten), 4(play), =(record)
        """
        self.info_clear()
        if self.enable == 'rds':#-switch to record-sample
            self.enable = 'rec'
            self.ui.pushButtonRec.setText('4')
            self.ui.pushButtonMode.setText('»')
            self.ui.pushButtonDel.setText('@')
            self.show_record()
        else:
            if self.enable == 'rec':#- switch to radio-station
                self.enable = 'rds'
                self.ui.pushButtonRec.setText('=')
                self.ui.pushButtonMode.setText('¤')
                self.ui.pushButtonDel.setText('s')
                self.show_rds()
            else:
                self.enable == 'rds'
                print('<ERROR1>:unknow mode: ' + self.enable + '>')
                raise
        print('>>>> RDS: aktiv mode = ', self.enable)

    def add_record(self):
        """ add a new Record-Sample Item """
        if self.enable == 'rds':#-in rds mode
            date = time.localtime()
            date = str(date[2]).rjust(2,'0') + '.' + str(date[1]).rjust(2,'0') +\
                   '.' + str(date[0]) + ' ' +  str(date[3]).rjust(2,'0') +\
                   ':' + str(date[4]).rjust(2,'0')
            item = {"time": date,\
                    "rds": self.data[1],\
             	    "interpret": self.data[3],\
    	 	        "titel": self.data[4] }
            self._init.data['record'].append(item)
            self._init.save()
            self.player.record_start(self.data[3] + '_' + self.data[4])
        if self.enable == 'rec':#-in record mode
            pass

    def call_pos(self):
        """ read Radio-Station infos all 1xsec"""
        position = self.player.get_pos()
        time = divmod(position/1000, 60)
        #---  second - tick ---
        if int(time[1]) != self.time_change:
            self.time_change = int(time[1])
            std = divmod(time[0], 60)
            print ('>>>> rds:Min/Sec', int(time[0]), int(time[1]))
            self.data = self.player.get_info()
            self.data.append("{:.2f}".format(std[0] + (1/60*std[1])))
            self.ui.labelStation.setText(self.data[1])
            self.ui.labelGenre.setText(self.data[2])
            self.ui.labelInterpret.setText(self.data[3])
            self.ui.labelTitel.setText(self.data[4])
            self.ui.labelInfo.setText('Spielzeit(Std):' + self.data[6] + self.data[5])

    def up(self):
        """ Radio-Station previue """
        if self.ui.listWidgetRds.currentRow() - 1 >= 0:
            self.ui.listWidgetRds.setCurrentRow(self.ui.listWidgetRds.currentRow()-1)
            self.play()

    def down(self):
        """ next Radio-Station """
        len_ = self.ui.listWidgetRds.count()
        if self.ui.listWidgetRds.currentRow() + 1 < len_:
            self.ui.listWidgetRds.setCurrentRow(self.ui.listWidgetRds.currentRow()+1)
            self.play()

    def play(self, record = False):
        """ play Radio-Station """
        self.info_clear()
        #--- aktivate Radio-Station ---
        if self.enable == 'rds':
            station = self._init.data['station'][self.ui.listWidgetRds.currentRow()]['http']
            self.player.play(station)
            self.image_show('D:/Projekte/PyAudioPlay/AudioPlay_V0/files/icon1.gif')
        #--- aktivate Recorde-Samples ---
        if self.enable == 'rec':
            self.ui.labelStation.setText(self._init.data['record']\
                [self.ui.listWidgetRds.currentRow()]['rds'])
            self.ui.labelGenre.setText('---')
            self.ui.labelInterpret.setText(self._init.data['record']\
                [self.ui.listWidgetRds.currentRow()]['interpret'])
            self.ui.labelTitel.setText(self._init.data['record']\
                [self.ui.listWidgetRds.currentRow()]['titel'])
            self.ui.labelInfo.setText(self._init.data['record']\
                [self.ui.listWidgetRds.currentRow()]['time'])

    def info_clear(self):
        """ clear info section """
        self.player.stop()
        self.player.record_stop()
        self.ui.labelStation.setText('---')
        self.ui.labelGenre.setText('---')
        self.ui.labelInterpret.setText('---')
        self.ui.labelTitel.setText('---')
        self.ui.labelInfo.setText('---')

    def image_show(self, file):
        """ show the image
        file:   path + imagename
        """
        scene = QtWidgets.QGraphicsScene(self)
        pixmap = QPixmap(file)
        pixmap = pixmap.scaled(self.ui.graficesViewPlay.height(), self.ui.graficesViewPlay.width(), \
                QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        self.ui.graficesViewPlay.setScene(scene)


class DialogImage(QDialog):
    """ cover/bookled-viewer """
    def __init__(self, image, parent=None):
        """ Image Viewer
        image:  image-list (path + image-name)
        """
        #super(FormImage, self).__init__(parent)
        super().__init__(parent)
        self.ui = Ui_DialogImage() # Create an instance of the GUI
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
        self.ui.pushButtonRadio.clicked.connect(self.pb_radio)
        self.ui.pushButtonExit.clicked.connect(self.close)
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

    def pb_radio(self):
        """ search CD / Titel """
        try:
            rds = DialogRds()
        except Exception as e:
            show_msg('Fehler in RdsPlay.ini:\n- Datei fehlt ?\n- Falsches Format ?'\
                     '\n<< PYTHON ERROR:>>\n' + str(e), 'RadioStation Player')
        rds.exec()

    def pb_search(self):
        """ search CD / Titel """
        dlg = DlgKeyboard('suche?')
        dlg.exec()
        self.hmi.list_build(['interpret', '', 'interpret', False])
        self.hmi.list_save('search')
        self.hmi.list_autoplay(False)

    def pb_image(self):
        """ start image-viewer """
        image_list = self.hmi.find_get('image')
        img = DialogImage(image_list)
        img.exec()

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
