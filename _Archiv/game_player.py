# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 23:16:41 2022

@author: juergen
"""
import pygame
from threading import Timer

class InfinityTimer(Timer):
    """ InfinityTimer(Interval(sec), Call-Function) --> start()=start / cancel()=Stop
    self.timer = InfinityTimer(1, self.end), self.timer.start(), drlf.timer.cancel()
    """
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class PgAudio():
    """ Audio-Player from pygame-modul
        use for audio-tracks based on SDL2_Audio
    """
    def __init__(self, interval=0.1, frq=44100, bit=16, ch_=2, buf = 512, dev=None):
        """ init pygame mixer modul
        interval: time in sec for update callbacks "cb_end" or ....
        frq:    sample-rate (44100Hz, 48000Hz, 98000Hz)
        bit:    solution 16 -16(unsigned) 32
        cd_:    numb of channel 1(Mono), 2(Stereo), 4(Quad) 6(Surrond)
        buf:    low val = öow latenz, high val = less drop-out
        dev:    name of audiodevice
        (opt:)  AUDIO_ALLOW_FREQUENCY_CHANGE / AUDIO_ALLOW_FORMAT_CHANGE
                AUDIO_ALLOW_CHANNELS_CHANGE / AUDIO_ALLOW_ANY_CHANGE
        """
        pygame.init()
        pygame.mixer.init(frq, bit, ch_, buf, dev)
        self._audio_file = ''
        self.MUSIC_END = pygame.USEREVENT+1
        pygame.mixer.music.set_endevent(self.MUSIC_END)
        self.timer = InfinityTimer(interval, self.end)
        self.timer.start()
        self.cb_end = None
        self.cb_interval = None

    def __del__(self):
        """ deinit (destructor) timer  & pygame"""
        self.timer.cancel()
        pygame.quit()

    def end(self):
        """ callback "cb_end" if titel finished
            callback every interval "cb_interval"
        """
        for event in pygame.event.get():
            if event.type == self.MUSIC_END:
                if self.cb_end is not None:
                   self.cb_end()
        if self.cb_interval is not None:
            self.cb_interval()

    def init(self, frq=44100, bit=16, ch_=2, buf = 512, dev=None):
        """ new init of the audio-device (description in __init__)
        """
        return pygame.mixer.pre_init(frq, bit, ch_, buf, dev)

    def play(self, file):
        """ play current audio_file
        file:   audio file
        return: True = OK or Error
        """
        self._audio_file = file
        pygame.mixer.music.load(self._audio_file)
        return pygame.mixer.music.play()

    def stop(self):
        """ stop currently playing
        """
        return pygame.mixer.music.stop()

    def pause(self):
        """ pause for currently playing
        """
        return pygame.mixer.music.pause()

    def unpause(self):
        """ play after pause
        """
        return pygame.mixer.music.unpause()

    def getting(self, typ):
        """ restart currently playing
        *** Typ ***:
        -state:  True=played, False=not played
        -pos:    currently Audio-Pos
        -init:   sample-Frq/Solution/Channels/Changing
        -ch:     numb of used channel
        -ver:    version of pygame
        -vol:    volume of audio(0....1)
        -end:    True = end of track
        return:  value of function
        """
        state = False
        if typ == 'state':
            state = pygame.mixer.music.get_busy()
        if typ == 'pos':
            state = pygame.mixer.music.get_pos()
        if typ == 'init':
            state = pygame.mixer.get_init()
        if typ == 'ch':
            state = pygame.mixer.get_num_channels()
        if typ == 'ver':
            state = pygame.mixer.get_sdl_mixer_version()
        if typ == 'vol':
            state = pygame.mixer.music.get_volume()
        if typ == 'end':
            for event in pygame.event.get():
                if event.type == self.MUSIC_END:
                    state = True
        return state

    def setting(self, typ, *val):
        """ set playing-position /volume
        *** typ: ***
        -pos:    setting track-pos(not wav),
        -vol:    set volume(0...1)
        val:    value of setting
        return:
        """
        state = False
        if typ == 'pos':
            pygame.mixer.music.set_pos(val[0])
        if typ == 'vol':
            pygame.mixer.music.set_volume(val[0])
        return state

class PgSound():
    """ Audio-Sounds from pygame-modul
        only for short effects
    """
    def __init__(self):
        """ init pygame mixer modul """
        pygame.init()
        pygame.mixer.init(44100, 16, 2)
        self.sound = None

    def play(self, file):
        """ sound-play current audio_file
        file:   audio file
        return: True = OK or Error
        """
        self._audio_file = file
        self.sound = pygame.mixer.Sound(self._audio_file)
        self.sound.play()

    def stop(self):
        """ stop currently playing
        """
        self.sound.stop()

    def getting(self, typ):
        """ restart currently playing
        pos:    currebtly position of playing
        """
        state = None
        if typ == 'len':
            state = self.sound.get_length()
        if typ == 'raw':
            state = self.sound.get_raw()
        if typ == 'ch':
            state = self.sound.get_num_channels()
        if typ == 'vol':
            state = self.sound.get_volume()
        return state

    def setting(self, typ, val):
        """ set playing-position
        """
        state = None
        if typ == 'vol':
            state = self.sound.set_volume(val)
        return state

# =================== Modul Test =======================
if __name__ == '__main__':
    def end_music():
        print('>>>> Titel finished:')
    def pos_music():
        print(pg.getting('pos'))
    def help_txt():
        print('***** Audio-Player *****')
        print('* 1 = play track1')
        print('* 2 = play track2')
        print('* s = stop')
        print('* p = pause')
        print('* u = unpause')
        print('* 5 = Info position(len)')
        print('* 6 = Info sample/bit/channels')
        print('* 7 = Info of available channels(ch)')
        print('* 8 = Info of version')
        print('* b = get busy-flag(raw)')
        print('* v = get volume')
        print('* f = set position')
        print('* ' ' = test end file')
        print('* h = show help-text')
        print('* q = exit')
        print('************************')
    pg = PgAudio(1)
    pg.cb_end = end_music
    pg.cb_interval = pos_music
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
            #print(pg.getting('len'))
        if key == '6':
            print(pg.getting('init'))
        if key == '7':
            print(pg.getting('ch'))
            #print(pg.getting('ch'))
        if key == '8':
            print(pg.getting('ver'))
        if key == 'b':
            print(pg.getting('state'))
            #print(pg.getting('raw'))
        if key == 'v':
            print(pg.getting('vol'))
            #print(pg.getting('vol'))
        if key == 'f':
            print(pg.setting('pos', 10000.0))
            #print(pg.init())
        if key == ' ':
            print(pg.getting('end'))
        if key == 'h':
            help_txt()
    print('>>>> Audio-Player exit <<<<')
    pg.__del__()
    
        