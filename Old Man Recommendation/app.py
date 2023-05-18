from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        artist_name = request.form.get('artist')  # Get the artist name from the form
        client_credentials_manager = SpotifyClientCredentials(client_id='78bd4216655a4f1d917e1962f8f1a6a4', client_secret='163c01a6e7f843d2a7a8d4aeeb320019')
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        results = sp.search(q='artist:' + artist_name, type='artist')  # Search for the artist
        try:
            artist_id = results['artists']['items'][0]['id']  # Get the artist's Spotify ID
            related_artists = sp.artist_related_artists(artist_id)  # Get related artists

            artist_data = []
            for artist in related_artists['artists'][:10]:  # Limit to top 10 related artists to avoid too many requests
                albums = sp.artist_albums(artist['id'], album_type='album')  # Get the artist's albums
                latest_album_date = max(album['release_date'] for album in albums['items'][:5])  # Get the latest release date from the top 5 albums
                artist_data.append((artist['name'], latest_album_date))

            artist_data.sort(key=lambda x: x[1], reverse=True)  # Sort the artists by the latest release date
            related_artists_sorted = [artist[0] for artist in artist_data]  # Get the list of artist names
        except IndexError:
            return "Artist not found"

        return render_template('artists.html', artists=related_artists_sorted)  # Return the sorted list of related artists
    return render_template('index.html')  # Render the form


if __name__ == '__main__':
    app.run(debug=True)
