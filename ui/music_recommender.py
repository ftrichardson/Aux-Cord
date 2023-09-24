# Music Recommendation Algorithm

import os
import json

import pandas as pd

import pydotplus

import matplotlib
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = "f496ea2bb6d5495ea72c159979c02820"
CLIENT_SECRET = "15c95a4e67f14caf9528c441482d705c"

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
    of each bin for an audio feature.

    Inputs:
        binned_audio_features (pandas DataFrame): audio_features_dataframe with 
            non-mode audio features categorized into 0.1-width bins
    
    Returns: all_bin_proportions (list): a list of 1-column DataFrames, where each
        DataFrame represents the relative distribution of each bin for an audio
        feature
    """
    all_bin_proportions = []

    for audio_feature in binned_audio_features:
        audio_feature_bin_proportions = pd.DataFrame(binned_audio_features[audio_feature].value_counts())
        all_bin_proportions.append(audio_feature_bin_proportions \
            [audio_feature_bin_proportions[audio_feature] != 0] / 
            len(binned_audio_features))
    
    return all_bin_proportions


def find_highest_interval_densities(audio_feature_interval_densities):
    """
    Analyzes DataFrame of interval densities for a specific audio feature and returns
    the highest interval densities (at most 2)

    Inputs:
        audio_feature_interval_densities (pandas DataFrame): DataFrame of interval densities 
            for a specific audio feature
    
    Returns: highest_interval_densities (list): a list of highest interval densities for 
        a specific audio feature
    """
    highest_interval_densities = []
    percent_data_processed = 0

    for interval, interval_density in audio_feature_interval_densities.iterrows():
        # If the audio feature being analyzed is mode, which has 2 possible values,
        # simply return the value that occurs more frequently in [[interval, interval]] format
        if audio_feature_interval_densities.columns[0] == "mode":
            return [[interval, interval]]
        
        weighted_interval_density = (interval.left + interval.right) / 2 * interval_density[0]
        highest_interval_densities.append([interval, interval_density[0], weighted_interval_density])

        # For efficiency, stop once at least 50% of the data is accounted for
        percent_data_processed += interval_density[0]

        if percent_data_processed >= 0.5:
            break
    
    highest_interval_densities.sort()
    index = 0

    # Check for any jump discontinuities between intervals
    while index < len(highest_interval_densities) - 1:
        if highest_interval_densities[index][0].right == highest_interval_densities[index + 1][0].left:
            highest_interval_densities[index][0] = pd.Interval(left=highest_interval_densities[index][0].left,
                                                        right=highest_interval_densities[index + 1][0].right,
                                                        closed='right')
            highest_interval_densities[index][1] += highest_interval_densities[index + 1][1]
            highest_interval_densities[index][2] += highest_interval_densities[index + 1][2]
            del highest_interval_densities[1]
        else:
            index += 1
    
    for interval_density in highest_interval_densities:
        interval_density[2] /= interval_density[1]
        del interval_density[1]
    
    return sorted(highest_interval_densities, key= lambda interval_density: interval_density[1], reverse=True)[:2]


def find_highest_intervals(track_compilation):
    """
    Given a track compilation, finds the highest-represented interval for each audio feature

    Inputs:
        track_compilation (dictionary): an album or playlist
    
    Returns: highest_intervals (list): a list of interval, average value pairs for each
        audio attribute
    """
    audio_features_dataframe = create_audio_features_dataframe(track_compilation)
    bin_audio_features(audio_features_dataframe)
    all_bin_proportions = generate_bin_proportions(audio_features_dataframe)
    highest_intervals = all_bin_proportions # Renamed to reflect content of end result of this function

    for index, __ in enumerate(highest_intervals):
        highest_intervals[index] = highest_intervals[index].rename_axis('interval').groupby('interval').sum()
        highest_intervals[index].sort_values(ascending=False, inplace=True, by=audio_features[index])
        highest_intervals[index] = find_highest_interval_densities(highest_intervals[index])
    
    return highest_intervals


def generate_song_selection_criteria(highest_intervals, index):
    """
    Using the list of highest intervals, this function recursively creates different combinations 
    of audio feature values that a Spotify user may prefer

    Inputs:
        highest_intervals (list): a list of interval, average value pairs for each
            audio attribute
        index (int): an accumulator variable to keep track of recursion depth
    
    Returns: song_selection_criteria (list): a list of lists of audio feature values
    """
    song_selection_criteria = []

    if index == 7: # Do not want to exceed maximum of 2^7 search sequences
        for (__, average_interval_value) in highest_intervals[index]:
            song_selection_criteria.append([average_interval_value])
    else:
        for (__, average_interval_value) in highest_intervals[index]:
            for song_selection_criterion in generate_song_selection_criteria(highest_intervals, index + 1):
                song_selection_criteria.append([average_interval_value] + song_selection_criterion)
    
    return song_selection_criteria


def find_recommended_songs(track_compilation, input_genre):
    """
    Given a track compilation and user-inputted genre, this function recommends songs
    based on new releases and a seed of 5 tracks in the track compilation

    Inputs:
        track_compilation (dictionary): an album or playlist
        input_genre (list): a list containing a string representation of a user's
            preferred genre
    
    Returns: recommended_songs (list): a list of track ids
    """
    recommended_songs = []
    song_selection_criteria = generate_song_selection_criteria(find_highest_intervals(track_compilation), 0)

    # Use new_release to prioritize more recent songs
    recommended_songs.extend(sp.recommendations(seed_genres=input_genre + ['new_release'],
                                            target_acousticness=song_selection_criteria[0][0],
                                            target_danceability=song_selection_criteria[0][1],
                                            target_energy=song_selection_criteria[0][2],
                                            target_intrumentalness=song_selection_criteria[0][3],
                                            target_liveness=song_selection_criteria[0][4],
                                            target_mode=song_selection_criteria[0][5],
                                            target_speechiness=song_selection_criteria[0][6],
                                            target_valence=song_selection_criteria[0][7], limit=100)['tracks'])
    

    for song_selection_criterion in song_selection_criteria:
        recommended_songs.extend(sp.recommendations(seed_tracks=generate_track_list(track_compilation)[:5],
                                       target_acousticness=song_selection_criterion[0],
                                       target_danceability=song_selection_criterion[1],
                                       target_energy=song_selection_criterion[2],
                                       target_intrumentalness=song_selection_criterion[3],
                                       target_liveness=song_selection_criterion[4],
                                       target_mode=song_selection_criterion[5],
                                       target_speechiness=song_selection_criterion[6],
                                       target_valence=song_selection_criterion[7], limit=100)['tracks'])
    
    recommended_songs = list(map(lambda track: track['id'], recommended_songs))

    return recommended_songs













