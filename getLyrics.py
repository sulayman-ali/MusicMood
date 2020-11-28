import pandas as pd
import urllib
import re
import json
from bs4 import BeautifulSoup
import pickle
import requests
import multiprocessing


df = pd.read_csv("data/spotifyqueriesresults.csv")[5000:]
def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    lyrics = html.find("div", class_ = "lyrics").get_text()
    return lyrics

base_url = "http://api.genius.com"
# headers = {'Authorization': 'Bearer D4h8hVWW7v5LIH2xey0lURGwEhvW_H5RF2e76i9d7qqxikML2_Pjk2PMn4uQisFc'}
headers = {'Authorization': 'Bearer r0oN8Yy1kyt4b6RgJRB8hLxnUdmFXEgLwUreXt-1dQ43ZKJbQWuMLhWePkV2y84A'}
#headers = {'Authorization': 'Bearer aXSt3tncxabMd7mIfezUBZZLfrTMcJChNC66oPP0LfHW9sGCv6kgWx9Tl4ZSw14ytDHvJyNunPaJrsQD0-cyyg'}

# def get_lyrics(row):
#         song_title = row['title']
#         artist_name = row['artist']
def get_lyrics(song_title,artist_name):
        search_url = base_url + "/search?q=" + urllib.parse.quote_plus(str(song_title) + urllib.parse.quote_plus(" "+str(artist_name)))
        response = requests.get(search_url, headers=headers)
        json = response.json()
        song_info = None
        for hit in json["response"]["hits"]:
            if song_title.lower() in str(hit["result"]['full_title']).lower():
                song_info = hit
                break
        try:
            api_path = song_info['result']['api_path']
            lrc_string = lyrics_from_song_api_path(api_path)
            ls1 = re.sub(r'[0-9]',' ', lrc_string)
            ls2 = re.sub(r'[^\w\s]','',ls1)
            return ls2
        except:
            return None

test_object = [(str(row[1]["title"]),str(row[1]["artist"])) for row in df.iterrows()]

def multiprocess_lyrics(obj):
    pool = multiprocessing.Pool()
    result = pool.starmap(get_lyrics,[item for item in obj])
    return result 

lyrics = multiprocess_lyrics(test_object)

pickle.dump(lyrics, open("lyrics2.pkl", 'wb'))
