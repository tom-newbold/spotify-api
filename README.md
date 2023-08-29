A basic light-weight spotify web-app for displaying the currently playing track for the attached account.

Both a venv and `requirements.txt` are provided to aid in running.
Exectuting `spotify_client.py` will start the flask server, and navivating to the indicated IP will prompt spotify login (these details should be saved by your browser for future iterations).
Alternatively, run the provided `server.bat` file.

Authentication details, found on your personal [Spotify for Developers](https://developer.spotify.com/) dashboard, need to be added into the blank `config.json` provided.

#### Currently working on:

<i>/playlist_followers/ page</i> - This should be able to show all your playlists, and fetch the usernames of those who follow it (as long as they follow you). Unfortunately, I have run into some problems when developing this, and it seems it might not be possible; due to a combination of "missing" endpoint functionality on Spotify's end, as well as indeterminate scope and/or permission issues.
