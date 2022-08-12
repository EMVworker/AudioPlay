# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 12:07:58 2022

@author: juergen
"""
import time
import os
import copy
import logging
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
             level=logging.INFO, format='%(asctime)s')
        #fh = logging.FileHandler(log_file)
        # #h.setLevel(logging.INFO)
        # #fh.setFormatter(formater)
        #self.log = logging.getLogger(log_file)
        #self.log.setLevel(logging.INFO)
        #self.log.addHandler(fh)
        #log_init(log_file)


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


    def get_time(self, typ='date_time'):
        """ give the time
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


    def save(self, typ, file=None):
        """select titel & titel-paramter from base-list
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
        """select titel & titel-paramter from base-list
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
        """ read settings from ini-file
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


    def base_info_check(self, path, info_file='CDInfo.txt'):
        """ check the cd-root and the CDInfo-File
        path:       path to the cd
        info_file:  Name of InfoFile
        return:     info-data
        """
        file_list = os.listdir(path)# list all files & paths
        del_list = copy.deepcopy(file_list)
        #--- read CDInfo.txt ---
        home = path + '/' + info_file
        self._info.load(home)
        home = path + '/'
        #--- check tracks in CDInfo-File ---
        for track in self._info.data['tracks']:
            if (track[0] in file_list) is False:
                self.error('base_info_check', 'Tracks not found: ' + home + track[0], False)
            else:
                del_list.remove(track[0])
        #--- check images in CDInfo-File ---
        for image in self._info.data['image']:
            if (image in file_list) is False:
                self.error('base_info_check', 'Image not found:' + home + image, False)
            else:
                del_list.remove(image)
        #--- clear del-list ---
        try:
            del_list.remove(info_file)
            del_list.remove('CDInfo.txt')
        except:
            pass
        #--- check if files unuesd ---
        for file in del_list:
            #--- unknows files ---
            self.error('base_info_check', 'Unknow files:' + home + file, False)
        return self._info.data


    def base_info_conv(self, path, info_file='CDIndex.txt'):
        """ tranfer "info_file" in "CDInfo.txt" format
        path:       path to the cd
        info_file:  name of infoFile
        return:     CDIndex-File
        """
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
                    for pos in enumerate(val1[0]):
                        if pos.isdigit():
                            nr_ = nr_ + pos
                    state = [val1[0], val2[0].replace('\n',''), nr_]
                    #print ('>>> cut:', val1[0], val2[0])
            except:
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
                val.append( [tmp[1], int(tmp[2]), 0] )
        self._info.data['tracks'] = val
        return cd_index


    def base_info_prep(self, path):
        """ prepered for a new  cdinfo text-block (not all infos available)
        path:       path to the cd
        return:     CDInfo-File
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
        file_list = os.listdir(path)# list all files & paths
        val = ['interpret', 'album', 'genre', 'year', 'import']
        #--- infos convertieren ---
        self._info.data['path'] = path
        for key in val:
            self._info.data[key] = '<unknow>'
        #--- tracks listen ---
        val =[]
        i=1
        for key in file_list:
            #tmp = file_find('image', key)
            #if key.find('.wav') > 0:
            if file_find('track', key) > 0:
                val.append([key, i, 0])
                i += 1
        self._info.data['tracks'] = val
        #--- image listen ---
        #file_list.sort(reverse=True)
        for key in file_list:
            #if key.find('.jpg') > 0:
            if file_find('image', key) > 0:
                self._info.data['image'].append(key)
        return self._info.data


    def base_make(self, save_info=False):
        """ build a new base-list for available tracks
        save_info:  save CDInfo.txt in cd path
        result: CDInfo/CDIndex
        """
        val = None
        path = self.get_init('cd')# all available paths
        val = os.listdir(path[0])# first path with all cds
        path = path[0] + '/' + val[0]
        #------------ greate "CDInfo.txt" file ---------------
        #--- new info-file 'CDInfo.txt' ---
        if os.path.isfile(path + '/' + 'CDInfo.txt'):
            val = self.base_info_check(path)
            #print('>>> base_make:', '"CDInfo.txt" is checked"')
            self.error('base_info_check', '----- "CDInfo.txt" is checked" -----', False)
        else:
            #--- old info-file 'CDIndex.txt' ---'
            if os.path.isfile(path + '/' + 'CDIndex.txt'):
                val = self.base_info_conv(path)
                #print('>>> base_make:', '"CDIndex.txt" convert to "CDinfo.txt"')
                self.error('base_info_check',\
                    '----- "CDIndex.txt" convert to "CDinfo.txt" -----', False)
            else:
                #--- no info-file ---
                val = self.base_info_prep(path)
                #print('>>> base_make:', 'No Info-File available')
                self.error('base_info_check', '----- No Info-File available -----', False)
        if val is None:
            self.error('base_make', '[error] wrong parameter: ')
        else:
            #--- save CDInfo ---
            if save_info is True:
                self._info.save(self._info.data['path'] + '/CDInfo.txt')
        return val, path

    def list_get(self, numb, typ):
        """ get info from list-entry
        numb:   Number of list entry
        typ:    Info-Typ: play=full path, imgae,interpret, album, genre, year
                          import, track, track_list, pos, calls
        """
        path = self._list.data['data'][numb][0]
        cd_ = str(path).split('/')[-1]
        track = self._list.data['data'][numb][1][0]
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
            #print('>>> Get:', track)
            val = self._titel_list(cd_, track)[1]
        if typ == 'call':
            val = self._titel_list(cd_, track)[2]
        #print('>>> path, cd_, track',path,cd_,track)
        return val


    def list_edit(self, mode, par1=None, par2=None):
        """ edit the list add-format: [ path,[pos,calls] ]
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
        """ sort the play-listsort
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
        """ search in base-list after parameter-list
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


# =================== Modul Test =======================
if __name__ == '__main__':
    db = SongList()#'D:/Projekte/PyAudioPlay/AudioPlay_V0/report.log')
    #json_show(db._base.data)
    # print(db._init.data)
    # print(db._info.data)
    db.list_filter('interpret', '')
    #json_show(db._list.data)
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
    print ( db.base_make())
    print('----------------------------------------------')
    json_show(db._info.data)
