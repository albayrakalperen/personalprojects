from bs4 import BeautifulSoup
from decouple import config
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import requests

SPOTIFY_CLIENT_ID = config("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET = config("SPOTIFY_SECRET")
SPOTIFY_REDIRECT_URI = "http://example.com"

# Scraping Hit Songs By Date
date = input("Which year do you want to travel to? (YYYY-MM-DD): ")
HIT_SONGS_BY_DATE_URL = f"HIT_SONGS_WEBSITE/{date}/"
response = requests.get(HIT_SONGS_BY_DATE_URL)
billboard_top100 = response.text
soup = BeautifulSoup(response.text, "html.parser")
song_names = soup.select(selector="div ul li ul li h3", id="title-of-a-story")
top_songs_list = [song.getText().strip() for song in song_names]

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope="playlist-modify-private"))

# Create new playlist
user_name = sp.current_user()["id"]
billboard_playlist = sp.user_playlist_create(user="USERNAME", name=f"Billboard's Top 100 ({date})", public=False,
                                             collaborative=False, description="")

# Search songs by title and add to new playlist
billboard_playlist_id = billboard_playlist["id"]
result_artist_id_list = []
result_song_id_list = []
for i in range(100):
    result_song = sp.search(q='track:' + top_songs_list[i], type='track', limit=1)
    try:
        result_song_id = result_song["tracks"]["items"][0]["id"]
        result_song_id_list.append(result_song_id)
    except IndexError:
        pass

sp.playlist_add_items(billboard_playlist_id, result_song_id_list, position=None)

