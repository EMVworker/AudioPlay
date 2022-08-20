# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 12:07:58 2022

@author: juergen
"""
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
        """select titel & titel-paramter from base-list
        cd_:     cd_-Name
        name:   None = Titel-Liste, xxx: result[0]=position result[1]=calls
        """
        val=[]
        for titel in self._base.data['data'][cd_]['tracks']:
            val.append(titel[0])
        if name is not None:
            #print('>>> _titel:', val, name)
            index = val.index(name)
            val = self._base.data['data'][cd_]['tracks'][index]
        return val


    def _head_edit(self, lst, file=None, free_nr=None):
        """ edit head-section
        lst:    list-typ: list=Songlist, base=CD Data-Base
        file:   name of file
        freeNr: next free list-number
        """
        if file is not None:
            lst.data['head']['name'] = file
        lst.data['head']['date'] = self.get_time()
        lst.data['head']['count'] = str(len(lst.data['data']))
        if free_nr is not None:
            lst.data['head']['freeNr'] = free_nr


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
        """ read settings(cd-path,bin,...) from ini-file
        typ:    cd=path for dcs, bin=execute-files, list=player-list
                searchTyp=search-key, searchVal=search-value, lastPlay= last wave
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
    def _base_info_check(self, path, info_file='CDInfo.txt'):
        """ check the cd-root and the CDInfo-File
        path:       path to the cd
        info_file:  Name of InfoFile
        result:     True = done, Other = ERROR-message
        """
        state =True
        file_list = os.listdir(path)# list all files & paths
        del_list = copy.deepcopy(file_list)
        #--- read CDInfo.txt ---
        home = path + '/' + info_file
        self._info.load(home)
        home = path + '/'
        #--- check head is empty ---
        if self._info.data['interpret'] == '<unknow>':
            if self._info.data['album'] == '<unknow>':
                self.error('base_info_prep', \
                         '[[WARNING _base_info_prep]: edit head-section'+\
                        '(interpret,album....): ' +  path, False)
        #--- check tracks in CDInfo-File ---
        for track in self._info.data['tracks']:
            if (track[0] in file_list) is False:
                self.error('base_info_check', 'tracks not found: ' +\
                           home + track[0], False)
            else:
                del_list.remove(track[0])
        #--- check images in CDInfo-File ---
        for image in self._info.data['image']:
            if (image in file_list) is False:
                self.error('base_info_check', 'Image not found:' + home + image, False)
            else:
                if image in del_list:
                    del_list.remove(image)
        #--- clear del-list ---
        for delin in ['CDIndex.txt', 'CDInfo.txt']:
            if delin in del_list:
                del_list.remove(delin)
        #--- check if files unuesd ---
        for file in del_list:
            #--- unknows files ---
            self.error('base_info_check', 'unknow files:' + home + file, False)
        return state


    def _base_info_conv(self, path, info_file='CDIndex.txt'):
        """ tranfer "info_file" in "CDInfo.txt" format
        path:       path to the cd
        info_file:  name of infoFile
        result:     True = done, Other = ERROR-message
        """
        self._list
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
        with open(path + '/' + info_file) as row:
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
                            #print('>>>_base_info_conv:', val[1])
                            state = '[[ERROR _base_info_conv]: directory not available: ' + val[1]
                            error = True
                        if not error:
                            self._info.data[key] = val[1]
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
                #print ('>>> line_cdindex:', tmp)
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
                #print('>>> _base_info_prep:', self._info.data[key])
                self._info.data[key] = '<unknow>'
                #--- tracks listen ---
                val =[]
                i=1
                for file in file_list:
                    if file_find('track', file) > 0:
                        val.append([file, i, 0])
                        i += 1
                        self._info.data['tracks'] = val
                #--- image listen ---
                #file_list.sort(reverse=True)
                for file in file_list:
                    if file_find('image', file) > 0:
                        self._info.data['image'].append(file)
        else:
            state = '[[ERROR _base_info_prep]: no files available: ' +  path
        return state


    def _base_info_update(self, name, info_file='CDInfo.txt'):
        """ update CDInfo.txt with base-list
        name:  edit-name = cd-path
        result: True = done, Other = ERROR-message
        """
        state = True
        path_name = name.split('/')
        info_file = name + '/' + info_file
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
                    state = self._info.load(name + '/' + 'CDInfo.txt')
                self._base.data['data'].update({path_name[-1]:state})
                if save is True:
                    state = self._info.save(name + '/CDInfo.txt')
                    self._base.data['data'].update({path_name[-1]:state})
                    state = True
            else:
                state = '[ERROR base_edit(add)]: in "' + name + '" no files available'
        else:
            state = '[[ERROR base_edit(add)]: path not available: ' + name
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
                state = '[[ERROR base_edit(del)]: path not available: ' + name
        else:
            state = '[[ERROR base_edit(del)]: path not in base-list: ' + name
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
            state = '[[ERROR base_edit(head)]: path not in base-list: ' + name
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
                            state = '[[ERROR base_edit(track)]: \
                             file not available: ' +  name + '/' + val
                    #- del track
                    else:
                        print (val, tmp)
                        self._base.data['data'][path_name[-1]]['tracks'].pop(tmp)
                        try:
                            os.remove(name + '/' + val)
                            state = True
                        except FileNotFoundError:
                            state = '[[ERROR base_edit(track)]: \
                                file not available: ' + name + '/' + val
                else:
                    state = '[[ERROR base_edit(track)]: no new track-name'
            else:
                state = '[[ERROR base_edit(track)]: track "' + val +\
                        '" not in base-list: ' +  name
        else:
            state = '[[ERROR base_edit(image)]: path not in base-list: ' + name
        return state


    def _base_import_cd(self, source, target):
        """ import cds-path(with wav/image/CDinfo.txt) to target
        source:  home from source
        target:  target of the import
        result:  True = done, Other = ERROR-message
        """
        state =True
        file_list = os.listdir(source)# list all files & paths
        count = len(os.listdir(source))
        if count < 1:
            state = '[ERROR _base_import_cd]: no imports available'
        if os.path.isdir(target):
            for i, dirs in enumerate(file_list):
                home = source + '/' + dirs
                if os.path.isdir(home):
                    if os.path.isfile(home + '/' + 'CDInfo.txt'):
                        length = len(os.listdir(home))
                        if length > 1:
                            try:
                                shutil.move(home, target)
                            except IOError as msg:
                                state = '[ERROR _base_import_cd]: file accsess denied: ', msg
                            self.show_prozess(i, count, home )
                        else:
                            state = '[ERROR _base_import_cd]: no audio-files available'
                    else:
                        state = '[ERROR _base_import_cd]: no "CDInfo.txt" available'
                else:
                    state = '[ERROR _base_import_cd]: object is not a directory: '+ dirs
        else:
            state = '[ERROR _base_import_cd]: target directory is not available: '+ target
        return state


    def _base_build_cdinfo(self, save=True):
        """ build / check the "CDInfo.txt" for all cds in init.path
        save_info:  save CDInfo.txt in cd path
        result:     (list of all available cds (cd_dir), True / Errors)
        """
        #--- built make-list ----
        cd_dir = []
        for home in self.get_init('cd'):#- all cd-roots from init-file
            for cds in os.listdir(home):#- cd-path in roots
                cd_dir.append(home + '/' + cds)
        count = len(cd_dir)
        #--- great base_list ---
        #self._base.data['data'].clear()# clear base-list
        for i, path in enumerate(cd_dir):
            state = None
            #------------ greate "CDInfo.txt" file ---------------
            #--- new info-file 'CDInfo.txt' ---
            if os.path.isfile(path + '/' + 'CDInfo.txt'):
                state = self._base_info_check(path)
            else:
                #--- old info-file 'CDIndex.txt' ---'
                if os.path.isfile(path + '/' + 'CDIndex.txt'):
                    state = self._base_info_conv(path)
                else:
                    #--- no info-file ---
                    state = self._base_info_prep(path)
                    if state is True:
                        self.error('base_info_prep',\
                        '[[WARNING _base_info_prep]: edit head-section'+\
                        '(interpret,album....): ' +  path, False)
            #print ('>>> base_make:', path, ':', state)
            self.show_prozess(i, count, cd_dir[i] + ':' + str(state) )
            if state is not True:
                self.error('base_build_cdinfo', state, False)
            else:
                #--- save CDInfo ---
                if save is True:
                    self._info.save(path + '/CDInfo.txt')
        return cd_dir


    def base_make(self, save=True):
        """ make a new "base_main.bas" list for all avaiable cds with "CDInfo.txt"
        save:  save the new "base_main.bas"
        result: True = done, Other = ERROR-message
        """
        state = True
        #--- great base_list ---
        self.error('base_make', '################### make a new "base_main.bas" '+\
                                '###################', False)
        self.error('base_make', '*************           check all CDs          '+\
                                '*************', False)
        cd_list = self._base_build_cdinfo()
        count = len(cd_list)
        self._base.data['data'].clear()# clear base-list
        for i, path in enumerate(cd_list):
            #------------ greate "base_main.bas ---------------
            if os.path.isfile(path + '/' + 'CDInfo.txt'):
                #state = self._base_info_check(path)
                self._base_add_cd(path, val=None, save=True)
                self.show_prozess(i, count, cd_list[i] + ': added')
        self.error('base_make', '###################         end of make        '+\
                                '###################', False)
        #---  edit base-head ---
        self._base.data['head']['date'] = self.get_time()
        self._base.data['head']['count'] = str(count)
        self._base.data['head']['freeNr'] = 'CD' + str(count+1)
        #--- save base-list ---
        if save is True:
            self._base.save()
        return state


    #def base_edit(self, typ, name, val, par=None, save = True):
    def base_edit(self, *par, save = True):
        """ edit par[0](add,del,head,track) in the base-list
        par[0]:add:   par[1] = cd-path with image/track-files, par[2] = header(album...)
               del:   par[1] = cd-path with image/track-files
               head:  par[1] = cd-path, par[2] = new header
               track: par[1] = cd-path, par[2] = old file-name, par[3] = new filename or del("")
               import:par[1] = import-path, par[2] = target-path
        par[1]: edit-name
        par[2]: value for add or file-name
        par[3]: xxx = new-name for file, "" = delet file
        save:   save base_main.bas
        result: True = done, Other = ERROR-message
        """
        state = None
        #----- add new cds with data -----
        if par[0] == 'add':
            state = self._base_add_cd(par[1], par[2])
        #----- delete exist cds and his data -----
        if par[0] == 'del':
            state = self._base_del_cd(par[1])
        #----- edit head of cd -----
        if par[0] == 'head':
            state = self._base_rename_head(par[1], par[2])
            if state is True:
                state = self._base_info_update(par[1])
        #----- rename / remove track -----
        if par[0] == 'track':
            state = self._base_rename_track(par[1], par[2], par[3])
            if state is True:
                state = self._base_info_update(par[1])
        if par[0] == 'import':
            state = self._base_import_cd(par[1], par[2])
            # if state is True:
            #     state = self._base_info_update(par[1])
        #--- save base-list ---
        if save is True:
            self._base.save()
        #--- report message ---
        if state is not True:
            self.error('base-list', state, False)
        return state


    #**************************************************************************
    #************************** list-methoden *********************************
    def list_get(self, numb, typ):
        """ get info(path,image,interpret...) from list-entry
        numb:   Number of list entry
        typ:    Info-Typ: play=full path, imgae,interpret, album, genre, year
                          import, track, track_list, pos, calls
        """
        path = self._list.data['data'][numb][0]
        cd_ = str(path).split('/')[-1]
        track = self._list.data['data'][numb][1][0]
        #print('>>> list_get(path/track):',path,track,cd_) 
        if typ == 'play':
            val = path + '/' + track
        if typ == 'interpret':
            val = self._base.data['data'][cd_]['interpret']
        if typ == 'album':
            val = self._base.data['data'][cd_]['album']
        if typ == 'genre':
            val = self._base.data['data'][cd_]['genre']
        if typ == 'year':
            val = self._base.data['data'][cd_]['year']
        if typ == 'import':
            val = self._base.data['data'][cd_]['import']
        if typ == 'track':
            val = track
        if typ == 'track_list':
            val = self._titel_list(cd_)
        if typ == 'pos':
            #print('>>> list_get:', track)
            val = self._titel_list(cd_, track)[1]
        if typ == 'call':
            val = self._titel_list(cd_, track)[2]
        return val


    def list_edit(self, mode, par1=None, par2=None):
        """ edit(clear,add...) the list-format: [ path,[pos,calls] ]
        mode:   function add,cd=append track(s) from base_list, del=remove track,
                        clear=remove all tracks, ins=insert track before nr
                        head=date & count & (name)
        par1:   add=cd-name, del=list-nr
        par2:   list-position
        """
        if mode =='clear':
            self._list.data['data'].clear()
        if mode == 'add':
            self._list.data['data'].append(par1)
        if mode == 'cd':
            for titel in self._base.data['data'][par1]['tracks']:
                add_items = [self._base.data['data'][par1]['path'], titel]
                self._list.data['data'].append(add_items)
        if mode == 'del':
            self._list.data['data'][par1].clear()
        if mode == 'ins':
            self._list.data['data'].insert(par2,par1)
        if mode == 'head':
            if par1 is not None:
                self._list.data['head']['name'] = par1
            self._list.data['head']['date'] = self.get_time()
            self._list.data['head']['count'] = str(len(self._list.data['data']))


    def list_sort(self, typ, z_a=False):
        """ sort(interpreter,album...) the play-list
        typ:    sort-function = interpret, album, genre, year, import
        value:  Keyword
        a_z:    sort-direction
        """
        sort_list = []
        key = None
        #--- Selection of the sorting expression
        if typ == 'interpret':
            key=['interpret', 'album', 'pos', 'genre', 'year', 'import']
        if typ == 'album':
            key=['album', 'interpret', 'pos', 'genre', 'year', 'import']
        if typ == 'genre':
            key=['genre', 'interpret', 'album', 'pos', 'year', 'import']
        if typ == 'year':
            key=['year', 'interpret', 'album', 'pos', 'genre', 'import']
        if typ == 'import':
            key=['import', 'interpret', 'album', 'pos', 'genre', 'year']
        if key is None:
            self.error('list_sort', '[error] wrong parameter: ' + typ)
        for i in range(0, len(self._list.data['data'])):
            #print('>>> list_sort=', self._list.data['data'][i])
            #--- built sort_key ---
            sort_key = str(self.list_get(i,key[0])) + ':' + str(self.list_get(i,key[1])) +\
            ':' + str(self.list_get(i,key[2])) + ':' +str( self.list_get(i,key[3])) +\
            ':' + str(self.list_get(i,key[4])) + ':' + str(self.list_get(i,key[5]))
            #--- add sort_key + data ---
            sort_list.append([sort_key, self._list.data['data'][i]])
        #--- sort-list save as playlist
        sort_list.sort(reverse = z_a) #- Liste sortieren
        for i, val in enumerate(sort_list):
            self._list.data['data'][i] = val
            #print('>>> sort=', sort_list[i][0])
        #json_show(db._list.data)


    def list_filter(self, typ, value, clear=True):
        """ search(interpret,album...) in base-list after parameter
        typ:    search-function = interpret, album, genre, year, import
        value:  Keyword
        clear:  Clear current list
        """
        def _base_search_cd(key, search, new=True):
            """ search in bas-list
            key:    key in cd-data
            val:    search-value
            """
            cd_ = None
            if new is True:
                self.list_edit('clear',cd_)
            for cd_ in self._base.data['data']:
                val = str(self._base.data['data'][cd_][key]).lower().find(str(search).lower())
                if val >= 0:
                    self.list_edit('cd',cd_)
            self.list_edit('head','neuer Name xxxx')
            return True
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
    print ( db.base_make() )
    db.list_filter('interpret', '')
    db.save('list')
    db.load('list')
    #print(':', db.list_get(0, 'call') )
    db.list_sort('import', False)
    #----------- list_edit ---------------
    # db.list_edit('clear')
    # db.list_edit('cd', 'CD518')
    # db.list_edit('del', 1)
    # db.list_edit('add', ['c:/',['append Titel.wav',1,2]])
    # db.list_edit('ins', ['d:/test/',['insert Titel.wav',3,4]],1)
    #json_show(db._list.data)
    #print (db.get_init('lastPlay'))
    #print ( db.base_make(db.base_build_cdinfo()))
    head = {'interpret': '1.test_header', 'album': '2.', 'genre': '3.Rock', \
            'year': '4.2022', 'import': '__12.08.2022'}
    #print(db.base_edit('import', 'D:/_Test_CD/Import', 'D:/_Test_CD/Audio' ))
    #print(db.base_edit('head', 'D:/_Test_CD/Archiv3/new_add', head))#'Take_4.wav', 'Take 4.wav'))
    print('----------------------------------------------')
    json_show(db._base.data)
    assert False, 'Stop'
