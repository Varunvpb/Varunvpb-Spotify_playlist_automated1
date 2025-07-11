from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID='aee86ec44d334f9e88dffec5276c4fa8'
SPOTIPY_CLIENT_SECRET='cdaa3bf70e3845ff94017e86186a45a9'
SPOTIPY_REDIRECT_URI='https://example.com/'


header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"}
date = input()
url = "https://www.billboard.com/charts/hot-100/" + date
response = requests.get(url = url,headers= header)

soup = BeautifulSoup(response.text,'html.parser')

list1 = soup.select(selector="li ul li h3")
song_names = [song.getText().strip() for song in list1]   #list comprehension
print(song_names)

list2 = soup.select(selector="li ul li span")
artist_names = [name.getText().strip() for name in list2[::7]]
#print(artist_names)

songs = dict(zip(song_names,artist_names))
#print(songs)

#aee86ec44d334f9e88dffec5276c4fa8 id
#cdaa3bf70e3845ff94017e86186a45a9 secret

scope = "user-library-read playlist-modify-public playlist-modify-private"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="aee86ec44d334f9e88dffec5276c4fa8",
    client_secret="cdaa3bf70e3845ff94017e86186a45a9",
    redirect_uri="https://example.com/",
    scope=scope
))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])
user_id = sp.current_user()["id"]
print(user_id)

track_id = []

for so in song_names:
    result = sp.search(q=so,limit=1,type="track")
    track_id.append(result['tracks']['items'][0]['id'])

playlist = sp.user_playlist_create(user = user_id,name= f"top 100 on {date} ", public=True, collaborative=False, description='')
p_id = playlist["id"]
sp.user_playlist_add_tracks(user=user_id,playlist_id = p_id, tracks= track_id, position=None)
