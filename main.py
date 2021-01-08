import spotipy
from spotipy.oauth2 import SpotifyOAuth

REDIRECT_URI = "http://example.com"
PLAYLIST_URL = "https://open.spotify.com/playlist/48kylwDuk11a83UIddnfbf"
AFRICA_TOTO_URL = "https://open.spotify.com/track/3ZPKocroJIcnHGcnJVlLKD"


# Get keys from private files
clientID = ""
with open("clientid.dat", "r") as f:
    clientID = f.read()

clientSecret = ""
with open("clientsecret.dat", "r") as f:
    clientSecret = f.read()


# Init Spotify object
auth_manager = SpotifyOAuth(client_id=clientID, client_secret=clientSecret, username="sneakypancake17", scope="playlist-modify-public", redirect_uri=REDIRECT_URI)
sp = spotipy.Spotify(auth_manager=auth_manager)


# Add Africa to Playlist
user = sp.user("sneakypancake17")
sp.user_playlist_add_tracks(user, PLAYLIST_URL, [AFRICA_TOTO_URL])