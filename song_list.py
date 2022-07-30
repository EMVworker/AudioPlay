# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 12:07:58 2022

@author: juergen
"""
from json_data import JsonData
from json_data import json_show

class SongList():
    """ json-format for data creation
    """
    def __init__(self):
        """ init
        Set the data-struct
        """
        #--- Daten-Strukturen laden ---
        self._base = JsonData('base_main.bas')
        self._list = JsonData('list_search.lst')
        self._init = JsonData('AudioPlay.ini')
        self._info = JsonData('info_cd.txt')

    def list_get(self, numb, typ):
        """ get info from list-entry
        nr:     Number of list entry
        typ:    Info-Typ: play=full path, imgae,interpret, album, genre, year
                          import, track, track_list, pos, calls
        """
        def _titel_list(cd_, name=None):
            """select titel & titel-paramter from base-list
            cd_:     cd_-Name
            name:   None = Titel-Liste, xxx: result[0]=position result[1]=calls
            """
            val=[]
            for titel in self._base.data[cd_]['tracks']:
                val.append(titel[0])
            if name is not None:
                index = val.index(name)
                val = self._base.data[cd_]['tracks'][index]
            return val
        path = self._list.data['item'][numb][0]
        cd_ = str(path).split('/')[-1]
        track = self._list.data['item'][numb][1]
        if typ == 'play':
            val = path + '/' + track
        if typ == 'interpret':
            val = self._base.data[cd_]['interpret']
        if typ == 'album':
            val = self._base.data[cd_]['album']
        if typ == 'genre':
            val = self._base.data[cd_]['genre']
        if typ == 'year':
            val = self._base.data[cd_]['year']
        if typ == 'import':
            val = self._base.data[cd_]['import']
        if typ == 'track':
            val = track
        if typ == 'track_list':
            val = _titel_list(cd_)
        if typ == 'pos':
            val = _titel_list(cd_, track)[1]
        if typ == 'call':
            val = _titel_list(cd_, track)[2]
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
            self._list.data['item'].clear()
        if mode == 'add':
            self._list.data['item'].append(par1)
        if mode == 'cd':
            for titel in self._base.data[par1]['tracks']:
                add_items = [self._base.data[par1]['path'], titel]
                self._list.data['item'].append(add_items)
        if mode == 'del':
            self._list.data['item'][par1].clear()
        if mode == 'ins':
            self._list.data['item'].insert(par2,par1)
        if mode == 'head':
            if par1 is not None:
                 self._list.data['head']['name'] = par1
            self._list.data['head']['date'] = 'neue Zeit'
            self._list.data['head']['count'] = str(len(self._list.data['item']))
    
    def list_filter(self, typ, value, clear=True, list_find='list_search.lst'):
        """ search in base-list after parameter-list
        typ:    search-function = interpret, album, genre, year, import, tracks, calls
        value:  Keyword
        clear:  Clear current list
        """
        def _base_search(key, val):
            """ search in bas-list
            key:    key in cd-data
            val:    search-value
            """
            cd_ = None
            if clear is True:
                self.list_edit('clear',cd_)
            for cd_ in self._base.data:
                if cd_ != 'head':
                    val = str(self._base.data[cd_][key]).lower().find(str(value).lower())
                    if val >= 0:
                        self.list_edit('cd',cd_)
            self.list_edit('head','neuer Name xxxx')
        val=None
        if typ == 'interpret':
            _base_search('interpret', val)
        if typ == 'album':
             _base_search('album', val)
        if typ == 'genre':
            _base_search('genre', val)
        if typ == 'year':
            _base_search('year', val)
        if typ == 'import':
            _base_search('import', val)
        if typ == 'track':
            pass#val = track
        if typ == 'call':
            pass#val = titel_list(cd_, track)[2]
        return val
        

# =================== Modul Test =======================
if __name__ == '__main__':
    db = SongList()
    val = None
    print(db._base.data['CD12']['path'])
    json_show(db._list.data)
    # print()
    # print(db._init.data)
    # print()
    # print(db._info.data)
    db.list_filter('year', '2002')
    json_show(db._list.data)
    #print(db.list_get(0, 'titel_list'))
    #----------- list_edit ---------------
    # db.list_edit('clear')
    # db.list_edit('cd', 'CD518')
    # db.list_edit('del', 1)
    # db.list_edit('add', ['c:/',['append Titel.wav',1,2]])
    # db.list_edit('ins', ['d:/test/',['insert Titel.wav',3,4]],1)
    # json_show(db._list.data)
