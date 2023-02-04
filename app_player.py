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
from diag_rds_find_V1 import Ui_DialogRdsFind
from diag_keyboard_V0 import Ui_Keyboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtGui import QPixmap
import logging
import urllib
import webbrowser
from xml.sax import make_parser, handler

#--- File logger ---
logging.basicConfig (filename='report.log', filemode='a',\
     level=logging.INFO, format='%(asctime)-15s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
def printlog(name, error=None):
    """ basic-logging error - typ OK, ERR(or), SYS(tem)
    name = error - typ
    error= description of error --> if none, no logging-save
    """
    text ='[ ' + str(name) + ' ]: '
    if error is not None:
        text += str(error)
        logging.info(text)
    print(text)


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

    def get_input(self):
        """ get keyboard-input """
        return self.ui.leIn_text.text()


class XmlRdsFind(handler.ContentHandler):
    """ check radiostations from xml-file """
    def __init__(self, init):
        """ init XmlRdsFind
        init =  load init.data
        """
        self._search = init['init']['search']
        self._max_count = init['init']['base']['count']
        self._rds_count = 0
        self._rds_nr = 0
        self._rds_data = []

    def startElement(self, name, attrs):
        """ callback from SAX
        name =      Tag-name ( <name>...</name> )
        attrs =     Atribute-Dictonary (< name attrs="xxx" >)
        """
        if name == 'station':
            self._rds_nr += 1
            data = self.search_attrs(attrs)
            #--- founded station ---
            if data is not False:
                self._rds_count += 1
                #--- check range of results ---
                if self._rds_count <= self._max_count:
                    # print('---- XML-Tags: ', name + ' Nr.' + str(self._rds_nr) + ' ----')
                    # print(data)
                    # print('\n')
                    self._rds_data.append(data)

    def search_attrs(self, attrs):
        """ search in SAX-Atribute
        attrs =     Atribute-Dictonary (< name attrs="xxx" >)
        return =    Data = finded, False = Not finded
        """
        state = True
        value = ''
        for key in self._search:
            if key in attrs:
                #--- search the values ---
                value = str(attrs[key])
                if self._search[key] != '???': #- search enable
                    #--- search bitrate as numb ---
                    if key == 'bitrate':
                        if  int(value) < int(self._search[key]):
                            state = False
                            break
                    #--- search keyword exit ---
                    else:
                        value = value.lower()
                        if value.find(self._search[key].lower()) < 0: #- not find
                            #print('  *'+ key + ':', value)
                            state = False
                            break
        #--- build RDS-Data ---
        if state is True:
            state = {
                'name': str(attrs['name']),
                'genre': str(attrs['tags']),
                'url': str(attrs['url_resolved']),
                #'url': str(attrs['url']),
                'image': str(attrs['favicon']),
                'web': str(attrs['homepage']),
                'codec': str(attrs['codec']) + ':' +  str(attrs['bitrate']),
                'playtime': 0.0
            }
        return state

    def get_find(self):
        """ get found stations
        """
        return self._rds_data

class DialogRdsFind(QDialog):
    """ search internet radio-station """
    def __init__(self, init, parent=None):
        """ Init
        """
        super().__init__(parent)
        self.ui = Ui_DialogRdsFind() # Create an instance of the GUI
        self.ui.setupUi(self) # Run the .setupUi() method to show the GUI
        self.ui.pushButtonExit.clicked.connect(self.close)
        self.ui.pushButtonOk.clicked.connect(self.show_search)
        self.ui.pushButtonUpdate.clicked.connect(self.update)
        self.ui.pushButtonName.clicked.connect(self.keyboard)
        self._init = init
        self._search = init.data['init']
        #--- load last init ---
        self.ui.comboBoxLand.setCurrentText(self._search['search']['country'])
        self.ui.comboBoxGenre.setCurrentText(self._search['search']['tags'])
        self.ui.comboBoxCodec.setCurrentText(self._search['search']['codec'])
        self.ui.comboBoxRate.setCurrentText(self._search['search']['bitrate'])
        self.ui.pushButtonName.setText(self._search['search']['name'])
        self.ui.comboBoxBase.clear()
        self.ui.comboBoxBase.addItems(self._search['base']['server'])
        #json_show(self._init.data)
        
    def closeEvent(self, event):
        """ Close-Event """
        event.accept()

    def show_search(self):
        """ show radiostation """
        self._search['search']['country'] = self.ui.comboBoxLand.currentText()
        self._search['search']['tags'] = self.ui.comboBoxGenre.currentText()
        self._search['search']['codec'] = self.ui.comboBoxCodec.currentText()
        self._search['search']['bitrate'] = self.ui.comboBoxRate.currentText()
        self._search['search']['name'] = self.ui.pushButtonName.text()
        self._search['base']['current'] = self.ui.comboBoxBase.currentText()
        self.ui.labelResult.setText('......Suche: bitte warten')
        QtWidgets.QApplication.processEvents()
        self.rds = XmlRdsFind(self._init.data)
        self.parser = make_parser()
        self.parser.setContentHandler(self.rds)
        self.parser.parse(self._init.data['init']['base']['file'])
        self._init.data['station'] = self.rds.get_find()
        self.ui.labelResult.setText('Gefunden: ' + str(self.rds._rds_count) + \
            ' von ' + str(self.rds._rds_nr) + ' Stationen')
        del self.rds
        del self.parser

    def update(self):
        """ update radio-Station-database """
        url = self.ui.comboBoxBase.currentText()
        self.ui.labelResult.setText(url + '\n......Update: bitte warten')
        QtWidgets.QApplication.processEvents()
        base = urllib.request.urlopen(url)#- url anfordern
        data = base.read() #- serial url lesen
        #--- save  as binaer-file 
        with open(self._init.data['init']['base']['file'], 'wb') as f:
            f.write(data)
        self.ui.labelResult.setText(url + '\n>>>> Update: erfolgreich <<<<')

    def keyboard(self):
        """ update radio-Station-database """
        board = DlgKeyboard('')
        board.exec()
        name = board.get_input()
        if name == '':
            name = '???'
        del board
        self.ui.pushButtonName.setText(name)


class DialogRds(QDialog):
    """ play internet radio-station """
    def __init__(self, parent=None):
        """ Init
        """
        super().__init__(parent)
        self.ui = Ui_DialogRds() # Create an instance of the GUI
        self.ui.setupUi(self) # Run the .setupUi() method to show the GUI
        self.ui.pushButtonExit.clicked.connect(self.close)
        self.ui.pushButtonUp.clicked.connect(self.up)
        self.ui.pushButtonDown.clicked.connect(self.down)
        self.ui.listWidgetRds.clicked.connect(self.play)
        self.ui.pushButtonDel.clicked.connect(self.del_mode)
        self.ui.pushButtonRec.clicked.connect(self.record_play)
        self.ui.pushButtonMode.clicked.connect(self.change_mode)
        self.ui.pushButtonFind.clicked.connect(self.show_find)
        self.ui.pushButtonEnd.clicked.connect(self.close_find)
        self.ui.pushButtonSave.clicked.connect(self.save_find)
        self.ui.graficesViewPlay.mousePressEvent = lambda event: self.show_web(event)
        self.ui.pushButtonEnd.setHidden(True)
        self.ui.pushButtonSave.setHidden(True)
        self._init = JsonData('RdsPlay.ini')
        #--- self.ctrl:enable=mode 'rds'or'rec', titel=record-Name, tick=secend-Tick,
        #---           time=record-start-time, rec=stop/start/play, rds_time=playtime of rds
        self.ctrl = {'enable': 'rds', 'titel': "", 'tick': -1, 'time': 0, 'rec': 'stop', 'rds_time': [0,0.0], 'find': False}
        self.data = ['url', 'name', 'genre', 'interpret', 'titel', 'info','time']
        self.player = VlcPlayer([None, self.call_pos, None])
        self.sort_rds()
        self.show_rds()
        #json_show(self._init.data)
        
    def closeEvent(self, event):
        """ Close-Event """
        self.player.stop()
        self.rds_time('save')
        event.accept()

    def show_web(self, event):
        """ show the web-site """
        if self.ctrl['enable'] == 'rds': #- show infos
            text = '********** Internetseite aufrufen ??? **********'
            text += '[ URL:   ]\n ' + self._init.data['station'][self.ui.listWidgetRds.currentRow()]['url']
            text +='\n[ Name:  ]\n ' + self._init.data['station'][self.ui.listWidgetRds.currentRow()]['name']
            text +='\n[ Genre: ]\n ' + self._init.data['station'][self.ui.listWidgetRds.currentRow()]['genre']
            text +='\n[ Web:   ]\n ' + self._init.data['station'][self.ui.listWidgetRds.currentRow()]['web']
            text +='\n[ Codec: ]\n ' + self._init.data['station'][self.ui.listWidgetRds.currentRow()]['codec']
            if len(self.data[5]) > 1:
                text +='\n[ Infos: ]\n' + self.data[5]
            if show_msg(text, 'Infos Internet-Radio & Webseite') == 'yes':
                webbrowser.open_new(self._init.data['station'][self.ui.listWidgetRds.currentRow()]['web'])

    def del_mode(self):
        """ mode "rds" = del item, mode "rec" del item """
        if self.ctrl['enable'] == 'rds': #- del item from station-list
            if show_msg('Radio-Station wirklich löschen ?', 'Lösche Radio-Station') == 'yes':
                self.player.stop()
                self.recorder('end')
                del self._init.data['station'][self.ui.listWidgetRds.currentRow()]
                self._init.save()
                self.show_rds()
        if self.ctrl['enable'] == 'rec': #- del item from reclist
            if show_msg('Record-Sample wirklich löschen ?', 'Lösche Record-Sample') == 'yes':
                self.recorder('end')
                del self._init.data['record'][self.ui.listWidgetRds.currentRow()]
                try:
                    path_file = self._init.data['init']['path_rec'] + '/' + self.ctrl['titel'] + '.mpg'
                    os.remove(path_file)
                except OSError as e:
                    show_msg('Sample-Datei Fehler:\n"' + str(e) , 'Lösche Record-Sample')
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

    def show_find(self):
        """ show search-window """
        self.player.stop()
        self.ctrl['find'] = True
        self.ui.pushButtonEnd.setHidden(False)
        self.ui.pushButtonSave.setHidden(False)
        find = DialogRdsFind(self._init)
        find.exec()
        del find
        self.show_rds()

    def show_info(self, stream=None):
        """ show browser-infos
        stream = stream-data[6] = Time, stream-data[6] = unknow info
        """
        if stream is not None:
            text = '[Time]: ' + stream[6] + stream[5] # + '\n'
            #--- add browser-info ---
            text += '[Name]: ' + self._init.data['station'][self.ui.listWidgetRds.currentRow()]['name'] + '\n'
            text += '[Genre]:' + self._init.data['station'][self.ui.listWidgetRds.currentRow()]['genre'] + '\n'
            text += '[Codec]:' + self._init.data['station'][self.ui.listWidgetRds.currentRow()]['codec'] + '\n'
            text += '[Home]: ' + self._init.data['station'][self.ui.listWidgetRds.currentRow()]['web'] + '\n'
        else:
            text = self._init.data['record'][self.ui.listWidgetRds.currentRow()]['time'] + '\n'
            #--- add browser-info ---
            text += '[RDS]:  ' + self._init.data['record'][self.ui.listWidgetRds.currentRow()]['rds'] + '\n'
            text += '[INTP]: ' + self._init.data['record'][self.ui.listWidgetRds.currentRow()]['interpret'] + '\n'
            text += '[TRACK]:' + self._init.data['record'][self.ui.listWidgetRds.currentRow()]['titel'] + '\n'
            text += '[INFO]: ' + self._init.data['record'][self.ui.listWidgetRds.currentRow()]['info'] + '\n'
            text += '[SAMPLE]:' + self._init.data['record'][self.ui.listWidgetRds.currentRow()]['sample'] + '\n'
        self.ui.labelInfo.setText(text)
        

    def sort_rds(self):
        """ sort RDS-Station after playtime """
        sortlist = []
        sortdata = []
        #--- list sorted after playtime ---
        for count, data in enumerate(self._init.data['station']):
            sortlist.append([data['playtime'], count])
        sortlist.sort(reverse=True)
        for index in sortlist:
            sortdata.append(self._init.data['station'][index[1]])
        self._init.data['station'] = sortdata

    def show_record(self):
        """ show record-List """
        self.ui.listWidgetRds.clear()
        for item in self._init.data['record']:
            item = item['interpret'] + ': \n -"' + item['titel'] + '"'
            self.ui.listWidgetRds.addItem(item)
        self.ui.listWidgetRds.setCurrentRow(0)

    def change_mode(self):
        """ change between Radio-Station
            - Webdings: »(RDS), ¤(Sample), s(Info), @(Bearbeiten), 4(play), =(record)
                <(stop)
        """
        self.info_clear()
        if self.ctrl['enable'] == 'rds':#-switch to record-sample
            self.ctrl['enable'] = 'rec'
            if self.ctrl['rec'] == 'start':
                self.recorder('stop')
            self.ui.pushButtonRec.setText('4')
            self.ui.pushButtonMode.setText('»')
            self.ui.graficesViewPlay.setHidden(True)
            self.show_record()
        else:
            if self.ctrl['enable'] == 'rec':#- switch to radio-station
                self.ctrl['enable'] = 'rds'
                if self.ctrl['rec'] == 'play':
                    self.recorder('end')
                self.ui.pushButtonRec.setText('=')
                self.ui.pushButtonMode.setText('¤')
                self.ui.graficesViewPlay.setHidden(False)
                self.show_rds()
            else:
                self.ctrl['enable'] == 'rds'
                printlog('ERR unknow mode', self.ctrl['enable'])
                raise

    def close_find(self):
        """ close RDS-Finder 
        """
        self.ctrl['enable'] = 'rds'
        self.ctrl['find'] = False
        self.ui.pushButtonEnd.setHidden(True) #setEnabled(True)
        self.ui.pushButtonSave.setHidden(True)
        self._init = JsonData('RdsPlay.ini')
        self.show_rds()

    def save_find(self):
        """ save station to Favorite 
        """
        data = {
            'name': self._init.data['station'][self.ui.listWidgetRds.currentRow()]['name'],
            'genre': self._init.data['station'][self.ui.listWidgetRds.currentRow()]['genre'],
            'url': self._init.data['station'][self.ui.listWidgetRds.currentRow()]['url'],
            #'url': str(attrs['url']),
            'image': self._init.data['station'][self.ui.listWidgetRds.currentRow()]['image'],
            'web': self._init.data['station'][self.ui.listWidgetRds.currentRow()]['web'],
            'codec': self._init.data['station'][self.ui.listWidgetRds.currentRow()]['codec'],
            'playtime': 0.0
        }
        self.close_find()
        self._init.data['station'].append(data)
        self._init.save()
        self.show_rds()

    def record_play(self):
        """ add a new Record-Sample Item / play the record-sample """
        if self.ctrl['enable'] == 'rds':#-in rds mode
            date = time.localtime()
            date = str(date[2]).rjust(2,'0') + '.' + str(date[1]).rjust(2,'0') +\
                   '.' + str(date[0]) + ' ' +  str(date[3]).rjust(2,'0') +\
                   ':' + str(date[4]).rjust(2,'0')
            item = {"time": date,
                    "rds": self._init.data['station'][self.ui.listWidgetRds.currentRow()]['name'],
             	    "interpret": self.data[3],
    	 	        "titel": self.data[4], 
                    "info": self._init.data['station'][self.ui.listWidgetRds.currentRow()]['genre'],
                    "sample": self.ctrl['titel'] }
            if self.ctrl['rec'] == 'stop':
                self._init.data['record'].append(item)
                self.recorder('start')
            else:
                self.recorder('stop')
            self._init.save()
        if self.ctrl['enable'] == 'rec':#-in play sample record mode
            if self.ctrl['rec'] != 'play':
                self.recorder('play')
            else:
                self.recorder('end')

    def call_pos(self):
        """ read Radio-Station infos all 1xsec"""
        position = self.player.get_pos()
        time = divmod(position/1000, 60)
        #---  second - tick ---
        if int(time[1]) != self.ctrl['tick']:
            if self.ctrl['rec'] != 'play':
                self.rds_time('rds', self.ui.listWidgetRds.currentRow())
                self.ctrl['tick'] = int(time[1])
                std = divmod(time[0], 60)
                std_float = std[0] + (1/60*std[1])
                self.rds_time('time', std_float)
                std_str = "{:.2f}".format(std_float) + ' + ' + \
                    "{:.2f}".format(self._init.data['station'][self.ui.listWidgetRds.currentRow()]['playtime']) + ' Std\n'
                self.data = self.player.get_info()
                self.data.append(std_str)
                self.show_info(self.data)
                name = ''.join(char for char in self.data[3] if char.isalnum())
                name = name + '_' + ''.join(char for char in self.data[4] if char.isalnum())
                #--- max record-time ---
                if self.ctrl['rec'] == 'start':
                    if (time[0] - self.ctrl['time']) > self._init.data['init']['time_rec']:
                        self.recorder('stop')
                #--- changed interpred / titel ---
                if name != self.ctrl['titel']:
                    self.ctrl['titel'] = name
                    self.recorder('stop')
                    printlog('OK', 'Interpret / Titel changed: ' + name)
                    self.ui.labelStation.setText(self.data[1])
                    self.ui.labelGenre.setText(self.data[2])
                    self.ui.labelInterpret.setText(self.data[3])
                    self.ui.labelTitel.setText(self.data[4])

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
        if self.ctrl['enable'] == 'rds':
            current_rds = self.ui.listWidgetRds.currentRow()
            station = self._init.data['station'][current_rds]['url']
            self.rds_time('save')
            try:
                self.player.play(station)
            except Exception as err:
                printlog('ERR play-url', err)
                self.player.stop()
            try:
                self.image_webshow(self._init.data['station'][current_rds]['image'])
            except Exception as err:
                printlog('ERR web-image', err)
                self.image_webshow(None, self._init.data['init']['image'])
        #--- aktivate Recorde-Samples ---
        if self.ctrl['enable'] == 'rec':
            self.recorder('end')
            self.ui.labelStation.setText(self._init.data['record']\
                [self.ui.listWidgetRds.currentRow()]['rds'])
            self.ui.labelGenre.setText('---')
            interpret = self._init.data['record'][self.ui.listWidgetRds.currentRow()]['interpret']
            self.ui.labelInterpret.setText(interpret)
            titel = self._init.data['record'][self.ui.listWidgetRds.currentRow()]['titel']
            self.ui.labelTitel.setText(titel)
            self.show_info()
            name = ''.join(char for char in interpret if char.isalnum())
            name = name + '_' + ''.join(char for char in titel if char.isalnum())
            self.ctrl['titel'] = name

    def info_clear(self):
        """ clear info section """
        self.player.stop()
        self.ui.labelStation.setText('---')
        self.ui.labelGenre.setText('---')
        self.ui.labelInterpret.setText('---')
        self.ui.labelTitel.setText('---')
        self.ui.labelInfo.setText('---')

    def image_webshow(self, url, err=None):
        """ show the image from web
        url:   url-adress, None = err-image
        err:   error-image
        """
        scene = QtWidgets.QGraphicsScene(self)
        if url is not None: #- load web image
            data = urllib.request.urlopen(url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
        else: #- load error-image
            pixmap = QPixmap(err)
            #pixmap.loadFromData(err)
        #--- scale image ---
        pixmap = pixmap.scaled(self.ui.graficesViewPlay.height(), self.ui.graficesViewPlay.width(), \
                QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        self.ui.graficesViewPlay.setScene(scene)

    def rds_time(self, mode, val = 0):
        """ handle the radio-station playtime
        mode:  - rds = set radio-station nr
               - time = set current playtime
               - save = save playtime in *.ini
        """
        if mode == 'save':
            #--- save playtime for last station ---
            last_rds = self.ctrl['rds_time'][0]
            last_time = self.ctrl['rds_time'][1]
            if last_time > 0:
                self._init.data['station'][last_rds]['playtime'] = self._init.data['station'][last_rds]['playtime'] + last_time
                if self.ctrl['find'] is False:
                    self._init.save()
        if mode == 'rds':
            self.ctrl['rds_time'][0] = val
        if mode == 'time':
            self.ctrl['rds_time'][1] = val

    def recorder(self, mode):
        """ control recorder 
        mode:   - play  = play record-sample
                - end   = play end
                - start = start recording
                - stop  = stop recording
        Webdings: »(RDS), ¤(Sample), s(Info), @(Bearbeiten), 4(play), =(record), <(stop)
        """
        path_file = self._init.data['init']['path_rec'] + '/' + self.ctrl['titel']
        if mode == 'stop':
            self.player.record_stop()
            self.ui.pushButtonRec.setStyleSheet('color : black')
            self.ui.pushButtonRec.setText('=')
            self.ui.labelRec.setStyleSheet('color : black')
            self.ui.labelRec.setText('')
            self.ctrl['rec'] = 'stop'
        if mode == 'start':
            self.player.record_start(path_file)
            self.ui.pushButtonRec.setStyleSheet('color : red')
            self.ui.pushButtonRec.setText('<')
            self.ui.labelRec.setStyleSheet('color : red')
            self.ui.labelRec.setText('Aufnahme\n läuft !!')
            self.ctrl['rec'] = 'start'
        if mode == 'play':
            self.player.play(path_file + '.mpg')
            self.ui.pushButtonRec.setText('<')
            self.ctrl['rec'] = 'play'
        if mode == 'end':
            self.player.stop()
            self.ui.pushButtonRec.setText('4')
            self.ctrl['rec'] = 'end'


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
        rds = DialogRds()
        #rds = DialogRdsFind()
        # try:
        #     rds = DialogRds()
        # except Exception as e:
        #     show_msg('Fehler in RdsPlay.ini:\n- Datei fehlt ?\n- Falsches Format ?'\
        #              '\n<< PYTHON ERROR:>>\n' + str(e), 'RadioStation Player')
        rds.exec()
        del rds

    def pb_search(self):
        """ search CD / Titel """
        board = DlgKeyboard('suche?')
        board.exec()
        text = board.get_input()
        del board
        self.hmi.list_build(['interpret', '', 'interpret', False])
        self.hmi.list_save('search')
        self.hmi.list_autoplay(False)

    def pb_image(self):
        """ start image-viewer """
        image_list = self.hmi.find_get('image')
        img = DialogImage(image_list)
        img.exec()
        del img

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
