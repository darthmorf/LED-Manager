import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from PIL import Image
import requests
from io import BytesIO

scope = 'user-read-currently-playing'

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="3db3ce732b68473aaa810f74dcaeb433", client_secret="3cdff1f9ac89488285027b5f2330558e", redirect_uri="http://localhost:8888/callback", scope=scope))
current_track = spotify.current_user_playing_track()

url = current_track["item"]["album"]["images"][0]["url"]


response = requests.get(url)
im = Image.open(BytesIO(response.content)) 
px = im.load()
print(px[0,0])