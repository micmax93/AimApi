__author__ = 'micmax93'

import vlc
import time

class Player(object):
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.list = self.instance.media_list_new()
        self.manager = self.instance.media_list_player_new()
        self.manager.set_media_player(self.player)
        self.manager.set_media_list(self.list)
        self.manager.set_playback_mode(vlc.PlaybackMode.loop)
        self.player.set_fullscreen(1)

    def play(self):
        self.manager.play()

    def pause(self):
        self.manager.pause()

    def stop(self):
        self.manager.stop()

    def next(self):
        self.manager.next()

    def remaining_time(self):
        return self.player.get_length()*(1-self.player.get_position())

    def clear(self):
        while self.list.remove_index(0) == 0:
            pass

    def add(self, mrl):
        media = self.instance.media_new(mrl)
        self.list.insert_media(media, self.list.count())

    def remove(self, index=0):
        self.list.remove_index(index)


class SinglePlayer(Player):
    def set_next(self, mrl, auto_play=True):
        self.clear()
        media = self.instance.media_new(mrl)
        self.list.insert_media(media, 0)
        if (not self.manager.is_playing()) and auto_play:
            self.play()

    def wait(self, margin=0.0):
        t = self.remaining_time()-margin
        time.sleep(t/1000.0)
