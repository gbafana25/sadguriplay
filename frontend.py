from PyQt5 import QtWidgets, QtCore, uic 
from PyQt5.QtCore import QTimer
import json
import vlc
import backend
import time

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Gui(object):

	def load(self):
		super(Gui, self).__init__()
		uic.loadUi('homescreen.ui', self)
		self.show()

class VidPlayer(QtWidgets.QMainWindow, Gui):
    player = vlc.MediaPlayer()
    curr_volume_level = 0
    search_data = {}

    def __init__(self):
        super().__init__()
        self.load()

        self.playbtn.clicked.connect(self.playTrack)
        self.pausebtn.clicked.connect(self.pauseTrack)
        self.downloadbtn.clicked.connect(self.downloadTrack)
        self.refresh_playlistbtn.clicked.connect(self.refreshPlaylist)
        self.volume_control.setRange(0, 100)
        self.volume_control.setValue(50)
        self.volume_label.setText("50")
        self.player.audio_set_volume(50)
        self.volume_control.setSingleStep(5) 
        self.search_btn.clicked.connect(self.runSearch)
        self.online_dloadbtn.clicked.connect(self.downloadOnline)
        self.volume_control.valueChanged.connect(self.getVolume)
        self.getPlaylist()
        #self.getVolume()
        #self.songlist.insertItem(0, "test")

    def runSearch(self):
        term = self.search_bar.text()
        self.search_data = backend.searchVideos(term)
        self.songlist.clear()
        for r in self.search_data:
            if r['type'] == 'video':
                # put in playlist view
                #print(r['title'])
                self.songlist.addItem(r['title'])
        self.online_dloadbtn.setEnabled(True)

    def getPlaylist(self):
          with open("new_playlist.json", "r") as playlist:
                self.search_data = json.load(playlist)
                for d in self.search_data['idList']:
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

            self.elapsed_timer = QTimer(self)
            self.elapsed_timer.timeout.connect(self.updateDuration)
            time.sleep(2)
            dur_seconds = int((self.player.get_length() / 1000)%60)
            dur_minutes = int((self.player.get_length() / 1000 / 60)%60)
            self.duration_label.setText(str(dur_minutes)+":"+"{0:02d}".format(dur_seconds))
            self.elapsed_timer.start(5)
            
            self.time_bar.setMaximum(self.player.get_length())

    def updateDuration(self):
        seconds = int((self.player.get_time() / 1000) % 60)
        minutes = int((self.player.get_time() / 1000 / 60)  % 60)
        self.curr_time.setText(str(minutes)+":"+"{0:02d}".format(seconds))
        self.time_bar.setValue(self.player.get_time())
        self.update()
        self.time_bar.setValue(self.player.get_time())

    def stopTrack(self):
        self.player.stop()

    def pauseTrack(self):
        self.player.pause()
        #self.curr_time.setText('{0:.2f}'.format((self.player.get_time() / 1000)/60))
    
    def getVolume(self, value):
         #self.curr_volume_level = str(self.player.audio_get_volume())
         #self.volume_label.setText(self.curr_volume_level)
        self.volume_label.setText(str(value))
        self.player.audio_set_volume(value)

    def downloadOnline(self):
        selected_song = self.songlist.currentItem().text()
        all_songs = {}
        new_title = None
        for s in self.search_data:
            if s['type'] == 'video' and s['title'] == selected_song:
                #print(s['title'], s['videoId'])
                with open("new_playlist.json", "r") as playlist:
                    all_songs = json.load(playlist)
                    new_title = selected_song.replace("|", "").replace(" ", "").replace("(", "").replace(")", "").replace("/", "").replace("\"", "")
                    all_songs['idList'].append({'title':new_title, 'id':s['videoId'], 'author':s['author']}) 
                with open("new_playlist.json", "w") as playlist_new:
                    json.dump(all_songs, playlist_new)
                backend.downloadVideo(s['videoId'], new_title) 
                break
        self.refreshPlaylist()
        self.search_bar.setText("")
        self.online_dloadbtn.setEnabled(False)

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
                    selected_song = selected_song.replace("|", "").replace(" ", "").replace("(", "").replace(")", "").replace("/", "").replace("\"", "")
                    after_len = len(selected_song)
                    if before_len != after_len:
                        # replace title
                        self.replaceTitle(orig_title, selected_song)
                    song_data = d
                    #song_data['title'] = selected_song

                    backend.downloadVideo(song_data['id'], selected_song)
                    self.refreshPlaylist()