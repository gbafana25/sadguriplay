from PyQt5 import QtWidgets, QtCore, uic 
import json
import os
import vlc
import backend

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Gui(object):

	def load(self):
		super(Gui, self).__init__()
		uic.loadUi('homescreen.ui', self)
		self.show()

class VidPlayer(QtWidgets.QMainWindow, Gui):
    player = vlc.MediaPlayer()
    def __init__(self):
        super().__init__()
        self.load()

        self.playbtn.clicked.connect(self.playTrack)
        self.pausebtn.clicked.connect(self.pauseTrack)
        self.downloadbtn.clicked.connect(self.downloadTrack)
        self.refresh_playlistbtn.clicked.connect(self.refreshPlaylist)
        self.getPlaylist()
        #self.songlist.insertItem(0, "test")

    def getPlaylist(self):
          with open("new_playlist.json", "r") as playlist:
                data = json.load(playlist)
                for d in data['idList']:
                      self.songlist.addItem(d['title'])

    def refreshPlaylist(self):
        self.songlist.clear()
        self.getPlaylist()

    def replaceTitle(self, old_title, new_title):
        pdata = None 
        with open("new_playlist.json", "r") as playlist:
            pdata = json.load(playlist)
        for d in pdata['idList']:
            if d['title'] == old_title:
                 d['title'] = new_title
        with open("new_playlist.json", "w") as playlist:
             json.dump(pdata, playlist)

    def playTrack(self):
          selected_song = self.songlist.currentItem().text()
          
          # get file w/ name matching selected_song
          
          #self.player = vlc.MediaPlayer("file:///home/gareth/vid-player/songs/"+selected_song+".mp3")
          if selected_song != None:
            self.player.set_mrl("file:///home/gareth/vid-player/songs/"+selected_song+".mp3")
            if self.player.is_playing():
                print(self.player.get_media())
                self.player.stop()
            # play song
            self.player.play()
            self.curr_song.setText(selected_song)

    def stopTrack(self):
        self.player.stop()

    def pauseTrack(self):
        self.player.pause()

    def downloadTrack(self):
        selected_song = self.songlist.currentItem().text() 
        song_data = {}
        with open("new_playlist.json", "r") as playlist:
            data = json.load(playlist)
            for d in data['idList']:
                if selected_song == d['title']:
                     # if file name > x characters, shorten and change in playlist 
                    before_len = len(selected_song)
                    orig_title = selected_song
                    selected_song = selected_song.replace("|", "").replace(" ", "").replace("(", "").replace(")", "").replace("/", "")
                    after_len = len(selected_song)
                    if before_len != after_len:
                        # replace title
                        self.replaceTitle(orig_title, selected_song)
                    song_data = d
                    #song_data['title'] = selected_song

                    backend.downloadVideo(song_data['id'], selected_song)
                    self.refreshPlaylist()