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

    # Adding tracks to the list
    if message.content.startswith(prefix + "list add"):
        # If the query is blank, don't do anything
        if message.content.replace(" ", "") == prefix+"listadd":
            await message.channel.send("Please give me a valid search query!")
            return

        query = message.content.replace(prefix+"list add ","").replace(" ","+")
        searchResults = (sp.search(query, limit=10, offset=0, type="track"))["tracks"]["items"]
        if len(searchResults) == 0:
            await message.channel.send("No results found. Try again with a new query?")
            return

        index = 0
        trackURL = searchResults[index]["external_urls"]["spotify"]

        channel = message.channel
        await channel.send("Here's what I found. Which track are you looking for? (❌ to cancel)\n" + trackURL)
        botMessage = channel.last_message
        await botMessage.add_reaction("✅")
        await botMessage.add_reaction("❌")
        if len(searchResults) > 1:
            await botMessage.add_reaction("➡️")
        while True:

            def check(reaction, user):
                if user == message.author:
                    userReaction = str(reaction.emoji)
                    if userReaction == "✅" or userReaction == "❌":
                        return True
                    elif index < (len(searchResults) - 1) and userReaction == "➡️": # A "next" arrow is a valid response as long as this is not the last element.
                        return True
                    elif index > 0 and userReaction == "⬅️":
                        return True

                return False

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
        
            except asyncio.TimeoutError:
                await botMessage.delete()
                await channel.send(message.author.mention + " Track add aborted (timed out).")
                return

            else:
                if str(reaction.emoji) == "✅":
                    # Add the first search result to the playlist
                    sp.user_playlist_add_tracks(user, PLAYLIST_URL, [trackURL])
                    await botMessage.delete()
                    await channel.send("Added track. See the newly-renovated playlist here:\n" + PLAYLIST_URL)
                    return

                elif str(reaction.emoji) == "➡️":
                    # Suggest the next result
                    await botMessage.remove_reaction("➡️", message.author)
                    index += 1
                    trackURL = searchResults[index]["external_urls"]["spotify"]
                    if index == 1:
                        await botMessage.clear_reaction("➡️")
                        await botMessage.add_reaction("⬅️")
                        await botMessage.add_reaction("➡️")
                    if index == len(searchResults) - 1:
                        await botMessage.clear_reaction("➡️")
                    
                    await botMessage.edit(content="Here's what I found. Which track are you looking for? (❌ to cancel)\n" + trackURL)

                elif str(reaction.emoji) == "⬅️":
                    # Go back to the previous
                    await botMessage.remove_reaction("⬅️", message.author)
                    index -= 1
                    trackURL = searchResults[index]["external_urls"]["spotify"]
                    if index == 0:
                        await botMessage.clear_reaction("⬅️")
                    if index < len(searchResults) - 1:
                        await botMessage.add_reaction("➡️")

                    await botMessage.edit(content="Here's what I found. Which track are you looking for? (❌ to cancel)\n" + trackURL)
                    
                else:
                    # Cancel
                    await botMessage.delete()
                    await channel.send("Track add cancelled. Let me know if you need me again!")
                    return

    # Get the list
    if message.content == (prefix + "list play"):
        await message.channel.send("Due to budgeting concerns, we are currently outsourcing playback. Please paste this command into Discord:\n-play " + PLAYLIST_URL)
        return

    # Offer a hug
    if message.content.startswith(prefix + "hug"):
        await message.channel.send("Ugh, fine. I guess you are my little pogchamp " + message.author.mention + ". Come here.", file=discord.File("hug.jpg"))
        return

#################################################################
client.run(botToken)