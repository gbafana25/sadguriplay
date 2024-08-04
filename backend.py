#!/usr/bin/python3
import json
import requests
import sys
import os
import time
import subprocess

# add list of instances
#BASE_URL = "https://vid.puffyan.us/api/v1"
#BASE_URL = "https://invidious.slipfox.xyz/api/v1"
BASE_URLS = ["https://inv.tux.pizza", "https://invidious.protokolla.fi", "https://invidious.io.lol"]
URL = ""
base_path = os.path.expanduser("~/sideplay/")
playlist_path = base_path+"new_playlist.json"

# removes characters that cause ffmpeg command to fail
def sanitizeTitle(name):
    newname = ''
    for i in range(len(name)):
        if(name[i] >= 'A' and name[i] <= 'z'):
            #name[i] = ''
            newname+=name[i]

    return newname
    #return name.replace(' ', '-').replace('&', '').replace('(', '').replace(')', '').replace("\"", "").replace(":", "").replace(",", "")

def slugTerm(term):
	return term.replace(" ", '-')


def convertToMp3(name, src):	
	print(name)
	print(src)
	#os.system("ffmpeg -i "+src+" "+name+".mp3")
	subprocess.run(["ffmpeg", "-i", src, base_path+"songs/"+name+".mp3"])
	# delete .mp4
	subprocess.run(['rm', './'+src])


def searchVideos(term):
	print("searching...")
	r = requests.get(BASE_URLS[2]+"/api/v1/search?q="+term)
	p = r.json()
	return p
	#print(p)
	"""
	count = 0
	vid_list = []
	for e in range(10):
		try:
			if(p[e]['type'] == "video"):
				vid_title = ""
				if(len(p[e]['title']) <= 25):
					vid_title = p[e]['title']
				else:
					vid_title = p[e]['title'][:24]+"..."
					
					
				print(str(count) + ")", vid_title + "|" + p[e]['author'] + "|" + str(round(p[e]['lengthSeconds']/60)) + "min|" + str(p[e]['viewCount']) + "|" + p[e]['publishedText'])
				vid_list.append((count, e))
				count += 1
		except:
			pass

	v = input("> ")
	for i in range(len(vid_list)):
		if vid_list[i][0] == int(v):
			form = input("Keep as video? [y/n] ").lower()	
			return (p[vid_list[i][1]]['videoId'], p[vid_list[i][1]]['title'], form, slugTerm(qu))
	"""
		

def downloadVideo(l, full_name):
	v = requests.get(BASE_URLS[0]+"/api/v1/videos/"+l)
	p = json.loads(v.text)	
	# list index correlates to video quality 
	# 0 - usually 144p

	url = p['formatStreams'][len(p['formatStreams'])-1]['url']
	print("downloading video...")
	raw = requests.get(url)
	ext = ".mp4"
	filename = l.strip()
	with open(filename+ext, "wb+") as o:
		o.write(raw.content)
		o.close()

	convertToMp3(full_name, l+".mp4")	

def testInstances():
	for i in range(len(BASE_URLS)):
		try:
			r = requests.get(BASE_URLS[i])
			return BASE_URLS[i]
		except ConnectionError:
			print(URL+" doesn't work, skipping...")	

def savetoPlaylist(vid_id):
	data = None
	if os.path.exists("playlist.json") == False:
		with open("playlist.json", "w+") as p:
			d = {
				'idList': []
			}
			json.dump(d, p)

	with open("playlist.json", "r") as p:
		data = json.load(p)
		data['idList'].append(vid_id)

	with open("playlist.json", "w") as p:
		json.dump(data, p)


def getVideoId(vid_id):
	plist = None
	vid_info = requests.get(URL+'/api/v1/videos/'+vid_id)
	data = json.loads(vid_info.text)
	if data != None:	
		if 'title' in data and 'author' in data:
			print(data['title'], data['author'])
		if os.path.exists(playlist_path) == False:
			with open(playlist_path, "w+") as p:
				d = {
					'idList': []
				}
				json.dump(d, p)

		with open(playlist_path, "r") as playlist:
			plist = json.load(playlist)
			if 'title' in data and 'videoId' in data and 'author' in data:
				plist['idList'].append({"title": data['title'], "id": data['videoId'], "author": data['author']})
		
		with open(playlist_path, "w") as playlist:
			json.dump(plist, playlist)


def copyNewSongs():
	#subprocess.run(['mkdir', '-p', 'music_mnt'])
	#subprocess.run(['go-mtpfs', 'music_mnt/', '&'])#, executable="/bin/bash", shell=True)
	computer_dir = os.listdir("/home/gareth/sideplay/songs")
	#phone_dir = os.listdir("./music_mnt/Internal shared storage/Download/")
	phone_dir = subprocess.run(['/home/gareth/sideplay/sync_files.sh'], capture_output=True)
	phone_contents = phone_dir.stdout.decode().split('\n')
	stored_music = []
	#print(phone_contents)
	#print(type(phone_contents))
	for p in phone_contents:
		if p[-4:] == '.mp3':
			stored_music.append(p[:-4])	

	subprocess.run(['/home/gareth/sideplay/mount_phone.sh'])
	for c in computer_dir:
		if c not in stored_music:
			print("Copying "+c)
			subprocess.run(['cp', "/home/gareth/sideplay/songs/"+c, "./music_mnt/Internal shared storage/Download/"])

	subprocess.run(['fusermount', '-u', 'music_mnt/'])
	"""
	for c in computer_dir:
		if c not in phone_dir:
			print(c)
	subprocess.run(['fusermount', '-u', 'music_transfer'])
	"""