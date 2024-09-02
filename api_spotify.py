#Code was constructed with Spotipy API and ChatGPT referencing SpotipyAPI.

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import heapq

# Replace with your client ID and client secret
client_id = 'f32e47f002124474834dc28b01450218'
client_secret = 'bd65693f357544e794e1090acccdfc46'

# Set up client credentials
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# tools to use from Spotipy
playlist_id = '37i9dQZF1E39pCaJfDcdb8'
playlist_ob = sp.playlist_tracks(playlist_id)
tracks = playlist_ob['items']

print('--- TRACKS IN PLAYLIST ---')
for item in tracks:
    track = item['track'] # tracks contains id, name, artisit, album data, and more
    print(track['name'])
    
# reading in albums from an artist
artist_id = '2jbd7OqeJJd1hz81vOXwwW'
albums_ob = sp.artist_albums(artist_id = artist_id, album_type='single')
albums = albums_ob['items']

print('--- ALBUMS IN ARTIST ---')
for album in albums:
    print(album['name'])
    
# reading in tracks from an album
album_id = '26rTTXIEtEeSTan28AiLaV'
tracks_ob = sp.album_tracks(album_id)
tracks = tracks_ob['items']

print('--- TRACKS IN ALBUM ---')
for track in tracks:
    print(track['name'])
    
# cool track feature
print('--- TRACK FEATURE ---')
track_id = '7qzQfE2se3Ai5reZcxs920'
audio_features = sp.audio_features(track_id) # audio features, audio analysis, etc.
print(audio_features[0]['danceability'])
#end of tools to use from Spotipy



#input artist's name
artist_name_input=input("Enter artist's name: ")

#search for the artist
results = sp.search(q=artist_name_input,type="artist",limit=1,market="US")



year=[]
popularity_average=[]
#Check if the artist name exists and print artist details
if results['artists']['items']:
    #save the artist tracking ID
    artist_id = results['artists']['items'][0]['id']
    artist_name = results['artists']['items'][0]['name']

    #check artist's name is exactly the same
    if artist_name == artist_name_input:
        artist_info = sp.artist(artist_id)

        followers = artist_info['followers']['total']
        genres = artist_info['genres']
        print(f"Followers: {followers}")
        print(f"Genres: {', '.join(genres)}")
        print("Here are the albums and tracks of", artist_name_input)
    
    #if not, exit the script
    else:
        print("No artist exist")
        exit("Exiting the script")


#function to get all albums from the artist
def get_all_albums(artist_id):
    albums = []
    #find albums
    results = sp.artist_albums(artist_id, album_type='album')  
    albums.extend(results['items'])
    
    # move to next page, if there is one
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    
    return albums


# use the artist ID we obtained earlier to fetch all the albums.
albums = get_all_albums(artist_id)

#get all tracks from each album
def get_all_tracks_from_album(album_id):
    tracks = []
    #find tracks
    results = sp.album_tracks(album_id)
    tracks.extend(results['items'])
    
    # move to next page, if there is one
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    return tracks



#the dict is for later use of print out 5 top songs fron the artist
track_pop_dict={}

# print album names, release date, and tracks of each album
for album in albums:
    #save all popularity of each song in a specific album in one list
    popularity_for_all=[]
    #save all track's name from a specific albun in one list
    all_track=[]

    # print album names and release date
    print(f"\nAlbum: {album['name']}")
    print("Released date: ", album['release_date'])

    # use function get_all_tracks_from_album to get all the tracks of each album
    album_tracks = get_all_tracks_from_album(album['id'])
    for track in album_tracks:
        print(track['name'])
        all_track.append(track['name'])
        
        track_id = track['id']
        market = 'US'
        track_info = sp.track(track_id)

        # Print track popularity
        popularity = track_info['popularity']
        popularity_for_all.append(popularity)

        track_pop_dict[track['name']]=popularity
        
        print(f"Popularity Score: {popularity}")
    print("Popularity Average Score:", round((sum(popularity_for_all)/len(popularity_for_all)),2))

    #get the highest popularity
    highest_pop = max(popularity_for_all)
    index_of_max = popularity_for_all.index(highest_pop)
    #print the more popular song
    print("Most popular song in this album is", all_track[index_of_max])

    #save the average score of popularity(will use it to vreate a plot)
    
    popularity_average.append(sum(popularity_for_all)/len(popularity_for_all))

    # save the released year into date(will use it to create a plot)
    year.append(album['release_date'].split('-')[0])

# using popularity to fetch top 5 songs from the artist
top_5_songs = heapq.nlargest(5, track_pop_dict.items(), key=lambda item: item[1])
top_5_song_names = [song for song, score in top_5_songs]

print("\nTop 5 songs from", artist_name_input)
for i in range(0,5):
    print("\n",top_5_song_names[i])

#let it sort from oldest to newest
year.reverse()
popularity_average.reverse()

#set the figure size
plt.figure(figsize=(10, 6))  




#create a plot of average popularity of each album by release year
plt.plot(year,popularity_average, color='blue', label='Popularity',marker=".")
#label for the x-axis
plt.xlabel('Year')  
#label for the y-axis
plt.ylabel('Average Popularity')  
#title of the plot
plt.title('Average Popularity of Each Album by Release Year')
#rotate x-ticks
plt.xticks(rotation=45) 
#add legend
plt.legend()
plt.grid(True)
plt.show()