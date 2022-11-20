# -*- coding: utf-8 -*-
"""
Created on 08.09.2022 @ 20:04

1@author: juergen1
"""
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
import sys


class QtPlayer():
    """ Audio-Player from qt5.QMediaPlayer
        use for audio-tracks & internet-Radio
    """
    def __init__(self, callback=[None,None,None], interval=500, volume=100):
        """ init Qt5.Media-Player:\n
        - callback:   [0]=on_state, [1]=on_pos, [2]=on_media:\n
        - interval:   time in sec for update callbacks:\n
            - "on_state" = player-state (stop, play, pause)\n
            - "on_pos" = position in ms:\n
            - "on_media" = stream state:\n
        - volume:     audio-volume 0...100:\n
        return::\n
        """
        self.__audioPlayback = QMediaPlayer()
        self.__audioPlayback.setVolume(volume)
        self.__audioPlayback.stateChanged.connect(self.on_state)
        self.__audioPlayback.positionChanged.connect(self.on_pos)
        self.__audioPlayback.mediaStatusChanged.connect(self.on_media)
        self.__audioPlayback.setNotifyInterval (interval)
        self.callback = callback

    def on_state(self, state):
        """ callback state of player
        state: 0=stop, 1=play, 2=pause
        """
        if self.callback[0] is not None:
            self.callback[0]()
        else:
            print ('- QtPlayer State:', state)

    def on_pos(self, position):
        """ callback position of titel
        position:   time in ms
        """
        if self.callback[1] is not None:
            self.callback[1]()
        else:
            print ('- QtPlayer Postiton:', position)

    def on_media(self, media):
        """ callback player-media is changed
        *** media-Status ***
        0 = UnknownMediaStatus: The status of the media cannot be determined.
        1 = NoMedia: There is no current media. The player is in the StoppedState.
        2 = LoadingMedia: The current media is being loaded. The player may be in any state.
        3 = LoadedMedia: The current media has been loaded. The player is in the StoppedState.
        4 = StalledMedia:Playback of the current media has stalled due to insufficient buffering or some other temporary interruption. The player is in the PlayingState or PausedState.
        5 = BufferingMedia: The player is buffering data but has enough data buffered for playback to continue for the immediate future. The player is in the PlayingState or PausedState.
        6 = BufferedMedia: The player has fully buffered the current media. The player is in the PlayingState or PausedState.
        7 = EndOfMedia: Playback has reached the end of the current media. The player is in the StoppedState.
        8 = InvalidMedia: The current media cannot be played. The player is in the StoppedState.0 = UnknownRole: The role is unknown or undefined
        """
        if self.callback[2] is not None:
            self.callback[2]()
        else:
            print ('- QtPlayer MediaState:', media)

    def play(self, path):
        """ play current audio_file
        file:   audio file
        return: None = OK or Error
        """
        content = QMediaContent(QUrl(path))
        self.__audioPlayback.setMedia(content)
        return  self.__audioPlayback.play()

    def stop(self):
        """ stop currently playing
        """
        return self.__audioPlayback.stop()

    def pause(self):
        """ pause for currently playing
        """
        if self.__audioPlayback.state() == QMediaPlayer.PlayingState:
            return self.__audioPlayback.pause()

    def unpause(self):
        """ play after pause
        """
        if self.__audioPlayback.state() == QMediaPlayer.PausedState:
            return self.__audioPlayback.play()

    def get_pos(self):
        """ get currently position
        """
        #if self.__audioPlayback.state() == QMediaPlayer.PlayingState:
        return self.__audioPlayback.position()

    def set_pos(self, position):
        """ set currently position
        position:   position in ms
        """
        return self.__audioPlayback.setPosition(int(position))

    def get_vol(self):
        """ get volume 0...100
        """
        return self.__audioPlayback.volume()

    def set_vol(self, volume):
        """ set volume 0...100
        """
        return self.__audioPlayback.setVolume(int(volume))

    def get_time(self):
        """ get duration in ms
        """
        return self.__audioPlayback.duration()

    def get_state(self):
        """ get state of play: 0=stop, 1=play, 2=pause
        """
        return self.__audioPlayback.state()

    def get_info(self):
        """ get get Meta-Data from Audio-Stream
        return:     dict[available datatype : value]
        """
        data = {}
        keys = self.__audioPlayback.availableMetaData()
        for key in keys:
            data[key] = self.__audioPlayback.metaData(key)
        return data

    def get_error(self):
        """ get error 
        **** errors:****
        0 = NoError: No error has occurred.
        1 = ResourceError: A media resource couldn't be resolved.
        2 = FormatError: The format of a media resource isn't (fully) supported. Playback may still be possible, but without an audio or video component.
        3 = NetworkError: A network error occurred.
        4 = AccessDeniedError: There are not the appropriate permissions to play a media resource.
        5 = ServiceMissingError:  valid playback service was not found, playback cannot proceed.time in ms
        """
        return self.__audioPlayback.error()


# =================== Modul Test =======================
if __name__ == '__main__':
    def help_txt():
        print('***** Audio-Player *****')
        print('* 1 = play track1')
        print('* 2 = play track2')
        print('* 3 = internet-Radio1')
        print('* 4 = internet-Radio2')
        print('* s = stop')
        print('* p = pause')
        print('* u = unpause')
        print('* 5 = get Volume')
        print('* 6 = set position')
        print('* 7 = get Volume')
        print('* 8 = set Volume')
        print('* t = time(duration)')
        print('* e = get error')
        print('* m = get media-status')
        print('* i = get stream meta-data')
        print('* h = show help-text')
        print('* q = exit')
        print('************************')
    app = QApplication(sys.argv)
    pg = QtPlayer()
    key = ''
    url1 = 'https://f111.rndfnk.com/ard/swr/swr2/live/mp3/256/stream.mp3?aggregator=web&sid=28ew6Usq6cch83eglcsXwLlNRS3&token=Ip5bwQ_T81Lq_mqKc3HUjnxrk94ek2bDcfNyNHuqRGk&tvf=XFsRgyq06xZmMTExLnJuZGZuay5jb20'
    url2 = 'http://channels.webradio.antenne.de/black-beatz'
    help_txt()
    while key != 'q':
        key = input('>>> ?(h=help)')
        if key == '1':
            print(pg.play('D:/Projekte/PyAudioPlay/AudioPlay_V0/files/test.wav'))
        if key == '2':
            print(pg.play('D:/Projekte/PyAudioPlay/AudioPlay_V0/files/test1.wav'))
        if key == '3':
            print(pg.play(url1))
        if key == '4':
            print(pg.play(url2))
        if key == 's':
            print(pg.stop())
        if key == 'p':
            print(pg.pause())
        if key == 'u':
            print(pg.unpause())
        if key == '5':
            print(pg.get_pos())
        if key == '6':
            val = input('>>> Position ?:')
            print(pg.set_pos(val))
        if key == '7':
            print(pg.get_vol())
        if key == '8':
            val = input('>>> Volume: ?')
            print(pg.set_vol(val))
        if key == 't':
            print(pg.get_time())
        if key == 'e':
            print(pg.get_error())
        if key == 'm':
            pg.on_media()
        if key == 'i':
            print ( pg.get_info() )
        if key == 'h':
            help_txt()
    print(pg.stop())
    #sys.exit(app.exec_())
    print('>>>> Audio-Player exit <<<<')
