from venv import create
from xxlimited import new
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth

from flask import Flask, request, url_for, session, redirect

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Cookie'
app.secret_key = 'asd082&*#!3kjah!@sd0jasdkKAJS0qjd'

TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    
    token_info = create_spotify_oauth().get_access_token(code)
    
    session[TOKEN_INFO] = token_info
    
    return redirect(url_for('recommend_songs', _external= True))


@app.route('/recommend')
def recommend_songs():
    try: 
        token_info = get_token()
    except:
        print('User not logged in')
        return redirect("/")

    sp = spotipy.Spotify(auth=token_info['access_token'])

    curr_user_id = sp.current_user()['id']

    top_tracks = sp.current_user_top_tracks()
    top_artists = sp.current_user_top_artists()

    recommended_playlist = sp.user_playlist_create(curr_user_id, "New Recommended Songs", True)
    recommended_playlist_id = recommended_playlist['id']
    
    track_seeds = []
    artist_seeds = []
    genre_seeds = sp.recommendation_genre_seeds

    for i in range(20):
        #get current track id -> add to track_seeds
        #get current artist id -> add to artist_seeds

    recommended_songs = recommendations(artist_seeds, genre_seeds, track_seeds)

    song_uris = []
    for song in recommended_songs:
        uri = song['uri']
        song_uris.append(uri)
    
    sp.user_playlist_add_tracks(curr_user_id, recommended_playlist_id, song_uris, None)

    return ('Recomended song playlist successfully created and added to current user account. Enjoy!')

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', external=False))
    
    now = int(time.time())

    is_expired  = token_info['expires_at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = 'c41a2733e2ce41b0b45ea49cbdfed264',
        client_secret = '4fc77b7c2ab34d408fdff7d01e3b3907',
        redirect_uri = url_for('redirect_page', _external= True),
        scope = 'user-library-read playlist-modify-public playlist-modify-private'
    )

app.run(debug=True)
