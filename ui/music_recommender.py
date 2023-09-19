# Music Recommendation Algorithm


import os

import pandas as pd

import pydotplus

import matplotlib
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = '29a9fed336c0425aa09a96c840d88a3f'
CLIENT_SECRET = '7aae807829bd4b27aed0bc546b4200f2'

client_credentials_manager = SpotifyClientCredentials(CLIENT_ID,CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


attribute_order = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                   'liveness','mode', 'speechiness', 'valence']


def generate_track_list(track_compilation):
    """
    Generates a list of track ids given a track compilation (album or playlist)

    Inputs:
        track_compilation (dictionary): an album or playlist

    Returns: tracklist (list): a list of track ids
    """
    assert track_compilation['type'] == 'album' or track_compilation['type'] == 'playlist'

    if track_compilation['type'] == 'album':
        tracks_info = sp.album_tracks(track_compilation['id'])
    else:
        tracks_info = sp.playlist(track_compilation['id'], fields = 'tracks')['tracks']
    
    tracks = tracks_info['items']

    while tracks_info['next']:
        tracks_info = sp.next(tracks_info)
        tracks += tracks_info['items']
    
    if track_compilation['type'] == 'album':
        return list(map(lambda t: t['id'], tracks))
    else:
        return list(map(lambda t: t['track']['id'], tracks))


