#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:36:15 2023

@author: kiranchandra
"""

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import pandas as pd
import json

CLIENT_ID = "Enter your client ID"
CLIENT_SECRET = "Enter your client Secret"

data = {'Sanam Gambhir': '6C70YxzkKJhdL4uND1hCaC', 'spotify': '37i9dQZF1DX5IDTimEWoTd', 'ROYAL NINJA': '2RdquYcoGqFNP1KUGIUOaL', "jp'sjams":'5xEIQ2u3ZzG5gt0Cg7uDrj'}


# Create empty dataframe
playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]  
playlist_df = pd.DataFrame(columns = playlist_features_list)

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

def playlistAnalyzer(creator, Id):  
    
    global playlist_df
    
    playlist = spotify.user_playlist_tracks(creator, Id)["items"]
    for track in playlist:
        
        # Create empty dict
        playlist_features = {}
        
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]
        playlist_features["popularity"] = track["track"]["popularity"]
        playlist_features["is_local"] = track["track"]["is_local"]
        playlist_features["duration_ms"] = track["track"]["duration_ms"]

        # Get audio features
        audio_features = spotify.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]

        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
        
    return playlist_df


def playlist_creator(Id):
    
    playlists = spotify.category_playlists(category_id = Id)['playlists']['items']
    for playlist in playlists:
        data[playlist['name']] = playlist['id']

#Fetch Categories ID
category_list_id = []
categories_ids = spotify.categories()['categories']
for category_id in categories_ids['items']:
    category_list_id.append(category_id['id'])

#Loop through Each categories to get their playlist ID
for i in category_list_id: 
    try:       
        playlist_creator(i)
    except:
        pass
 
# Get Songs Info
for i in data.keys():
    try:
        playlist_df = playlistAnalyzer(i, data[i])
    except:
        pass

#Export Dataset
playlist_df.to_csv('DataFrame.csv', index=False)

print(playlist_df)