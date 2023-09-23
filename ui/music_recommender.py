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


audio_features = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                   'liveness','mode', 'speechiness', 'valence']

# Spotipy can handle maximum 100 tracks in tracklist per API call
MAX_TRACKS_PER_BATCH = 100


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


def create_audio_features_dataframe(track_compilation, is_playlist=True):
    """
    Creates an n x 8 pandas DataFrame of audio feature statistics for each
    track id in track_compilation

    Inputs:
        track_compilation (dictionary or list): an album or playlist, or a
            list of track ids
        is_playlist (boolean): indicates if track_compilation is a playlist
    
    Returns: audio_features_dataframe (pandas DataFrame): the n x 8 DataFrame
    """
    audio_features_list = []

    if is_playlist:
        tracklist = generate_track_list(track_compilation)
    else:
        tracklist = track_compilation
    
    batches = len(tracklist) // MAX_TRACKS_PER_BATCH # Must process in batches

    if len(tracklist) % MAX_TRACKS_PER_BATCH != 0:
        batches += 1
    
    for batch in range(batches):
        start = batch * MAX_TRACKS_PER_BATCH
        end = (batch * MAX_TRACKS_PER_BATCH) + MAX_TRACKS_PER_BATCH
        audio_features_list.extend(sp.audio_features(tracklist[start: end]))
    
    # Preprocess audio_features_dataframe
    audio_features_dataframe = pd.DataFrame(audio_features_list)
    audio_features_dataframe.set_index('id', inplace=True)
    audio_features_dataframe.drop(columns=['type', 'uri', 'track_href', 
                                'analysis_url', 'tempo', 'time_signature', 
                                'duration_ms', 'loudness', 'key'], inplace = True)
    audio_features_dataframe = audio_features_dataframe[audio_features]

    return audio_features_dataframe
    

def bin_audio_features(audio_features_dataframe):
    """
    Discretizes non-mode audio features in audio_features_dataframe, categorizing
    the data into 0.1-width bins to prepare it for machine learning-based 
    recommendation

    Inputs:
        audio_features_dataframe (pandas DataFrame): n x 8 DataFrame indexed by track id
    
    Returns: None (modifies audio_features_dataframe in-place)
    """
    for audio_feature in audio_features:
        if audio_feature != 'mode':
            audio_features_dataframe[audio_feature] = pd.cut(audio_features_dataframe[audio_feature], 
                [-0.001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])


def generate_bin_proportions(binned_audio_features):
    """
    Generates a list of 1-column DataFrames that each represent the proportions
    of each bin for an audio feature. This list will be 

    Inputs:
        binned_audio_features (pandas DataFrame): audio_features_dataframe with 
            non-mode audio features categorized into 0.1-width bins
    
    Returns: all_bin_proportions (list): a list of 1-column DataFrames, where each
        DataFrame represents the relative distribution of each bin for an audio
        feature
    """
    all_bin_proportions = []

    for audio_feature in binned_audio_features:
        bin_proportions = pd.DataFrame(binned_audio_features[audio_feature].value_counts())
        all_bin_proportions.append(bin_proportions[bin_proportions[audio_feature] != 0] / 
            len(binned_audio_features))
    
    return all_bin_proportions
