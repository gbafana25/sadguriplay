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
h = {"User-Agent":"Mozilla/5.0"}
BASE_URLS = ["https://iv.ggtyler.dev", "https://invidious.nerdvpn.de", "https://inv.nadeko.net"]
URL = ""
base_path = os.path.expanduser("~/sadguriplay/")
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
	r = requests.get(BASE_URLS[2]+"/api/v1/search?q="+term, headers=h)
	p = r.json()
	return p
	#print(p)	
		

def downloadVideo(l, full_name):
	v = requests.get(BASE_URLS[0]+"/api/v1/videos/"+l, headers=h)
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
			r = requests.get(BASE_URLS[i], headers=h)
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
	vid_info = requests.get(URL+'/api/v1/videos/'+vid_id, headers=h)
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
	subprocess.run('go-mtpfs music_mnt &', shell=True)
	time.sleep(2);
	phone_proc = subprocess.run([base_path+'read_phone.sh'], capture_output=True)
	phone_dir = phone_proc.stdout.decode().split('\n')
	host_dir = os.listdir(base_path+'songs/')
	songs_to_copy = []
	for h in host_dir:
		if h not in phone_dir and h[-3:] == 'mp3':
			songs_to_copy.append(h)
	
	#for c in songs_to_copy:
	#	print(c)
	for s in songs_to_copy:
		subprocess.run(['cp', base_path+"songs/"+s, base_path+"music_mnt/Internal shared storage/Download"])

	subprocess.run(['fusermount', '-u', base_path+'music_mnt/'])
	
