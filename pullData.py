import pandas as pd
import aiohttp
from aiohttp import ClientSession
import requests
import json
import urllib
import numpy as np

CLIENT_ID = open("secrets.txt").read().splitlines()[0]
print(CLIENT_ID)
CLIENT_SECRET = open("secrets.txt").read().splitlines()[1]

def authenticate(client_id,client_secret):
	AUTH_URL = 'https://accounts.spotify.com/api/token'
	#POST
	auth_response = requests.post(AUTH_URL,{
		'grant_type': 'client_credentials',
		'client_id': client_id,
		'client_secret': client_secret})
	
	# save the access token
	access_token = auth_response.json()['access_token']
	return access_token


def query_playlists(query):
	access_token = authenticate(CLIENT_ID,CLIENT_SECRET)
	headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
	url = f"https://api.spotify.com/v1/search?query={query}&type=playlist&offset=0&limit=50"
	          #print(url)
	r = requests.get(url, headers = headers).text
	playlistIDs = []
	for n in range(len(json.loads(r)["playlists"]['items'])):
	    playlistIDs.append((json.loads(r)["playlists"]['items'][n]["id"]))

	return playlistIDs



if __name__ == "__main__":
	print(CLIENT_ID)
	print(query_playlists("hype"))