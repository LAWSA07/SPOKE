import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import current_app, session, url_for

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=current_app.config['SPOTIFY_CLIENT_ID'],
        client_secret=current_app.config['SPOTIFY_CLIENT_SECRET'],
        redirect_uri=current_app.config['SPOTIFY_REDIRECT_URI'],
        scope='user-library-read playlist-read-private'
    )

def get_spotify_client():
    if not session.get('token_info'):
        return None
        
    sp_oauth = create_spotify_oauth()
    token_info = session.get('token_info')
    
    # Check if token needs refresh
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
        
    return spotipy.Spotify(auth=token_info['access_token'])

def search_songs(query, limit=10):
    spotify = get_spotify_client()
    results = spotify.search(q=query, limit=limit, type='track')
    
    songs = []
    for track in results['tracks']['items']:
        song = {
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'preview_url': track['preview_url']
        }
        songs.append(song)
    return songs 