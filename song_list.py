# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 12:07:58 2022

@author: juergen
"""
import sys
sys.path.insert(0,'D:/Projekte/PyAudioPlay/AudioPlay_V0/')
import time
import os
import copy
import logging
import shutil
from json_data import JsonData
from json_data import json_show

class SongList():
    """ json-format for data creation
    """
    class INI():
        """ app paramter
        """
        cd_info  = 'CDInfo.txt'
        cd_index = 'CDIndex.txt'
        cd_text = 'CD'
        cd_max  = 10000
        cd_min  = 1


    def __init__(self, log_file = 'report.log'):
        """ init
        Set the data-struct
        """
        #--- Daten-Strukturen laden ---
        self._base = JsonData('base_main.bas')
        self._list = JsonData('list_search.lst')
        self._init = JsonData('AudioPlay.ini')
        self._info = JsonData('info_cd.txt')
        #FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.basicConfig (filename=log_file, filemode='a',\
             level=logging.INFO, format='%(message)s')


    def _titel_list(self, cd_, name=None):
        """select titel & titel-paramter from base-list:\n
        cd_:    cd_-Name\n
        name:   None = Titel-Liste\n
        result: [titel_path, Titel, position, calls]\n
        """
        val=[]
        if name is None:
            path = self._base.data['data'][cd_]['path']
            for titel in self._base.data['data'][cd_]['tracks']:
                val.append([path + '/' + titel[0], titel[0], titel[1], titel[2]])
        else:
            try:
                for track in self._base.data['data'][cd_]['tracks']:
                    val.append(track[0])
                index = val.index(name)
                val = self._base.data['data'][cd_]['tracks'][index]
            except ValueError:
                val = ['[ERROR]: unknow track "' + name + '"', 0, 0]
                self.error('_titel_list', '[ERROR]: track:"' + name +
                           '" not in CD:"' + cd_ +'"', False)
        return val


    def split_name_int(self, text):
        """ split text and integer (text, number)
        text:   text with numbers
        result: text split from numbers (text, numbers)
        """
        numb = ''
        name = ''
        for chr_ in text:
            if chr_.isdigit() is True:
                numb = numb + chr_
            else:
                name = name + chr_
        return name, numb


    def _head_edit(self, lsttyp, file=None, free_nr=None):
        """ edit head-section
        lsttyp: list-typ: list=Songlist, base=CD Data-Base
        file:   name of file
        freeNr: next free list-number
        """
        if file is not None:
            lsttyp.data['head']['name'] = file
        lsttyp.data['head']['date'] = self.get_time()
        lsttyp.data['head']['count'] = str(len(lsttyp.data['data']))
        if free_nr is not None:
            lsttyp.data['head']['freeNr'] = free_nr


    #*************************************************************************
    #************************** GeneralFunction ******************************
    def error(self, source, msg, exit_app = True):
        """ error handler with message and protocol
        source: occurrence of the error
        msg:    Error-Infotext
        exit_app:   True=Abort App, False=only protocolation
        result: Error-Infotext
        """
        error = self.get_time() + ':' + '<' + source + '>. ' + str(msg)
        #--- exit application ---
        if exit_app is True:
            assert False, error
        else:
            #--- save to protokol ---
            logging.info(error)
        return error


    def show_prozess(self, cur, count, msg=''):
        """ show the currently prozess
        cur:   current number prozess
        count: Expected number of prozesses
        msg:   description of the prozess
        """
        print(str(int(cur)+1) + 'v' + str(count) + ': ' + str(msg) )
        #time.sleep(1)


    def get_time(self, typ='date_time'):
        """ give the time(date,time,date_time)
        typ:    date=date EU, time=time, date_time=date EU & time
        """
        date = time.localtime()
        if typ == 'date_time':
            val = str(date[2]).rjust(2,'0') + '.' + str(date[1]).rjust(2,'0') +\
                    '.' + str(date[0]) + ' ' +  str(date[3]).rjust(2,'0') +\
                    ':' + str(date[4]).rjust(2,'0')
        if typ == 'date':
            val = str(date[2]).rjust(2,'0') + '.' + str(date[1]).rjust(2,'0') +\
                    '.' + str(date[0])
        if typ == 'time':
            val = str(date[3]).rjust(2,'0') +  ':' + str(date[4]).rjust(2,'0')
        return val


    def save(self, typ, file=None ):
        """save list(play or base) as file(ASCII)
        typ:    list=working-list, base=base-list
        file:   file-name for new file
        """
        val = None
        if typ == 'list':
            val = self._list.save(file)
            self._head_edit(self._list, file) #- set [head]-data
        if typ == 'base':
            val = self._base.save(file)
            self._head_edit(self._base, file) #- set [head]-data
        if val is None:
            self.error('save', '[error] wrong parameter: ' + typ)
        return val


    def load(self, typ, file=''):
        """load list(play or base) as file(ASCII)
        typ:    list=working-list, base=base-list
        file:   file-name for new file
        """
        val = None
        if typ == 'list':
            val = self._list.load(file)
        if typ == 'base':
            val = self._base.load(file)
        if val is None:
            self.error('load', '[error] wrong parameter: ' + typ)
        return val


    def get_init(self, typ):
        """ read settings(cd-path,bin,...) from ini-file:\n
        typ:\n
        - cd        = path for dcs\n
        - bin       = execute-files\n
        - list      = player-list\n
        - searchTyp = search-key\n
        - searchVal = search-value
        - lastPlay  = last wave
        return: value
        """
        val = None
        if typ == 'cd':
            val = self._init.data['path'][typ]
        if typ == 'bin':
            val = self._init.data['path'][typ]
        if typ == 'list':
            val = self._init.data['player'][typ]
        if typ == 'searchTyp':
            val = self._init.data['player'][typ]
        if typ == 'searchVal':
            val = self._init.data['player'][typ]
        if typ == 'lastPlay':
            val = self._init.data['player'][typ]
        if val is None:
            self.error('_get_init', '[error] wrong parameter: ' + typ)
        return val


    #*************************************************************************
    #*************************** base-Function *******************************
    def _base_info_check(self, path):
        """ check the cd-root and the CDInfo-File
        path:       path to the cd
        result:     True = done, Other = ERROR-message
        """
        state =True
        file_list = os.listdir(path)# list all files & paths
        del_list = copy.deepcopy(file_list)
        #--- read CDInfo.txt ---
        home = path + '/' + self.INI.cd_info
        self._info.load(home)
        home = path + '/'
        #--- check path is available ---
        if os.path.isdir(self._info.data['path']):
            #print('>>> _base_info_check:',self._info.data['path'],'\n')
            #--- check head is empty ---
            if self._info.data['interpret'] == '<unknow>':
                if self._info.data['album'] == '<unknow>':
                    self.error('base_info_prep', \
                             '[WARNING]: edit head-section'+\
                            '(interpret,album....): ' +  path, False)
            #--- check tracks in CDInfo-File ---
            for track in self._info.data['tracks']:
                if (track[0] in file_list) is False:
                    self.error('base_info_check', '[ERROR]: tracks not found: ' +\
                               home + track[0], False)
                else:
                    del_list.remove(track[0])
            #--- check images in CDInfo-File ---
            for image in self._info.data['image']:
                if (image in file_list) is False:
                    self.error('base_info_check', '[WARNING]: Image not found:' +\
                               home + image, False)
                else:
                    if image in del_list:
                        del_list.remove(image)
            #--- clear del-list ---
            for delin in [self.INI.cd_index, self.INI.cd_info]:
                if delin in del_list:
                    del_list.remove(delin)
            #--- check if files unuesd ---
            for file in del_list:
                #--- unknows files ---
                self.error('base_info_check', '[WARNING]: unknow files:' + home + file, False)
        else:
            self.error('base_info_check', '[ERRORR]: unknow CD-Path in "CDInfo.txt":' +\
                       home + 'CDInfo.txt = ' + self._info.data['path'], False)
        return state


    def _base_info_conv(self, path):
        """ tranfer "info_file" in "CDInfo.txt" format
        path:       path to the cd
        result:     True = done, Other = ERROR-message
        """
        state = True
        error = False
        def line_cdindex(line, key, sep1='=', sep2='#'):
            """ separate key word & value from line
            result:     tulpe Key, Value or None
            """
            state = [None, None, None]
            nr_ = ''
            try:
                val1 = line.split(sep1)
                if val1[0].find(key) == 0:
                    val2 = val1[1].split(sep2)
                    for pos in val1[0]:
                        if pos.isdigit():
                            nr_ = nr_ + pos
                        state = [val1[0], val2[0].replace('\n',''), nr_]
            except ValueError:
                pass
            return state
        info_list ={'path':'CDDir', 'interpret':'Interpret', 'album':'Album',
                  'genre':'Genre', 'year':'Jahr' }
        #--- read index as line-array ---
        with open(path + '/' + self.INI.cd_index) as row:
            cd_index = row.readlines()
        row.close()
        #--- convert CDIndex to CDInfo ---
        val = ''
        #--- Infos converion ---
        for key in info_list:
            for line in cd_index:
                if line.find(info_list[key]) == 0:
                    val = line_cdindex(line, info_list[key])
                    #--- check path ---
                    if key == 'path':
                        if val[1][-1] == chr(92):
                            val[1] = val[1][0:-1]
                        val[1] = val[1].replace(chr(92), '/')
                        if os.path.isdir(val[1]) is not True:
                            state = '[ERROR _base_info_conv]: directory not available: ' + val[1]
                            error = True
                    if not error:
                        self._info.data[key] = val[1]
        #print ('>>> info_conv:', self._info.data, '\n', cd_index)
        #assert False
        #--- image conversion ---
        val =[]
        for line in cd_index:
            if line.find('Image') == 0:
                val.append(line_cdindex(line, 'Image')[1])
        self._info.data['image'] = val
        #self._info.data['image'].sort(reverse=True)
        val = []
        #--- tracks conversion ---
        for line in cd_index:
            if line.find('Track') == 0:
                tmp = line_cdindex(line, 'Track')
                val.append( [tmp[1], int(tmp[2]), 0] )
        self._info.data['tracks'] = val
        return state


    def _base_info_prep(self, path):
        """ prepered for a new  cdinfo text-block (not all infos available)
        path:       path to the cd
        result:     True = done, Other = ERROR-message
        """
        def file_find(ext, dat):
            """ find list of file-extensions
            ext:    image=.jpg/.bmp/..., track=.wav/.mp3/.flac
            dat:    data-element
            return: position (-1 not found)
            """
            state = -1
            search = {'image':['.jpg', '.bmp'],
                         'track':['.wav', '.mp3', '.flac']}
            for val in search[ext]:
                state = dat.find(val)
                if state > 0:
                    break
            return state
        state = True
        file_list = os.listdir(path)# list all files & paths
        for key in file_list:
            if os.path.isfile(path + '/' + key) is False:
                state = False
        #--- great CDInfo.txt if files available ---
        if state is True:
            val = ['interpret', 'album', 'genre', 'year', 'import']
            #--- infos convertieren ---
            self._info.data['path'] = path
            for key in val:
                self._info.data[key] = '<unknow>'
            #--- tracks listen ---
            val =[]
            self._info.data['tracks'].clear()
            i=1
            for file in file_list:
                if file_find('track', file) > 0:
                    val.append([file, i, 0])
                    i += 1
                    self._info.data['tracks'] = val
            #--- image listen ---
            #file_list.sort(reverse=True)
            self._info.data['image'].clear()
            for file in file_list:
                if file_find('image', file) > 0:
                    self._info.data['image'].append(file)
                    #print('>>> _base_info_prep:', file, key, '\n')
        else:
            state = '[ERROR _base_info_prep]: no files available: ' +  path
        return state


    def _base_info_update(self, name):
        """ update CDInfo.txt with base-list
        name:  edit-name = cd-path
        result: True = done, Other = ERROR-message
        """
        state = True
        path_name = name.split('/')
        info_file = name + '/' + self.INI.cd_info
        self._info.load(info_file)
        self._info.data = self._base.data['data'][path_name[-1]]
        if state is True:
            self._info.save(info_file)
        return state


    def _base_add_cd(self, name, val=None, save=True):
        """ add a new cd in base-lst (image/track-files nessesery)
        name:  edit-name = cd-path
        val:   head-value = head:{'interpret':'?', 'album':'?', 'genre': '?',\
               'year':'?', 'import':'?'} or val = None(export head from "CDInfo.txt")
        result: True = done, Other = ERROR-message
        """
        state = True
        path_name = name.split('/')
        if os.path.isdir(name):
            if len(os.listdir(name)) > 0:
                if val is not None:
                    #--- Import head from val ---
                    state = self._base_info_prep(name)
                    for key in val:
                        if key in state:
                            state[key] = val[key]
                        else:
                            state = '[ERROR base_edit(add)]: unknow head \
                                      parameter: ' + key
                            break
                else:
                    #--- Import head from "CDInfo.txt""
                    save = False
                    state = self._info.load(name + '/' + self.INI.cd_info)
                    state['path'] = name
                self._base.data['data'].update({path_name[-1]:state})
                if save is True:
                    state = self._info.save(name + '/CDInfo.txt')
                    self._base.data['data'].update({path_name[-1]:state})
                    state = True
            else:
                state = '[ERROR base_edit(add)]: in "' + name + '" no files available'
        else:
            state = '[ERROR base_edit(add)]: path not available: ' + name
        return state


    def _base_del_cd(self, name):
        """ delete cd in base-list & file-system
        name:  edit-name = cd-path
        result: True = done, Other = ERROR-message
        """
        state = True
        path_name = name.split('/')
        if (path_name[-1] in self._base.data['data']) is True:
            self._base.data['data'].pop(path_name[-1])
            try:
                shutil.rmtree(name)
                state = True
            except FileNotFoundError:
                state = '[ERROR base_edit(del)]: path not available: ' + name
        else:
            state = '[ERROR base_edit(del)]: path not in base-list: ' + name
        return state


    def _base_rename_head(self, name, val):
        """ rename cd-head(interpret, album.....)
        name:  edit-name = cd-path
        val:   head-value = {'interpret':'?', 'album':'?', 'genre': '?',\
                             'year':'?', 'import':'?'}
        result: True = done, Other = ERROR-message
        """
        state = True
        path_name = name.split('/')
        if (path_name[-1] in self._base.data['data']) is True:
            for key in val:
                #--- rename base-list ---
                if key in self._base.data['data'][path_name[-1]]:
                    self._base.data['data'][path_name[-1]][key] = val[key]
                else:
                    state = '[ERROR base_edit(head)]: unknow head parameter: ' + key
                    break
             #--- update CDInfo.txt ---
        else:
            state = '[ERROR base_edit(head)]: path not in base-list: ' + name
        return state


    def _base_rename_track(self, name, val, par):
        """rename track-name / track-filer in base-list / cd-path
        name:  edit-name
        val:   value for add or file-name
        par:   xxx = new-name for file, "" = delet file
        result: True = done, Other = ERROR-message
        """
        state = True
        tmp = None
        path_name = name.split('/')
        if (path_name[-1] in self._base.data['data']) is True:
            state = [ key[0] for key in self._base.data['data'][path_name[-1]]['tracks'] ]
            if (val in state) is True:
                if par is not None:
                    #- rename track
                    tmp = state.index(val)
                    if par != '':
                        self._base.data['data'][path_name[-1]]['tracks']\
                                       [tmp][0] = par
                        try:
                            os.rename(name + '/' + val, name + '/' + par)
                            state = True
                        except FileNotFoundError:
                            state = '[ERROR base_edit(track)]: \
                             file not available: ' +  name + '/' + val
                    #- del track
                    else:
                        print (val, tmp)
                        self._base.data['data'][path_name[-1]]['tracks'].pop(tmp)
                        try:
                            os.remove(name + '/' + val)
                            state = True
                        except FileNotFoundError:
                            state = '[ERROR base_edit(track)]: \
                                file not available: ' + name + '/' + val
                else:
                    state = '[ERROR base_edit(track)]: no new track-name'
            else:
                state = '[ERROR base_edit(track)]: track "' + val +\
                        '" not in base-list: ' +  name
        else:
            state = '[ERROR base_edit(image)]: path not in base-list: ' + name
        return state


    def _base_import_cd(self, source, target, auto=True):
        """ import cds-path(with wav/image/CDinfo.txt) to target
        source:  source-path
        target:  target-path
        dirs:    CD-Dir
        auto:    True= automatic CD-Name, False= Source CD-Name
        result:  True = done, Other = ERROR-message
        """
        def copy_cdpath(cpy_from, cpy_to, dirs):
            state = True
            #--- copy cd-path ---
            length = len(os.listdir(home))
            if length > 1:
                cpy_from = cpy_from + '/' + dirs
                if auto is True:
                    cd_dir = cpy_to + '/' + self._base_find_freecd()
                else:
                    cd_dir = cpy_to + '/' + dirs
                try:
                    shutil.move(cpy_from, cd_dir)
                    state = self.base_edit('add', cd_dir, None)
                    #print('>>>>_base_import_cd:',cpy_from, cd_dir)
                except IOError as msg:
                    state = '[ERROR _base_import_cd]: file accsess denied: '+ str(msg)
                else:
                    state = '[ERROR _base_import_cd]: no audio-files available'
            return state
        state =True
        file_list = os.listdir(source)# list all files & paths
        count = len(os.listdir(source))
        if count < 1:
            state = '[ERROR _base_import_cd]: no imports available'
        if os.path.isdir(target):
            for i, dirs in enumerate(file_list):
                home = source + '/' + dirs
                if os.path.isdir(home):
                    #--- copy if CDInfo.txt available ---
                    if os.path.isfile(home + '/' + self.INI.cd_info):
                        state = copy_cdpath(source, target, dirs)
                        self.show_prozess(i, count, home )
                    else:
                        state = '[ERROR _base_import_cd]: no "CDInfo.txt" available'
                else:
                    state = '[ERROR _base_import_cd]: object is not a directory: '+ dirs
        else:
            state = '[ERROR _base_import_cd]: target directory is not available: '+ target
        return state


    def _base_find_freecd(self):
        """ find the next free-cd-path/name in base-list
        result:next free CD-Name
        """
        next_numb = self.INI().cd_min
        while next_numb <= self.INI().cd_max:
            if self.INI.cd_text + str(next_numb) in self._base.data['data']:
                next_numb += 1
            else:
                break
        return self.INI.cd_text + str(next_numb)


    def base_build_cdinfo(self, save=True):
        """ build / check the "CDInfo.txt" for all cds in init.path:\n
        - save:  save CDInfo.txt in cd path\n
        result:     (list of all available cds (cd_dir), True / Errors)\n
        """
        cd_dir = []
         #--- scan cd-paths ----
        for home in self.get_init('cd'):#- all cd-roots from init-file
            for cds in os.listdir(home):#- cd-path in roots
                if os.path.isdir(home + '/' + cds):
                    cd_dir.append(home + '/' + cds)
                else:
                    self.error('base_build_cdinfo',\
                    '[ERROR]: wrong cd-path: "' +  home + '/' + cds +\
                    '". Only directories without files allowed (AudioPlay.ini.cd)', False)
        count = len(cd_dir)
        #print('>>> base_build_cdinfo:', cd_dir, '\n')
        #--- great base_list ---
        #self._base.data['data'].clear()# clear base-list
        for i, path in enumerate(cd_dir):
            state = None
            #------------ greate "CDInfo.txt" file ---------------
            #--- new info-file 'CDInfo.txt' ---
            if os.path.isfile(path + '/' + self.INI.cd_info):
                state = self._base_info_check(path)
            else:
                #--- old info-file 'CDIndex.txt' ---'
                if os.path.isfile(path + '/' + self.INI.cd_index):
                    state = self._base_info_conv(path)
                else:
                    #--- no info-file ---
                    state = self._base_info_prep(path)
                    if state is True:
                        self.error('base_info_prep',\
                        '[WARNING]: edit head-section'+\
                        '(interpret,album....): ' +  path, False)
            self.show_prozess(i, count, cd_dir[i] + ': <base_build_info> ' + str(state) )
            if state is not True:
                self.error('base_build_cdinfo', state, False)
            else:
                #--- save CDInfo ---
                if save is True:
                    self._info.save(path + '/' + self.INI.cd_info)
        return cd_dir


    def base_make(self, save=True, sort = False):
        """ make a new "base_main.bas" list for all avaiable cds with "CDInfo.txt":\n
        - save:  save the new "base_main.bas"\n
        - sort:  True = sort after interpret, sort after CD-Name\n
        result: True = done, Other = ERROR-message
        """
        state = True
        #--- great base_list ---
        self.error('base_make', '################### make a new "base_main.bas" '+\
                                '###################', False)
        cd_list = self.base_build_cdinfo()
        count = len(cd_list)
        self._base.data['data'].clear()# clear base-list
        for i, path in enumerate(cd_list):
            #------------ greate "base_main.bas ---------------
            if os.path.isfile(path + '/' + self.INI.cd_info):
                #state = self._base_info_check(path)
                self._base_add_cd(path, val=None, save=True)
                self.show_prozess(i, count, cd_list[i] + ': <base_make> done')
        #--- check "base_main" for duplicate ---
        cd_list = []
        for cd_ in self._base.data['data']:
            cd_list.append([ cd_, self._base.data['data'][cd_]['path'] ])
        for pos, cd_ in enumerate(cd_list):
            if str(cd_[1]).find(cd_[0]) < 0:
                self.error('base_make', '[FATAL]: ' + \
                    'CD-Name:"' + cd_[0] + '" not in CD-Path:"' + cd_[1] + '"', False)
        #--- sort base_list after interpreter / CD-Path ---
        cd_list.clear()
        base_list = {}
        for cd_ in self._base.data['data']:
            #--- built sort_key ---
            if sort is True:
                sort_key = self._base.data['data'][cd_]['interpret'] + ':' +\
                            self._base.data['data'][cd_]['album']
            else:
                txt, numb = self.split_name_int(cd_)
                if numb.isdecimal():
                    numb =int(numb)
                else:
                    numb = 10000
                sort_key = [txt,numb]
                #print('>>> base:', txt, numb)
            #--- add sort_key + data ---
            cd_list.append([sort_key, cd_])
        cd_list.sort() #- Liste sortieren
        #------ copy the base_list -------
        base_list.update({'head':self._base.data['head']})
        base_list.update({'data':{}})
        for cd_ in cd_list:
            cd_dat = self._base.data['data'][cd_[1]]
            self._base.data['data'].pop(cd_[1])
            base_list['data'].update({cd_[1]:cd_dat})
        #print('>>> sort=', base_list, '\n')#self._base.data['data'], '\n')
        self._base.data = copy.deepcopy(base_list)
        #json_show(self._base.data)
        #---  edit base-head ---
        self._base.data['head']['date'] = self.get_time()
        self._base.data['head']['count'] = str(count)
        self._base.data['head']['freeNr'] = self._base_find_freecd()
        #--- save base-list ---
        if save is True:
            self._base.save()
        self.error('base_make', '###################         end of make        '+\
                                '###################', False)
        return state


    #def base_edit(self, typ, name, val, par=None, save = True):
    def base_edit(self, typ, *par, save = True):
        """ edit par[0](add,del,head,track) in the base-list\n
        - typ:\n
            - add:   par[0] = cd-path with image/track-files, par[2] = header(album...)\n
            - del:   par[0] = cd-path with image/track-files\n
            - head:  par[0] = cd-path, par[1] = new header\n
            - track: par[0] = cd-path, par[1] = old file-name, par[2] = new filename or del("")\n
            - import:par[0] = import-path, par[1] = target-path\n
        - save:   save base_main.bas\n
        result: True = done, Other = ERROR-message\n
        """
        state = None
        #----- add new cds with data -----
        if typ == 'add':
            state = self._base_add_cd(par[0], par[1])
        #----- delete exist cds and his data -----
        if typ == 'del':
            state = self._base_del_cd(par[0])
        #----- edit head of cd -----
        if typ == 'head':
            state = self._base_rename_head(par[0], par[1])
            if state is True:
                state = self._base_info_update(par[0])
        #----- rename / remove track -----
        if typ == 'track':
            state = self._base_rename_track(par[0], par[1], par[2])
            if state is True:
                state = self._base_info_update(par[0])
        if typ == 'import':
            state = self._base_import_cd(par[0], par[1])
        #--- save base-list ---
        if save is True:
            self._base.save()
        else:
            self.error('base-list', state, False)
        return state


    #**************************************************************************
    #************************** list-methoden *********************************
    def list_select(self, typ, par=True, num=None):
        """ select from current list\n
        - typ:\n
            - cd:    cd-infos from list (par: True=all, False=reduct)\n
                 return:(cd_path, Interpret, Album, genre, year, import)\n
            - titel: titel from cd/list.(par: cd_name, ""=all titel)\n
                 return: (titel_path, titel_name, track_nr, call_count)\n
            - sort:  intern use for sort-function\n
                 return:(interpret,album,genre,year,import,titel_nr)\n
        - par: <typ=cd> true=full, false =reduct <typ:titel> cd_name or all("")\n
        - num: select titel/CD-position\n
        return: depentend from function
        """
        item = []
        self.last_cdpath = ''
        def basic_data(numb):
            path = self._list.data['data'][numb][0]
            cd_ = str(path).split('/')[-1]
            track = self._list.data['data'][numb][1][0]
            return path, cd_, track
        def typ_cd(item):
            interpret = self._base.data['data'][cd_]['interpret']
            album = self._base.data['data'][cd_]['album']
            genre = self._base.data['data'][cd_]['genre']
            year = self._base.data['data'][cd_]['year']
            imp_ = self._base.data['data'][cd_]['import']
            if par is not False:
                if self.last_cdpath != cd_:
                    item.append([cd_, interpret, album, genre, year, imp_])
                    self.last_cdpath = cd_
            else:
                item.append([path, interpret, album, genre, year, imp_])
            return item
        def typ_titel(item):
            titel_path = path + '/' + track
            info = self._titel_list(cd_, track)
            item.append([titel_path, track, info[1], info[2]])
            return item
        def typ_sort(item):
            interpret = self._base.data['data'][cd_]['interpret']
            album = self._base.data['data'][cd_]['album']
            genre = self._base.data['data'][cd_]['genre']
            year = self._base.data['data'][cd_]['year']
            imp_ = self._base.data['data'][cd_]['import']
            pos = self._titel_list(cd_, track)[1]
            item.append([interpret, album, genre, year, imp_, pos, cd_])
            return item
        #--- list with all items of list ---
        val = []
        for i, j in enumerate(self._list.data['data']):
            item = []
            path, cd_, track = basic_data(i)
            if  typ == 'cd':
                typ_cd(item)
            if  typ == 'titel':
                if par == '':
                    typ_titel(item)
            if  typ == 'sort':
                typ_sort(item)
            if len(item) > 0:
                val = val + item
        if typ == 'titel':
            if par != '':
                val = self._titel_list(par)
        if num is not None:
            val = val[num]
        return val

    def list_edit(self, mode, par1=None, par2=None):
        """ edit(clear,add...) the list-format: [ path,[pos,calls] ]:\n
        - mode:\n
            - add  = added track to list (par1 = [ path,[pos,calls] ])\n
            - cd   = added all tracks from cd (par1 = path)\n
            - del  = remove track from list (par1 = list-nr)\n
            - clear= remove all tracks (no par.)\n
            - ins  = insert track before nr (par1 = [ path,[pos,calls], par2 = nr )\n
            - head = update date & count & name (par1 = new list-name)\n
        - par1:   add,cd = cd-name, del=list-nr\n
        - par2:   list-position\n
        return: True or Errors\n
        """
        state = True
        if mode =='clear':
            self._list.data['data'].clear()
        if mode == 'add':
            self._list.data['data'].append(par1)
        if mode == 'cd':
            path = self._base.data['data'][par1]['path']
            #print('>>>> list_edit:',path)
            if os.path.isdir(path):
                for titel in self._base.data['data'][par1]['tracks']:
                    add_items = [self._base.data['data'][par1]['path'], titel]
                    self._list.data['data'].append(add_items)
            else:
                state = '[ERROR list_edit]: directory is not available: '+ str(par1)
        if mode == 'del':
            self._list.data['data'][par1].clear()
        if mode == 'ins':
            self._list.data['data'].insert(par2,par1)
        if mode == 'head':
            if par1 is not None:
                self._list.data['head']['name'] = par1
            self._list.data['head']['date'] = self.get_time()
            self._list.data['head']['count'] = str(len(self._list.data['data']))
        return state

    def list_sort(self, typ, z_a=False):
        """ sort(interpreter,album...) the play-list:\n
        - typ:    sortfunction = -interpret, -album, -genre, -year, -import, -rand(random)\n
        - z_a:    sort-direction
        return: True or Errors
        """
        state = True
        sort_list = []
        key = None
        #--- Selection of the sorting expression pos=3
        if typ == 'interpret':
            key={'interpret':0,'album':1,'genre':2,'year':3,'import':4}
        if typ == 'album':
            key={'album':1,'interpret':0,'genre':2,'year':3,'import':4}
        if typ == 'genre':
            key={'genre':2,'interpret':0,'album':1,'year':3,'import':4}
        if typ == 'year':
            key={'year':3,'interpret':0,'album':1,'genre':2,'import':4}
        if typ == 'import':
            key={'import':4,'interpret':0,'album':1,'genre':2,'year':3}
        if typ == 'rand':
            key = True
        if key is None:
            self.error('list_sort', '[error] wrong parameter: ' + typ)
        if key != 'rand':
            #--- sortieren als interpret, album, genre, year, import ---
            sort_info = self.list_select('sort', '')
            for i in range(0, len(sort_info)):
                #--- built sort_key ---
                sort = ''
                for j in key:
                    sort = sort + str(sort_info[i][key[j]]) + ':'
                sort_key = [sort, int(sort_info[i][5])]
                #--- add sort_key + data ---
                sort_list.append([sort_key, self._list.data['data'][i]])
            #--- sort-list save as playlist
            sort_list.sort(reverse = z_a) #- Liste sortieren
        else:
            #---------------- generate a random-list -------------------
            pass
        #------ copy the sort-list -------
        for i, val in enumerate(sort_list):
            self._list.data['data'][i] = val[1]
        return state

    def list_filter(self, typ, value, clear=True):
        """ search(interpret,album...) in base-list after parameter and gerate\
            the search-list\n
        - typ:    searchfunction -interpret, -album, -genre, -year, -import\n
        - value:  Keyword\n
        - clear:  Clear current list\n
        return: state True or Errors
        """
        def _base_search_cd(key, search, new=True):
            """ search in bas-list
            key:    key in cd-data
            val:    search-value
            return: state True or Errors
            """
            state = True
            cd_ = None
            if new is True:
                state = self.list_edit('clear',cd_)
            for cd_ in self._base.data['data']:
                val = str(self._base.data['data'][cd_][key]).lower().find(str(search).lower())
                if val >= 0:
                    state = self.list_edit('cd',cd_)
            self.list_edit('head','neuer Name xxxx')
            return state
        val = None
        if typ == 'interpret':
            val = _base_search_cd(typ, value, clear)
        if typ == 'album':
            val = _base_search_cd(typ, value, clear)
        if typ == 'genre':
            val = _base_search_cd(typ, value, clear)
        if typ == 'year':
            val =_base_search_cd(typ, value, clear)
        if typ == 'import':
            val =_base_search_cd(typ, value, clear)
        if val is None:
            self.error('list_filter', '[error] wrong parameter: ' + typ)
        return val

#=============================================================================
# ============================ Modul Test ====================================
if __name__ == '__main__':
    db = SongList()#'D:/Projekte/PyAudioPlay/AudioPlay_V0/report.log')
    #json_show(db._base.data)
    # print(db._init.data)
    # print(db._info.data)
    print ( db.base_make(sort=True) ,'<base_make>\n')
    #json_show(db._base.data)
    print (db.list_filter('album', ''),'<list_filter>\n')
    db.save('list')
    db.load('list')
    print( db.list_sort('import', True),'<list_sort>\n')
    #json_show(db._list.data)
    for lst in db.list_select('cd'):
          print(lst)
    cd_name = ''
    for lst in db.list_select('titel', cd_name, None):
        print(lst)
    #----------- list_edit ---------------
    db.list_edit('clear')
    db.list_edit('cd', 'CD33')
    db.list_edit('del', 0)
    db.list_edit('add', ['c:/',['append Titel.wav',1,2]])
    db.list_edit('ins', ['d:/test/',['insert Titel.wav',3,4]],4)
    #json_show(db._list.data)
    print (db.get_init('lastPlay'))
    #print ( db.base_make(db.base_build_cdinfo()))
    head = {'interpret': 'Pink', 'album': 'Lady', 'genre': 'Pop', \
            'year': '2019', 'import': '12.04.2020'}
    #print(db.base_edit('del', 'D:/_Test_CD/Audio/CD34' ) )
    print(db.base_edit('head', "D:/_Test_CD/Archiv2/CD537", head), '<base_edit(head)>\n')
    print(db.base_edit('import', 'D:/_Test_CD/Import', 'D:/_Test_CD/Audio'), '<base_edit(import)>\n' )
    print('----------------------------------------------')
    #json_show(db._base.data)
    assert False, 'Stop'
