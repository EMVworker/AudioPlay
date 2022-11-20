# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 23:16:41 2022

1@author: juergen1
"""
import pygame as play

class PgAudio():
    """ Audio-Player from pygame-modul
    """
    def __init__(self):
        """ init pygame mixer modul """
        play.mixer.init(44100, 16, 2, play.AUDIO_ALLOW_ANY_CHANGE)
        self._audio_file = ''

    def play(self, file):
        """ play current audio_file
        file:   audio file
        return: True = OK or Error
        """
        self._audio_file = file
        play.mixer.music.load(self._audio_file)
        play.mixer.music.play()

    def stop(self):
        """ stop currently playing
        """
        play.mixer.music.stop()

    def pause(self):
        """ pause for currently playing
        """
        play.mixer.music.pause()

    def unpause(self):
        """ play after pause
        """
        play.mixer.music.unpause()

    def getting(self, typ):
        """ restart currently playing
        pos:    currebtly position of playing
        """
        state = None
        if typ == 'state':
            state = play.mixer.music.get_busy()
        if typ == 'pos':
            state = play.mixer.music.get_pos()
        if typ == 'init':
            state = play.mixer.get_init()
        if typ == 'ch':
            state = play.mixer.get_num_channels()
        if typ == 'ver':
            state = play.mixer.get_sdl_mixer_version()
        return state

    def setting(self, typ, val):
        """ set playing-position
        """
        state = None
        if typ == 'pos':
            state = play.mixer.music.set_pos(val)
        return state


# =================== Modul Test =======================
if __name__ == '__main__':
    def help_txt():
        print('***** Audio-Player *****')
        print('* 1 = play track1')
        print('* 2 = play track2')
        print('* s = stop')
        print('* p = pause')
        print('* u = unpause')
        print('* 5 = Info position')
        print('* 6 = Info sample/bit/channels')
        print('* 7 = Info of available channels')
        print('* 8 = Info of version')
        print('* b = get busy-flag')
        print('* f = set position')
        print('* h = show help-text')
        print('* q = exit')
        print('************************')
    play.init()
    pg = PgAudio()
    key = ''
    help_txt()
    while key != 'q':
        key = input('>>> ?(h=help)')
        if key == '1':
            print(pg.play('test.wav'))
        if key == '2':
            print(pg.play('test1.wav'))
        if key == 's':
            print(pg.stop())
        if key == 'p':
            print(pg.pause())
        if key == 'u':
            print(pg.unpause())
        if key == '5':
            print(pg.getting('pos'))
        if key == '6':
            print(pg.getting('init'))
        if key == '7':
            print(pg.getting('ch'))
        if key == '8':
            print(pg.getting('ver'))
        if key == 'b':
            print(pg.getting('state'))
        if key == 'f':
            print(pg.setting('pos', 10000.0))
        if key == 'h':
            help_txt()
    print('>>>> Audio-Player exit <<<<')
            
        