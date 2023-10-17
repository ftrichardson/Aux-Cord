import os
import csv

from django.shortcuts import render
from django import forms

from music_recommender import generate_playlist

RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')


def _load_column(filename, col=0):
    """Load single column from csv file."""
    with open(filename) as f:
        col = list(zip(*csv.reader(f)))[0]
        return list(col)


def _load_res_column(filename, col=0):
    """Load column from resource directory."""
    return _load_column(os.path.join(RES_DIR, filename), col=col)


def _build_dropdown(options):
    """Convert a list to (value, caption) tuples."""
    return [(x, x) if x is not None else ('', '') for x in options]


GENRES = _build_dropdown([None] + _load_res_column('genres.csv'))
AUDIO_FEATURES = _build_dropdown(_load_res_column('audio_features.csv'))


class SearchForm(forms.Form):
    """Django form to collect user input"""
    # User 1
    user_1_playlist = forms.CharField(label='User 1 Spotify Playlist URL',
                                    required=True,
                                    widget=forms.TextInput(attrs={'class': 'user-1-playlist-container', 'placeholder': 'Playlist ID'}))
    
    user_1_preferred_genre = forms.ChoiceField(label='User 1 Preferred Genre',
                                    choices=GENRES,
                                    required=True,
                                    widget=forms.Select(attrs={'class': 'user-1-preferred-genre-container'}))
    
    user_1_disliked_genre_required = forms.ChoiceField(label='User 1 Disliked Genre #1',
                                    choices=GENRES,
                                    required=True,
                                    widget=forms.Select(attrs={'class': 'user-1-disliked-genre-required-container'}))
    
    user_1_disliked_genre_optional = forms.ChoiceField(label='User 1 Disliked Genre #2 (Optional)',
                                    choices=GENRES,
                                    required=False,
                                    widget=forms.Select(attrs={'class': 'user-1-disliked-genre-optional-container'}))
    
    # User 2
    user_2_playlist = forms.CharField(label='User 2 Spotify Playlist URL',
                                    required=True,
                                    widget=forms.TextInput(attrs={'class': 'user-2-playlist-container', 'placeholder': 'Playlist ID'}))
    
    user_2_preferred_genre = forms.ChoiceField(label='User 2 Preferred Genre',
                                    choices=GENRES,
                                    required=True)
    
    user_2_disliked_genre_required = forms.ChoiceField(label='User 2 Disliked Genre #1',
                                    choices=GENRES,
                                    required=True)
    
    user_2_disliked_genre_optional = forms.ChoiceField(label='User 2 Disliked Genre #2 (Optional)',
                                    choices=GENRES,
                                    required=False)
    

def home(request):
    """Generates the home page of Aux Cord"""
    context = {}
    output_playlist = None

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            user_inputs = {} # Collect user input information...

            # Playlists
            user_inputs['first_track_compilation'] = form.cleaned_data['user_1_playlist']
            user_inputs['second_track_compilation'] = form.cleaned_data['user_2_playlist']

            # Disliked and preferred genres
            user_inputs['first_user_preferred_genre'] = [form.cleaned_data['user_1_preferred_genre']]
            user_inputs['second_user_preferred_genre'] = [form.cleaned_data['user_2_preferred_genre']]

            user_inputs['disliked_genres'] = []
            user_inputs['disliked_genres'].append(form.cleaned_data['user_1_disliked_genre_required'])
            user_inputs['disliked_genres'].append(form.cleaned_data['user_2_disliked_genre_required'])
            if form.cleaned_data['user_1_disliked_genre_optional']:
                user_inputs['disliked_genres'].append(form.cleaned_data['user_1_disliked_genre_optional'])
            if form.cleaned_data['user_2_disliked_genre_optional']:
                user_inputs['disliked_genres'].append(form.cleaned_data['user_2_disliked_genre_optional'])

            # Finally...validate user inputs
            is_user_inputs_valid = True
            for __, value in user_inputs.items():
                if len(value) == 0:
                    is_user_inputs_valid = False
            
            if is_user_inputs_valid:
                output_playlist = generate_playlist(user_inputs)
    else:
        form = SearchForm()
    

    if output_playlist == None:
        context['output_playlist'] = None
    else:
        context['output_playlist'] = output_playlist
        context['audio_features'] = True
        context['columns'] = ['Track', 'Artist', 'Album', 'Preview']
    
    context['form'] = form
    return render(request, 'index.html', context)