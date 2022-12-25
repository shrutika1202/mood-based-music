# imports
import pandas as pd
import random
import numpy as np
from numpy.linalg import norm
import tekore as tk
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# authorize spotify client
def authorize():
    CLIENT_ID = '018d93f2ca0d444a91a17019923c7204'
    CLIENT_SECRET = '1f560bde80154336a6da253537ce0c3e'
    app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
    return tk.Spotify(app_token)

# calculate distance between two points
def distance(p1, p2):
    distance_x = p2[0]-p1[0]
    distance_y = p2[1]-p1[1]
    distance_vec = [distance_x, distance_y]
    norm = (distance_vec[0]**2 + distance_vec[1]**2)**(1/2)
    return norm

# read dataset
df = pd.read_csv('valence_arousal_dataset.csv')
# get valence and energy as list
df["mood_vec"] = df[["valence", "energy"]].values.tolist()

print(df['mood_vec'])

# authorize client
sp = authorize()

# recommend 5 tracks
def recommend(track_id, ref_df, sp, n_recs = 5):
    
    # Crawl valence and arousal of given track from spotify api
    track_features = sp.track_audio_features(track_id)
    track_moodvec = np.array([track_features.valence, track_features.energy])
    
    # Compute distances to all reference tracks
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    # Sort distances from lowest to highest
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    # If the input track is in the reference set, it will have a distance of 0, but should not be recommendet
    ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    
    # Return n recommendations
    return ref_df_sorted.iloc[:n_recs]

# give song_id and recommend

def mood_based_recommend(mood):
    if(mood == 'happy'):
        new_track_id = "5nujrmhLynf4yMoMtj8AQF"
    elif(mood == 'anxiety'):
        new_track_id = "4VrWlk8IQxevMvERoX08iC"
    elif(mood == 'sad'):
        new_track_id = "2BN5ZMErVAhbEroB99b3no"
    elif(mood == 'angry'):
        new_track_id = "41b1nydaPsdAn4R3sqoVWu"
    elif(mood == 'disgust'):
        new_track_id = "3rJgVV3jjhFQc5CumVMsaT"

    re = recommend(track_id = new_track_id, ref_df = df, sp = sp, n_recs = 5)

    return re




















# ######## accepting song ID from user ########
# CLIENT_ID = '018d93f2ca0d444a91a17019923c7204'
# CLIENT_SECRET = '1f560bde80154336a6da253537ce0c3e'

# #Authentication - without user
# client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# # https://towardsdatascience.com/deploying-a-spotify-recommendation-model-with-flask-20007b76a20f

# # breaking shared spotify url of track to get song ID
# url = 'https://open.spotify.com/track/0og9wKFGgFFNQnrBe7eisG?si=Q4tNahcAR_qfscWizkh3cg&utm_source=copy-link'
# id = (url.split('/'))[-1].split('?')[0]
# id

# link = 'https://open.spotify.com/track/'+id
# sp.audio_features(link)[0]




