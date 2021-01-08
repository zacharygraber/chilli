import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

PLAYLIST_URL = "https://open.spotify.com/playlist/48kylwDuk11a83UIddnfbf"

clientID = ""
with open("clientid.dat", "r") as f:
    clientID = f.read()

clientSecret = ""
with open("clientsecret.dat", "r") as f:
    clientSecret = f.read()

sp = spotipy.Spotify(auth_manager = SpotifyClientCredentials(client_id = clientID, client_secret = clientSecret))
print("Successfully authenticated with Spotify Web API")

user = sp.user("sneakypancake17")

playlist = sp.user_playlist(user, playlist_id = PLAYLIST_URL)
print(playlist)