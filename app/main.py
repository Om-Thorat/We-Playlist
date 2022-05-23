import spotipy, time
import json
import os
import requests
import spotipy.util as util
import sys
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, render_template, redirect, url_for, request
app=Flask(__name__)
playlist_id=""
@app.before_request
def before_request():
    if 'DYNO' in os.environ:
        if request.base_url.startswith('http://'):
            url = request.base_url.replace('http://', 'https://', 1)
            print(request.base_url)
            print(url)
            return redirect(url)
@app.route('/')
def home():
                return render_template("index.html")
@app.route('/Make')
def make():       
                return render_template("Make.html")
@app.route('/Make', methods=['POST'])
def make_post():
                pname = request.form['text']
                global playlist_id
                username="myusername"
                scope="playlist-modify-public"
                spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
                tokenauth = util.prompt_for_user_token(username,scope,client_id="XXXXXXXXXXXXXXXXXXXXX",client_secret="XXXXXXXXXXXXXXXXXXXXXX",redirect_uri='http://localhost:8888/callback')
                print(tokenauth)
                sp = spotipy.Spotify(auth=tokenauth)
                user_id = "90xeph4nzjsa3yvaaf4e7d49i"
                endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
                request_body = json.dumps({
                          "name": pname,
                          "description": f"Playlist by WePlaylist!",
                          "public": True
                        })
                response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                                        "Authorization":f"Bearer {tokenauth}"})
                playlist_id = response.json()['id']
                print("here is your playlist")
                return render_template('load.html', value=playlist_id)
@app.route('/<playlist_id>')
def redirect(playlist_id):
                x=(request.base_url)
                playlist_idurl=(x[33:])
                return render_template('edit.html', value=playlist_idurl)
@app.route('/<playlist_id>',  methods=['POST'])
def redirect_post(playlist_id):
                        x=(request.base_url)
                        print(x[33:])
                        playlist_idurl=(x[33:])
                        username="myusername"
                        scope="playlist-modify-public"
                        spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
                        tokenauth = util.prompt_for_user_token(username,scope,client_id="XXXXXXXXXXXXXXXXXXXXX",client_secret="XXXXXXXXXXXXXXXXXXXXXX",redirect_uri='http://localhost:8888/callback')
                        print(tokenauth)
                        sp = spotipy.Spotify(auth=tokenauth)
                        user_id = "90xeph4nzjsa3yvaaf4e7d49i"
                        endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
                        try:
                                q = request.form['song']
                                print(q)
                                try:
                                        results = (spotify.search(q,limit=1,type='track'))
                                        spotifyid =[results['tracks']['items'][0]['id']]
                                        sp.user_playlist_add_tracks(username, playlist_idurl,spotifyid, position=None)
                                        print(f"added {q} to playlist")
                                except:
                                        return render_template('error.html' , value=x)
                        except:
                                print("no song input")
                        try:
                                r = request.form['remove']
                                print(r)
                                try:
                                        results = (spotify.search(r,limit=1,type='track'))
                                        spotifyidremove =[results['tracks']['items'][0]['id']]
                                        sp.user_playlist_remove_all_occurrences_of_tracks(user_id,playlist_idurl,spotifyidremove)
                                except:
                                        return render_template("error.html", value=x)
                        except:
                                print("no remove input")
                        try:
                                m = request.form['move']
                                print(m)
                                try:
                                        playlist_reorder_items(playlist_idurl,m[:1],m[2:])
                                except:
                                        return render_template("error.html")
                        except:
                                print("no move input")
                        return render_template('edit.html', value=playlist_idurl)

@app.route('/Find')
def find():
                return render_template('Find.html')
@app.route('/Find', methods=['POST'])
def find_post():
        playlist_id= request.form['text']
        return render_template('load.html', value=playlist_id)
app.run()
