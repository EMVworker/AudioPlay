# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 12:07:58 2022

@author: juergen
"""
import json

def json_show(data):
        """ save data-struct in file
        file:   name of json-File
        """
        data =json.dumps(data, indent=4)
        print(data)
        return data

class JsonData():
    """ json-format for data creation with "Typ-Check *.xxx"
    1. load data-template with unique extension as format
    2. only use files with same extension
    """
    def __init__(self, template_name):
        """ init
        template_name:  name of the data-struct format, Set the data extension
        """
        self.data = None
        self._template = template_name
        self._ext = template_name.split('.')[1]
        self.load()
        
    def error(self, source, msg):
        """ error handler
        source: occurrence of the error
        msg:    Error-Infotext
        result: Error-Infotext
        """
        error = '<Extension *.' + self._ext + ' @ ' + source + '>: ' + str(msg)
        #print(JsonData.__name__)
        assert False, error
        return(error)

    def load(self, file=''):
        """ load data-struct from file
        file:   name of json-File
        return: data-struct 
        """
        if file == '':
            file = self._template
        else:
            if file.find(self._ext) <= 0:
                self.error('load', '[warning] wrong data-struct: ' + file)
        try:
            with open(file, 'r') as f:
                self.data = json.load(f)
        except (IOError, ValueError) as msg:
            self.error('load', msg)
        return self.data

    def save(self, file=None):
        """ save data-struct in file
        file:   name of json-File
        """
        if file is None:
            file = self._template
        else:
            if file.find(self._ext) <= 0:
                self.error('save', '[warning] wrong data-struct: ' + file)
        try:
            with open(file, 'w') as f:
                json.dump(self.data, f, ensure_ascii = False, indent=4)
        except(IOError, ValueError) as msg:
            self.error('save', msg)
        return self.data
    
    def show(self, data):
        """ save data-struct in file
        file:   name of json-File
        """
        try:
            data =json.dumps(self.data, indent=4)
        except(IOError, ValueError) as msg:
            self.error('show', msg)
        return data

# =================== Modul Test =======================
if __name__ == '__main__':
    db = JsonData('load_main.txt')
    #print(db.load('load_main.txt'))
    print(db.load())
    db.save('save_test.txt')
    #print(db.data)
    json_show(db.data)


