import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

## Authentication

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-top-read'
    )
) 

if not sp.auth_manager.get_cached_token():
    st.warning('Please authenticate with Spotify to view data!')

## Streamlit UI setup

st.set_page_config(page_title='Playlist Optimizer', page_icon=':musical_note:')
st.title('Playlist Optimizer by Caleb Picone')
st.write('Create optimized playlists with this Spotify tool.')

## Fetch data from Spotify w/ error handling

try:
    top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')
    track_ids = [track['id'] for track in top_tracks['items']]
    audio_features = sp.audio_features(track_ids)
except Exception as e:
    st.error(f'Error fetching data from Spotify: {e}')
    st.stop()

## Pandas DataFrame initialization

df = pd.DataFrame(audio_features)
df['track_name'] = [track['name'] for track in top_tracks['items']]
df = df[['track_name', 'danceability', 'energy', 'valence']]
df.set_index('track_name', inplace=True)

st.subheader('Audio Features for Top Tracks')
st.bar_chart(df, height=500)
st.dataframe(df)