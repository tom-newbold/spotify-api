An early version of a light-weight spotify web-app for displaying currently playing track for the attached account.

Both a venv and `requirements.txt` are provided to aid in running.
Exectuting `spotify_client.py` will start the flask server, and navivating to the indicated IP will prompt spotify login (these details should be saved by your browser for future iterations).
Alternatively, run the provided `server.bat` file.

Authentication details, found on your personal [Spotify for Developers](https://developer.spotify.com/) dashboard, need to be added into the blank `config.json` provided.

Known areas which will be improved:
- Need better encapsulation for separate pages, as the high level request error code handling is the same for all pages
- An issue with the /playlist/ page when only recently played tracks are available is currently only handled by a try: except:
