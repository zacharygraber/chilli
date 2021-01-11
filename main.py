import spotipy
from spotipy.oauth2 import SpotifyOAuth
import discord
import asyncio

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

botToken = ""
with open("bottoken.dat", "r") as f:
    botToken = f.read()

# Init Spotify OAuth and manager object
auth_manager = SpotifyOAuth(client_id=clientID, client_secret=clientSecret, username="sneakypancake17", scope="playlist-modify-public", redirect_uri=REDIRECT_URI)
sp = spotipy.Spotify(auth_manager=auth_manager)
user = sp.user("sneakypancake17")

# Init Discord bot
client = discord.Client()
prefix = "&"

## Discord Bot Events ###########################################

@client.event
async def on_ready():
    print("Successfully connected.")

@client.event
async def on_message(message):
    # Protect against responding to bot's own messages
    if message.author == client.user:
        return
    
    # Quickly weed out messages not meant for the bot
    if not message.content.startswith(prefix):
        return

    if message.content.startswith(prefix + "list add"):
        # If the query is blank, don't do anything
        if message.content.replace(" ", "") == prefix+"listadd":
            await message.channel.send("Please give me a valid search query!")
            return

        query = message.content.replace(prefix+"list add ","").replace(" ","+")
        searchResults = (sp.search(query, limit=10, offset=0, type="track"))["tracks"]["items"]

        # TODO
        trackURL = searchResults[0]["external_urls"]["spotify"]

        channel = message.channel
        await channel.send("So you want me to add this track to the playlist?\n" + trackURL)
        botMessage = channel.last_message
        await botMessage.add_reaction("✅")
        await botMessage.add_reaction("❌")

        def check(reaction, user):
            if user == message.author:
                userReaction = str(reaction.emoji)
                if userReaction == "✅" or userReaction == "❌":
                    return True

            return False

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await channel.send("Track add aborted (timed out).")
        else:
            if str(reaction.emoji) == "✅":
                # Add the first search result to the playlist
                sp.user_playlist_add_tracks(user, PLAYLIST_URL, [trackURL])
                await channel.send("Added track. See the newly-renovated playlist here:\n" + PLAYLIST_URL)
            else:
                # Cancel
                await channel.send("Track add cancelled. Let me know if you need me again!")

#################################################################
client.run(botToken)