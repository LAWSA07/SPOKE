from flask import render_template, request, jsonify, redirect, session, url_for
from app import app
from .api import create_spotify_oauth, get_spotify_client
from firebase_admin import auth
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if not session.get('token_info'):
        return render_template('signin.html')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_token = request.json['idToken']
        try:
            decoded_token = auth.verify_id_token(id_token)
            user_id = decoded_token['uid']
            session['user'] = user_id
            return jsonify({'status': 'success'})
        except:
            return jsonify({'error': 'Invalid token'}), 401
    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/search')
@login_required
def search():
    if not session.get('token_info'):
        return redirect(url_for('login'))
        
    spotify = get_spotify_client()
    if not spotify:
        return redirect(url_for('login'))
        
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    results = spotify.search(q=query, limit=10, type='track')
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
    
    return render_template('results.html', songs=songs, query=query) 