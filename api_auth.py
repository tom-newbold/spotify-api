import json
with open('config.json','r') as config:
    config_loaded = json.load(config)
client_id = config_loaded['client_id']
client_secret = config_loaded['client_secret']
redirect_uri = config_loaded['redirect_uri']
authorization_base_url = config_loaded['authorization_base_url']
token_url = config_loaded['token_url']

from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

def get_auth_session(scope):
    return OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

def create_auth_session_w_token(token):
    return OAuth2Session(client_id, token=token, redirect_uri=redirect_uri)

def get_auth_url(auth_session):
    authorization_url, state = auth_session.authorization_url(authorization_base_url)
    return auth_session, authorization_url

def get_token(auth_session, redirect_response):
    if "https" not in redirect_response and "http" in redirect_response:
        redirect_response = redirect_response.replace("http","https")
    
    auth = HTTPBasicAuth(client_id, client_secret)
    token = auth_session.fetch_token(token_url, auth=auth,authorization_response=redirect_response)

    return token