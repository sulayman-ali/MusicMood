import aiohttp
from aiohttp import ClientSession
import requests
import json
import urllib
import numpy as np

CLIENT_ID = open("secrets.txt").read().splitlines()[0]
CLIENT_SECRET = open("secrets.txt").read().splitlines()[1]
LABELS = {
	"wonder": [],
	"transcendence":[],
	"tenderness":[],
	"nostlgia":[],
	"peacefulness":[],
	"power": [],
	"joyful_activation":[],
	"tension":[],
	"sadness":[]
}

def authenticate(client_id,client_secret):
	'''
	'''

	AUTH_URL = 'https://accounts.spotify.com/api/token'
	#POST
	auth_response = requests.post(AUTH_URL,{
		'grant_type': 'client_credentials',
		'client_id': client_id,
		'client_secret': client_secret})

	# save the access token
	access_token = auth_response.json()['access_token']
	return access_token

def getsong_details(uri,headers):
	url = "https://api.spotify.com/v1/audio-features/{item}".format(item = uri)
	results = {}
	try:
		r = requests.get(url, headers = headers).text
		j = json.loads(r)
		# results.append((
		# 	j['danceability'],j['energy'],j['key'],j['mode'],j['acousticness'],j['instrumentalness'],
		# 	j['tempo'],j["valence"],j["speechiness"],j["loudness"]))

		results["danceability"] = j['danceability']
		results["energy"] = j['energy']
		results["key"] = j['key']
		results["mode"] = j['mode']
		results["acousticness"] = j['acousticness']
		results["instrumentalness"] = j['instrumentalness']
		results["tempo"] = j['tempo']
		results["valence"] = j['valence']
		results["speechiness"] = j['speechiness']
		results["loudnes"] = j['loudnes']

	except:
		pass
	return results



def query_playlists(query):
	'''
	'''
	
	access_token = authenticate(CLIENT_ID,CLIENT_SECRET)
	headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
	url = f"https://api.spotify.com/v1/search?query={query}&type=playlist&offset=0&limit=50"
	          #print(url)
	r = requests.get(url, headers = headers).text
	playlistIDs = []
	for n in range(len(json.loads(r)["playlists"]['items'])):
	    playlistIDs.append((json.loads(r)["playlists"]['items'][n]["id"]))

	playlist_dict = {pid:[] for pid in playlistIDs}

	for playlist in playlistIDs[:1]:
		url = "https://api.spotify.com/v1/playlists/{p}/tracks".format(p = playlist)
		r = requests.get(url, headers = headers).text
		for s in range(len(json.loads(r)["items"])):
			try:
				# songs[playlist].append((json.loads(r)["items"][s]["track"]["name"],json.loads(r)["items"][s]["track"]["uri"]))
				uri = json.loads(r)["items"][s]["track"]["uri"].split(":")[2]
				title = json.loads(r)["items"][s]["track"]["name"]
				audio_features = getsong_details(uri,headers)
				artist = json.loads(r)["items"][s]["track"]["album"]["artists"][0]["name"]
				playlist_dict[playlist].append((title,
												artist,		
												audio_features))
			except:
				continue

	return playlist_dict


# def get_song_info(ids):
# 	'''
# 	'''

# 	access_token = authenticate(CLIENT_ID,CLIENT_SECRET)
# 	headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
# 	songs = {}
# 	for playlist in ids:
# 	    url = "https://api.spotify.com/v1/playlists/{p}/tracks".format(p = playlist)
# 	    r = requests.get(url, headers = headers).text
# 	    songs[playlist] = []
# 	    for s in range(len(json.loads(r)["items"])):
# 	        try:
# 	            songs[playlist].append((json.loads(r)["items"][s]["track"]["name"],json.loads(r)["items"][s]["track"]["uri"]))
# 	        except:
# 	            continue

# def getsong_details(l):
# 	access_token = authenticate(CLIENT_ID,CLIENT_SECRET)
# 	headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
#     deets = []
#     for item in l:
#         url = "https://api.spotify.com/v1/audio-features/{item}".format(item = item)
#         try:
#             r = requests.get(url, headers = headers).text
#             j = json.loads(r)
#             deets.append((
#                 j['danceability'],j['energy'],j['key'],j['mode'],j['acousticness'],j['instrumentalness'],
#                 j['tempo'],j["valence"],j["speechiness"],j["loudness"]
#                          ))
#         except:
#             deets.append(("!" * 10))
#     return deets


if __name__ == "__main__":
	print(query_playlists("hype"))