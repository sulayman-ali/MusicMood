import requests
import json
import urllib
import numpy as np
import pandas as pd
import pickle
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

CLIENT_ID = open("secrets.txt").read().splitlines()[0]
CLIENT_SECRET = open("secrets.txt").read().splitlines()[1]
LABELS = {
	"wonder": [],
	"transcendence":[],
	"tenderness":[],
	"nostalgia":[],
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
		#print(r)
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
		results["loudness"] = j['loudness']

	except:
		return "error"

	return results

def fetch_songs_from_playlist(session,query,playlist):
# def fetch_songs_from_playlist(url,session):
	access_token = authenticate(CLIENT_ID,CLIENT_SECRET)
	headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
	url = "https://api.spotify.com/v1/playlists/{p}/tracks".format(p = playlist)
	# r = requests.get(url, headers = headers).text
	r = session.get(url, headers = headers).text
	#print(r)
	result = []
	try:
		for s in range(len(json.loads(r)["items"])):
				try:
					rj = json.loads(r)
					uri = rj["items"][s]["track"]["uri"].split(":")[2]
					title = rj["items"][s]["track"]["name"]
					artist = rj["items"][s]["track"]["album"]["artists"][0]["name"]
					audio_features = getsong_details(uri,headers)
					audio_features["title"] = title
					audio_features["artist"] = artist
					audio_features["class"] = query
					audio_features["playlist_id"] = playlist
					result.append(audio_features)
				except:
					continue
	except:
		return None

	return json.dumps(result)

def multiprocess_queries(ids,query):
	pool = multiprocessing.Pool()
	with requests.Session() as session:
		result = pool.starmap(fetch_songs_from_playlist,[(session,query,playlist) for playlist in ids])
	return result 

def multithreading_queries(ids,query):
	with ThreadPoolExecutor(10) as pool:
		with requests.Session() as session:
			result = pool.map(fetch_songs_from_playlist,session * len(ids), query*len(ids), ids)
	return result 

def query_playlists(query):
	'''
	'''
	
	access_token = authenticate(CLIENT_ID,CLIENT_SECRET)
	headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
	url = f"https://api.spotify.com/v1/search?query={urllib.parse.quote_plus(query)}&type=playlist&offset=0&limit=50"
	r = requests.get(url, headers = headers).text
	playlistIDs = []

	#get playlist ID from search results for query
	for n in range(len(json.loads(r)["playlists"]['items'])):
	    playlistIDs.append((json.loads(r)["playlists"]['items'][n]["id"]))

	urls = ["https://api.spotify.com/v1/playlists/{p}/tracks".format(p = playlist) for playlist in playlistIDs]
	#result = multiprocess_queries(playlistIDs,query)
	result = multiprocess_queries(playlistIDs,query)
	return result

if __name__ == "__main__":
	df = pd.read_csv("data/emotion_queries.csv")
	# results = []
	# for q in df["query"]:
	# 	results.append(query_playlists(q))
	# pickle.dump(results, open("search_results.pkl", 'wb'))
	print(query_playlists("tender"))
	#pool = multiprocessing.Pool()
	#print(pool.map(cube,[1,2,3]))
