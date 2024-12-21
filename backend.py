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
BASE_URLS = ["https://inv.nadeko.net", "https://invidious.jing.rocks/", "https://iv.nboeck.de", "https://invidious.adminforge.de", "https://inv.tux.pizza", "https://invidious.reallyaweso.me", "https://invidious.yourdevice.ch", "https://iv.ggtyler.dev"]
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


def searchVideos(term):
	print("searching...")
	r = requests.get(BASE_URLS[2]+"/api/v1/search?q="+term, headers=h)
	p = r.json()
	return p
	#print(p)	

def searchVideosYoutube(term):
	print("searching...")
	obj = {
		"context": {
			"client": {
				"userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36,gzip(gfe)",
				"clientName": "WEB",
				"clientVersion": "2.20241212.08.00",
				"originalUrl": "https://www.youtube.com/results?search_query="+term.replace(" ", "+"),
				"configInfo": {
					"appInstallData": "CJ_E97oGEKaasAUQqJ3OHBDi1K4FEMrUsQUQzdGxBRCZ0v8SELbgrgUQlrHOHBDI2LEFEL2KsAUQ1uP_EhCHw7EFEPSzzhwQ56jOHBDE2LEFEJ3QsAUQ_97_EhDJ968FEKuezhwQ55rOHBCpps4cEPSlzhwQt-r-EhDqkM4cEOrDrwUQkrzOHBComrAFEIjjrwUQvZmwBRCi1LEFEIvUsQUQ0arOHBCM0LEFEPWGsQUQksuxBRCuj_8SEN6tsQUQo83_EhDxls4cEIqhsQUQytixBRCIh7AFEN-0zhwQwavOHBD4q7EFEL22rgUQnaawBRDh7LAFEPGcsAUQlP6wBRDgjf8SEPq4zhwQ0ZTOHBDiq84cEMC3zhwQiLDOHBCN1LEFEI7QsQUQzN-uBRDL0bEFEPHe_xIQu6zOHBCinbEFEOilzhwQms6xBRDGv7EFEN2dzhwQpLjOHBDr6P4SEParsAUQ2arOHBCPw7EFEMK3zhwQtqTOHBDB2v8SENCNsAUQjtexBRCio84cEIHDsQUQt--vBRCNzLAFEJS7zhwQ_LLOHBDJ5rAFEMbYsQUQ2pTOHBCmk7EFEIuuzhwQrZ7OHBDrmbEFEInorgUQmZixBRCWgrgiEMHNsQUQg8OxBRDmz7EFEJmNsQUQ0-GvBRDlubEFENy6zhwQ18GxBRDtubEFEI-tzhwQhaexBRDgzbEFELi3zhwQgdaxBRDbr68FEN68zhwQoJzOHBCO5v8SEIqzzhwQr6jOHCosQ0FNU0d4VVFwYjJ3RE56a0JvT3o5QXZvc1FTUDlBNm9ET0Z5MW53ZEJ3PT0%3D",
					"coldConfigData": "CJ_E97oGGjJBT2pGb3gyOEd5eDJHdUNlZTV3U1BxTFo2dWFPTWxjNjhBQkFVakVvZm9OdXRJaXVfQSIyQU9qRm94MjhHeXgyR3VDZWU1d1NQcUxaNnVhT01sYzY4QUJBVWpFb2ZvTnV0SWl1X0E%3D",
					"coldHashData": "CJ_E97oGEhM4NjM5ODU1OTY4MTYzNzI0NTY3GJ_E97oGMjJBT2pGb3gyOEd5eDJHdUNlZTV3U1BxTFo2dWFPTWxjNjhBQkFVakVvZm9OdXRJaXVfQToyQU9qRm94MjhHeXgyR3VDZWU1d1NQcUxaNnVhT01sYzY4QUJBVWpFb2ZvTnV0SWl1X0E%3D",
					"hotHashData": "CJ_E97oGEhQxMTk5MTE1OTk3MTg4MzgxMTg5ORifxPe6BjIyQU9qRm94MjhHeXgyR3VDZWU1d1NQcUxaNnVhT01sYzY4QUJBVWpFb2ZvTnV0SWl1X0E6MkFPakZveDI4R3l4Mkd1Q2VlNXdTUHFMWjZ1YU9NbGM2OEFCQVVqRW9mb051dElpdV9B"
				}
			}
		},
		"query": term,
		"webSearchboxStatsUrl": "/search?oq="+term+"&gs_l=youtube.3..0i471k1j0i512k1l2j0i512i10k1j0i512k1l2j0i512i10k1l4j0i512k1j0i512i10k1j0i512k1l2.10848.365206.0.365721......1.495.1881.0j10j1j0j1...ytqsicpu_p,ytpo-bo-me=0,ytposo-bo-me=0,ytpo-bo-ei=45358234,ytposo-bo-ei=45358234.0......1.......0..0i433i471k1j0i433i131i229k1j0i512i433k1j0i433i131i389k1j0i512i433i131k1j0i433i229k1j0i433i131i471k1j0i229k1j0i512i433i131i650k1.160"
	}

	r = requests.post("https://www.youtube.com/youtubei/v1/search?prettyPrint=false", json=obj)
	respdata = r.json()
	songlist = []
	content_objs = respdata['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
	for c in range(len(content_objs)):
		if 'videoRenderer' in content_objs[c]:
			content_info = content_objs[c]['videoRenderer']
			#print(content_info['videoId'], content_info['title']['runs'][0]['text'], content_info['lengthText']['simpleText'], content_info['viewCountText']['simpleText'])
			songlist.append(
				{
					"id": content_info['videoId'], 
					"title": content_info['title']['runs'][0]['text'], 
					"duration": content_info['lengthText']['simpleText'], 
					"views": content_info['viewCountText']['simpleText']
				}
			)
	return songlist


def downloadVideoYoutube(l, fullname):
	subprocess.run(['yt-dlp_linux', '-x', '--audio-format', 'mp3', '-o', base_path+"songs/"+fullname+".%(ext)s",'https://youtube.com/watch?v='+l])
	subprocess.run(['touch', base_path+"songs/"+fullname+".mp3"])

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
	
