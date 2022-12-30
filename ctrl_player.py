# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 21:20:26 2022

@author: juergen
"""
#import sys
#sys.path.insert(0,'D:/Projekte/PyAudioPlay/AudioPlay_V0/')
import glob
import copy
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap
from song_list import SongList
from qt_player import QtPlayer

class DirectPlay():
    """ direct remote player/list for GUI """
    def __init__(self, callback=[None,None,None]):
        """ init QTMediaPlayer & song_list 
        """
        self._db = SongList()#- Listenverwaltung Audioplayer
        self._play = QtPlayer(callback)#- QT5 Audio-Player
        
    def play(self, titel):
        """ start qt-player with file """
        state = self._play.get_state()
        if state == 2:
            self._play.unpause()
        else:
            self._play.play(titel)
        return state

    def stop(self):
        """ stop qt-player """
        self._play.stop()

    def pause(self):
        """ qt-player pause """
        state = self._play.get_state()
        if state == 2:
            self._play.unpause()
        else:
            self._play.pause()
        return state

    def get_time(self):
        """ get player-state 0=stop, 1=play, 2=pause """
        return self._play.get_time()

    def get_state(self):
        """ get playtime from current titel """
        return self._play.get_state()

    def get_pos(self):
        """ get play-position """
        return self._play.get_pos()

    def set_pos(self, position):
        """ set play-position 
        position:   new play-position
        """
        return self._play.set_pos(position)

    def find(self, par=['interpret', '', '', False] ):
        """ greate a playlist with find-results:\n
        - par[0] = search for ( interpret, album, genre, year import)\n
        - par[1] = search value\n
        - par[2] = sort after (interpret, album, genre, year, import, rand)\n
        - par[3] = sort-direction (True = z_a, False = a_z)\n
        return: True or Errors
        """
        state = True
        self._db.list_filter(par[0], par[1])
        if par[2] != '':
            self._db.list_sort(par[2], par[3])
        #print( self._db.list_select('cd') )
        return state

    def find_get(self, mode, par=''):
        """ give titel or interpret/Album:\n
        - mode:\n
            - cd:   all available CDs\n
            - titel:titel from CDs(par=cd-name) or all (par='')\n
            - path: cd-path from cd-Name(par=cd-name)
            - image:list of image from current cd(par='')
        return:\n
        """
        item = []
        state = False
        if mode == 'cd':
            state = self._db.list_select('cd')
            for val in state:
                item.append([val[0], val[1] + '\n - ' + val[2]])
        if mode == 'titel':
            state = self._db.list_select('titel', par)
            for val in state:
                item.append([val[0], val[1]])
        if mode == 'path':
            item = self._db.list_select('path', par)
        if mode == 'image':
            item = self._db.list_select('image', self.vuw_cd.data[self.vuw_cd.row])
        return item

    def info_get(self, track):
        """ give all information from seleceted track\n
        - track:   seleced track (path + titel)\n
        return:return:(cd_path, CD, Interpret, Album, genre, year, import, [track, pos,call])\n
        """
        return self._db.list_select('track',track)


class TcpPlay():
    """ remote player/player trough TCP-IP for GUI """
    pass


#--global Variable: ListData_name
class ListData:
    """ Managed the data for the ListWidget (for Interpreter, Album, Play/RecordList) """
    def __init__(self, list_wgt):
        """ init class with listWidget """
        self.wgt = list_wgt #- list-Widget
        self.row = 0        #- position in list
        self.items = []     #- data in Widget
        self.data = []      #- secend data(z.b path+file /)
        self.current = ''   #- current (aktiv) setting
        self.name = ''      #- list-name

    def config(self, name=None, items=None, row=None):
        """ config List-widget. For first config use name,items,row:\n
        - name:  name of list (cd, titel, rec), None=no setting of itrms,row\n
        - items: list of items in list-widget\n
        - row:  current nr of list\n
        return: None
        """
        global ListData_name
        self.wgt.clear()
        if name is not None:
            self.data.clear()
            self.items.clear()
            self.name = name
            for val in items:
                self.data.append(val[0])
                self.items.append(val[1])
            self.row = row
        self.wgt.addItems(self.items)
        self.wgt.setCurrentRow(self.row)
        self.current = self.data[self.row]
        ListData_name = self.name
        return ListData_name

    def set_par(self, mode, par=None):
        """ config List-widget:\n
        - mode:\n
            - row: set list-nr to the selected value. None=set current pos\n
            - list:set current listname (cd, titel, rec) \n
        - par:\n
        return: setting
        """
        state = False
        if mode == 'row':
            if par is None:
                self.row = self.wgt.currentRow()
            else:
                self.row = par
            self.wgt.setCurrentRow(self.row)
            self.current = self.data[self.row]
            state = self.row
        return state



#--global Variable: ListData_name
class HmiPlay(DirectPlay):
    """ Managed the widgets (list-box, bar, label cd/titel (play, search) 
    - use HmiPlay(...) to init the audioplayer-callbacks "on_end, on_pos, on_media
    - use config_wgt(...) to init the widget listbox, progress-bar, label cd/titel/info
    """
    def __init__(self, callback=[None,None,None]):
        """ init class with list-data """
        super().__init__(callback)
        self.style = {
         'titelAktiv': 'QListView { background-color : lightGray; color : black; }',
         'buttonOn': 'QPushButton { background-color : darkGray; color : blue; }',
         'buttonOff': 'QPushButton { background-color : lightGray; color : black; }',
         'labelOn': 'QLabel { background-color : lightGray; color : black; }',
         'labelOff': 'QLabel { background-color : light; color : black; }'
        }
        self.auto = False
        self.show_change = ''
        self.list_change = ''
        self.list_change_search = False
        self.titel_nr = 0
        self.bar_init = '???'
        #--- widgets ti init (config_wgt(....))
        self.wgt_list = None
        self.wgt_bar = None
        self.wgt_label_cd = None
        self.wgt_labal_titel = None
        self.wgt_labal_info = None
        self.wgt_image = None

    def _in_widget(self, mouse, wgt):
        """ mouse in widget
        wgt:    widget-objekt
        return:     (x_mouse, y_mouse, x_wgt, y_wgt, w_wgt, h_wgt) or False
        """
        state = False
        x_wgt = wgt.x()
        x_mouse = mouse.x()
        if x_mouse >= x_wgt:
            w_wgt = wgt.width()
            if x_mouse <= w_wgt + x_wgt:
                y_mouse = mouse.y()
                y_wgt = wgt.y()
                if y_mouse >= y_wgt:
                    h_wgt = wgt.height()
                    if y_mouse <= h_wgt + y_wgt:
                        state = (x_mouse, y_mouse, x_wgt, y_wgt, w_wgt, h_wgt)
        return state

    def config_wgt(self, listbox, bar, label_cd, label_titel, label_info, image):
        """ init wideget listbox
        listbox:    show titel dd in alist
        bar:        process-bar for played titel
        label_cd:   cd & titel-name
        label_titel:played titel-name
        label_info: info about cd/titel
        image:      image viewer
        """
        self.wgt_list = listbox
        self.wgt_bar = bar
        self.wgt_label_cd = label_cd
        self.wgt_label_titel = label_titel
        self.wgt_label_info = label_info
        self.wgt_image =image
        #--- add cd/titel-lists ---
        self.vuw_cd = ListData(self.wgt_list)
        self.vuw_titel = ListData(self.wgt_list)
        self.play_cd = ListData(self.wgt_list)
        self.play_titel = ListData(self.wgt_list)
        self.search_cd = ListData(self.wgt_list)
        self.search_titel = ListData(self.wgt_list)

    def list_build(self, find_sort=['interpret', '', 'interpret', False]):
        """ load liste from data-base """
        self.find( find_sort )#['interpret', '', 'interpret', False])
        val = self.find_get('cd')
        self.vuw_cd.config('cd',val, 0)
        val = self.find_get('titel', self.vuw_cd.current)
        self.vuw_titel.config('titel', val, 0)

    def list_copy(self, wgt_source, wgt_target):
        """ copy list-object from source to target \n
        - source: source list-objekt\n
        - target: target list-objekt\n
        """
        wgt_target.row = copy.deepcopy(wgt_source.row)
        wgt_target.items = copy.deepcopy(wgt_source.items)
        wgt_target.data = copy.deepcopy(wgt_source.data)
        wgt_target.current = copy.deepcopy(wgt_source.current)
        wgt_target.name = copy.deepcopy(wgt_source.name)

    def list_load(self, mode):
        """ load liste from list-object
        - mode:\n
                - "search" = search-result\n
                - "play" = current playlist\n
        return: None
        """
        if mode == 'search':
            self.list_copy(self.search_cd, self.vuw_cd)
            self.list_copy(self.search_titel, self.vuw_titel)
        if mode == 'play':
            self.list_copy(self.play_cd, self.vuw_cd)
            self.list_copy(self.play_titel, self.vuw_titel)

    def list_save(self, mode):
        """ save liste from list-object
        - mode:\n
                - "search" = search-result\n
                - "play" = current playlist\n
        return: None
        """
        if mode == 'search':
            self.list_copy(self.vuw_cd, self.search_cd )
            self.list_copy(self.vuw_titel, self.search_titel)
        if mode == 'play':
            self.list_copy(self.vuw_cd, self.play_cd )
            self.list_copy(self.vuw_titel, self.play_titel )

    def list_switch(self, name, opt=None):
        """ change current showed-list\n
        - name:   name of list (play = playlist, search = seachr-list)\n
        - opt:    add option for new list (up = next titel)\n
        return:   state of list
        """
        save = ''
        load = ''
        state = None
        if name == 'play':
            save = 'search'
            load = 'play'
        if name == 'search':
            load = 'search'
            save = 'play'
        self.list_save(save)
        self.list_load(load)
        self.vuw_titel.config()
        self.list_ctrl('set')
        if opt == 'up':
            state = self.list_ctrl('up')
        self.show_infos()
        return state

    def list_autoplay(self, enable):
        """ enable autoplay without MessageBox-request:\n"""
        if enable is True:
            self.list_change_search = False
        else:
            self.list_change_search = True

    def list_ctrl(self, mode):
        """ set list-item in widget:\n
        - mode:\n
            - down    = liste down (Titel-1)\n
            - set     = set list position after change\n
            - up      = liste up (Titel+1)\n
            - next    = next titel in playlist\n
            - back    = previues titel in playlist\n
            - load   = load titel from selected cd if changed
        return: True = OK, False = List-End\n
        """
        state = True
        len_ = self.wgt_list.count()
        if mode == 'up':
            self.titel_nr += 1
            if self.titel_nr >= len_:
                state = False
            self.titel_nr = min(self.titel_nr, len_-1)
        if mode == 'down':
            self.titel_nr -= 1
            self.titel_nr = max(self.titel_nr, 0)
        if mode == 'load':
            if self.list_change != self.vuw_cd.current:
                self.list_change = self.vuw_cd.current
                val = self.find_get('titel', self.vuw_cd.current)
                self.vuw_titel.config('titel', val, 0)
                self.titel_nr = 0
        if mode == 'set':
            if ListData_name == 'cd':
                self.titel_nr = self.vuw_cd.set_par('row')
            else:
                if ListData_name == 'titel':
                    self.titel_nr = self.vuw_titel.set_par('row')
        else:
            #--- set list-position ---
            if ListData_name == 'cd':
                self.vuw_cd.set_par('row', self.titel_nr)
            else:
                if ListData_name == 'titel':
                    self.vuw_titel.set_par('row', self.titel_nr)
        if mode == 'back':
            self.titel_nr = self.vuw_titel.row -1
            self.titel_nr = max(self.titel_nr, 0)
            self.vuw_titel.set_par('row', self.titel_nr)
        if mode == 'next':
            self.titel_nr = self.vuw_titel.row +1
            self.titel_nr = min(self.titel_nr, len_-1)
            self.vuw_titel.set_par('row', self.titel_nr)
        return state

    def start_play(self):
        """ start play with current titel and save the playlist """
        self.auto = False
        self.list_save('play')
        self.play(self.vuw_titel.current)
        self.bar_set()
        self.auto = True

    def bar_set(self):
        """ set the prozess-bar """
        pos = self.get_pos()
        if self.vuw_titel.current is not self.bar_init:
            init = self.get_time()
            if init > 0:
                self.wgt_bar.setMinimum(1)
                self.wgt_bar.setMaximum(init)
                self.bar_init = self.vuw_titel.current
        run = divmod(pos/1000, 60)
        total = divmod(self.wgt_bar.maximum()/1000, 60)
        self.wgt_bar.setFormat("{:.0f}".format(run[0]) + ':' + \
            "{:02d}".format(int(run[1])) + 'Min von ' + \
            "{:.0f}".format(total[0]) + ':' +  "{:02d}".format(int(total[1])) + 'Min')
        self.wgt_bar.setValue(pos)

    def bar_focus(self, event):
        """ mouse in bar-focus """
        par = self._in_widget(event, self.wgt_bar)
        if par is not False:
            t_base = self.get_time() / par[4]
            pos = int((par[0] - par[2]) * t_base)
            self.set_pos(pos)
            
    def clicked(self, event, wgt, fct):
        """ mouse in widget-focus and clicked
        - even: event mouse\n
        - wgt:  widget-object\n
        - fct:  called fubction if widget is clicked\n
        """
        par = self._in_widget(event, wgt)
        if par is not False:
            fct()

    def label_face(self, face=None):
        """ set descripten from image:\n
        - face:    appearence of "cd" = Interpret, "titel" = titel\n
        return:
        """
        #--- Colors = white,black,red,darkRed,green,darkGreen,blue,darkBlue,cyan
        #----         darkCyan,magenta,darkMagenta,yellow,darkYellow,gray,darkGray,
        #----         lightGray,transparent,color0(for bitmaps),color1GlobalColor
        if face == 'cd':
            self.wgt_label_cd.setStyleSheet(self.style['labelOn'])
            self.wgt_label_cd.setFrameShape(1)
            self.wgt_label_titel.setStyleSheet(self.style['labelOff'])
            self.wgt_label_titel.setFrameShape(0)
        if face == 'titel':
            self.wgt_label_titel.setStyleSheet(self.style['labelOn'])
            self.wgt_label_titel.setFrameShape(1)
            self.wgt_label_cd.setStyleSheet(self.style['labelOff'])
            self.wgt_label_cd.setFrameShape(0)

    def show_infos(self, err_image='no_image.gif'):
        """ show track-infos (text / cover):\n
        err_image:  image for not available covers (path = application-dir)\n
        return:
        """
        info = ['']
        #--- find cover-file ---
        if ListData_name == 'cd':
             info[0] = self.find_get('path', self.vuw_cd.data[self.vuw_cd.row]) + '/'
        #--- show text-infos ---
        if ListData_name == 'titel':
            info = self.info_get(self.vuw_titel.current)
            self.wgt_label_titel.setText( info[7][0] )
            cd_ = info[2] + '\n -' + info[3]
            self.wgt_label_cd.setText( cd_ )
            inf = 'GENRE: ' + info[4] + '   JAHR: ' + str(info[5]) +\
                '\nIMPORT: ' +  info[6] + '   NR:' + str(info[7][1]) + '   CALLS:' + str(info[7][2])
            self.wgt_label_info.setText( inf )
        #--- find cover-file ---
        file = glob.glob(info[0] +'?over*1.jpg')
        if len(file) > 0:
            file = file[0].replace('\\', '/')
        else:
            file = os.getcwd().replace('\\', '/') + '/' + err_image
        #--- show cover ---
        if self.show_change != file:
            self.show_change = file
            scene = QtWidgets.QGraphicsScene()
            pixmap = QPixmap(file)
            height = self.wgt_image.height()
            width = self.wgt_image.width()
            pixmap = pixmap.scaled(width, height, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene.addItem(item)
            self.wgt_image.setScene(scene)

    def show_msg(self, text, head = "Titel beendet"):
        """ show message-box:\n
        text:  text-information\n
        head:   text header
        return:button clicked
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(head)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg.exec_()

    def end_run(self):
        """ call at end of titel. differentiates between in search / play """
        state = self.get_state()
        if state == 0:
            if self.auto is True:
                if self.list_change_search is True:
                    state = self.list_switch('play', opt='up')
                    if self.show_msg('Nächste Playlist-Titel ?') == QMessageBox.No:
                        state = False
                    self.bar_set()
                else:
                    state = self.list_ctrl('up')
                if state is not False:
                    self.start_play()
                if self.list_change_search is True:
                    self.list_switch('search')
        self.auto = True

