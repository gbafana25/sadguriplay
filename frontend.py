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
    player = None
    def __init__(self):
        super().__init__()
        self.load()

        self.playbtn.clicked.connect(self.playTrack)
        self.stopbtn.clicked.connect(self.stopTrack)
        self.pausebtn.clicked.connect(self.pauseTrack)
        self.downloadbtn.clicked.connect(self.downloadTrack)
        self.getPlaylist()
        #self.songlist.insertItem(0, "test")

    def getPlaylist(self):
          with open("new_playlist.json", "r") as playlist:
                data = json.load(playlist)
                for d in data['idList']:
                      self.songlist.addItem(d['title'])

    def playTrack(self):
          selected_song = self.songlist.currentItem().text()
          # get file w/ name matching selected_song
          # play song
          self.player = vlc.MediaPlayer("file:///home/gareth/vid-player/songs/"+selected_song+".mp3")
          self.player.play()

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
                    song_data = d
        #print(song_data)

        backend.downloadVideo(song_data['id'], song_data['title'])