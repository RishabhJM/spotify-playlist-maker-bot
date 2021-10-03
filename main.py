from selenium import webdriver
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import itertools
import pprint

client_secret = "8ae35fe728ab4aa8bee14841a9244877"
client_id = "5e31483916514a379a99760e8a08a846"
redirect_uri = "http://example.com"
username = "o86pl3i1oot87lj8wo7n6a5h9"
scope = "playlist-modify-private"

date = input("Which year do you want to travel to? type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]

URL = "https://www.billboard.com/charts/hot-100/" + date

chrome_executable_path = "C:\Development\chromedriver.exe"
driver = webdriver.Chrome(chrome_executable_path)
driver.get(URL)

song_elements = driver.find_elements_by_class_name("chart-element__information__song")
tracks = [e.text for e in song_elements]

# artist_elements = driver.find_elements_by_class_name("chart-element__information__artist")
# artists = [a.text for a in artist_elements]
#
# tracks_final = []
#
# for (t,a) in zip(tracks,artists):
#         tracks_final.append({"track":t,"artist":a})




sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    ))
user = sp.user(username)["id"]

track_uris = []

# for song in tracks_final:
#         song_name = song["track"]
#         song_artist = song["artist"]
#         search_element = sp.search(q=f"track: {song_name} year: {year} artist:{song_artist}", type="track")
for song in tracks:
        search_element = sp.search(q=f"track: {song} year: {year}", type="track")

        try:
                uri = search_element["tracks"]["items"][0]["uri"]
                track_uris.append(uri)
        except IndexError:
                print(f"{song} doesn't exist on Spotify.Skipped.")


playlist = sp.user_playlist_create(user=user,name=f"{date} Billboard 100",public=False,description=f"Top 100 songs on Billboard on {date}")
playlist_id = playlist["id"]

sp.user_playlist_add_tracks(user=user,playlist_id=playlist_id,tracks=track_uris,position=None)




driver.close()
