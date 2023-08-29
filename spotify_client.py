import sys

from flask import Flask, request, session, redirect, url_for, render_template

from api_auth import get_auth_session, create_auth_session_w_token, get_auth_url, get_token
from api_auth import client_secret

app = Flask(__name__)
app.secret_key = client_secret
app.config['SESSION_TYPE'] = 'filesystem'

spotify_endpoint_url = "https://api.spotify.com/v1"
scope = ["user-read-currently-playing", "user-read-playback-state", "user-read-recently-played"]
error_codes = [401,503]

def error_handler(request):
    '''Checks for and deals with specific error codes associated with the intial request'''
    if request.status_code in error_codes:
        return redirect(url_for('auth'))
    elif request.status_code==429:
        return "Rate Limit Reached: Check developer dashboard<br>You may need to generate a new API key."
    if request.status_code==204:
        auth_session = create_auth_session_w_token(session['AUTH_TOKEN'])
        _, track, progress = fallback(auth_session)
        return home(track, progress, track['album'], 'playlist')
    else:
        return True

@app.route('/')
def auth():
    '''Generates authentication url and redirects to it'''
    _, url = get_auth_url(get_auth_session(scope))
    return redirect(url)

@app.route('/callback/')
def token():
    '''Handles callback by extracting authentication token from url'''
    token = get_token(get_auth_session(scope), request.url)
    session['AUTH_TOKEN'] = token
    return redirect(url_for('playing'))

@app.route('/playing/')
def playing():
    '''Calls the API to find the current playing track,
    Uses fallback() if this is not accessable'''
    auth_session = create_auth_session_w_token(session['AUTH_TOKEN'])
    r = auth_session.get(f"{spotify_endpoint_url}/me/player")
    error_check = error_handler(r)
    if error_check!=True:
        return error_check
    else:
        response = r.json()
        if "is_playing" not in response:
            response, track, progress = fallback(auth_session)
        elif response["is_playing"]:
            track = response['item']
            session['id'] = track['id']
            progress = [response['progress_ms'],response['item']['duration_ms']]
            session['progress'] = progress
        else:
            response, track, progress = fallback(auth_session)
    return home(track, progress, track['album'], 'playlist')

@app.route('/playing/playlist/')
def playlist():
    '''Same as playing() but fetches playlist information to display'''
    auth_session = create_auth_session_w_token(session['AUTH_TOKEN'])
    r = auth_session.get(f"{spotify_endpoint_url}/me/player")
    error_check = error_handler(r)
    if error_check!=True:
        return error_check
    else:
        response = r.json()
        if "is_playing" not in response:
            response, track, progress = fallback(auth_session)
        elif response["is_playing"]:
            track = response['item']
            session['id'] = track['id']
            progress = [response['progress_ms'],response['item']['duration_ms']]
            session['progress'] = progress
            if 'context' in response:
                if response['context']['type']=='playlist':
                    _r = auth_session.get(f"{spotify_endpoint_url}/playlists/{response['context']['uri'].split(':')[-1]}")
                    playlist = _r.json()
                    session['p_id'] = playlist['id']
                    return home(track, progress, playlist, 'playing')
        else:
            response, track, progress = fallback(auth_session)
            if 'p_id' in session:
                r = auth_session.get(f"{spotify_endpoint_url}/playlists/{session['p_id']}")
                response = r.json()
                playlist = response
                return home(track, progress, playlist, 'playing')
    return home(track, progress, track['album'], 'playing')

def fallback(auth_session):
    '''Uses session cache if it exists,
    Otherwise, call the API again to fetch the most recently played track'''
    if 'id' in session:
        r = auth_session.get(f"{spotify_endpoint_url}/tracks/{session['id']}")
        response = r.json()
        track = response
        progress = session['progress']
    else:
        r = auth_session.get(f"{spotify_endpoint_url}/me/player/recently-played?limit=1")
        response = r.json()
        track = response['items'][0]['track']
        progress = [0,0]
    return response, track, progress

def home(track, progress, album, next_view):
    '''Simply renders template with track/album information'''
    return render_template('now_playing.html', track_name=track['name'], track_progress=progress,
                           album_name=album['name'], album_art_link=album['images'][0]['url'],
                           next_view_url=url_for(next_view))


if __name__ == '__main__':
    print(f'Running in venv: {sys.prefix != sys.base_prefix}')
    app.run(port=8000)
