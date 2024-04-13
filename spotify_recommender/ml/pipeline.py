import pandas as pd
import logging
import spotipy
from funcy import chunks
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

#helper functions from Brenner Swenson https://github.com/brennerswenson/spotify-recommendations/blob/master/ml/helper_functions.py
def get_saved_tracks(username, token, results, sp):

    if token:

        # GET USER'S SAVED SONGS

        saved_tracks = sp.current_user_saved_tracks()  
        saved_tracks_final = saved_tracks["items"] 

        while saved_tracks["next"]:
            saved_tracks = sp.next(saved_tracks)
            saved_tracks_final.extend(saved_tracks["items"])

        for i in range(len(saved_tracks_final)):
            song_id = saved_tracks_final[i]["track"]["id"]
            if song_id not in results.keys():  # only get info for songs that aren't already in the list

                results[song_id] = {
                    "song_name": saved_tracks_final[i]["track"]["name"],
                    "duration_ms": saved_tracks_final[i]["track"]["duration_ms"],
                    "artist_name": saved_tracks_final[i]["track"]["artists"][0]["name"],
                    "artist_id": saved_tracks_final[i]["track"]["artists"][0]["id"],
                    "album_id": saved_tracks_final[i]["track"]["album"]["id"],
                    "album_name": saved_tracks_final[i]["track"]["album"]["name"],
                    "release_date": saved_tracks_final[i]["track"]["album"]["release_date"],
                    "popularity": saved_tracks_final[i]["track"]["popularity"],
                    "explicit": saved_tracks_final[i]["track"]["explicit"],
                }

        # create dataframe from song data
        df = pd.DataFrame(results).T

        df = df.dropna()

        return results, df

    else:
        logging.info(f"Can't get token for {username}")

def get_song_info(results, df, username, token, sp):
    '''
    if token:

        audio_features = dict()  # results dict for deep features

        # iterate through song ids in batches of 45
        for id_batch in chunks(45, results.keys()):
            # get audio features for batch
            try:
                batch_audio_features = sp.audio_features(id_batch)

                # create dictionary of song ids and features
                temp_dict = dict(zip(id_batch, batch_audio_features))

                # update main dictionary with results
                audio_features.update(temp_dict)
            except AttributeError:
                logging.info("ERROR AT {}".format(id_batch))
                continue

        # columns to drop
        drop_columns = ["duration_ms", "type", "analysis_url", "track_href", "uri", "id"]

        # create df from deep features and drop columns
        audio_features_df = pd.DataFrame(audio_features).T.drop(drop_columns, axis=1)

        # merge main df with deep df
        df = df.join(audio_features_df, on=df.index)
        return audio_features, df
    else:
        logging.info(f"Can't get token for {username}")     
    '''
    if token:
        audio_features = dict()  # results dict for deep features

        # iterate through song ids in batches of 45
        for id_batch in chunks(45, results.keys()):
            # get audio features for batch
            try:
                batch_audio_features = sp.audio_features(id_batch)

                # create dictionary of song ids and features
                temp_dict = dict(zip(id_batch, batch_audio_features))

                # update main dictionary with results
                audio_features.update(temp_dict)
            except AttributeError:
                logging.info("ERROR AT {}".format(id_batch))
                continue

        # columns to drop
        drop_columns = ["duration_ms", "type", "analysis_url", "track_href", "uri", "id"]

        # create df from deep features and drop columns
        audio_features_df = pd.DataFrame(audio_features).T

        # Drop columns that exist in the DataFrame
        existing_columns = df.columns.tolist()
        columns_to_drop = [col for col in drop_columns if col in existing_columns]
        df_cleaned = df.drop(columns=columns_to_drop, axis=1)

        # Add missing columns with None values
        for col in drop_columns:
            if col not in df_cleaned.columns:
                df_cleaned[col] = None

        # merge main df with deep df
        df_cleaned = df_cleaned.join(audio_features_df, on=df_cleaned.index)

        return audio_features, df_cleaned

    else:
        logging.info(f"Can't get token for {username}")

def get_artist_info(df, username, token, sp):
    if token:

        all_artists = dict()

        # iterate in batches

        for artist_id_batch in chunks(20, df["artist_id"].unique()):
            try:
                batch_artists = sp.artists(artist_id_batch)
                batch_artists = batch_artists["artists"]
                for i, artist_id in enumerate(artist_id_batch):
                    # get only attributes that are needed
                    all_artists[artist_id] = {
                        "artist_followers": batch_artists[i]["followers"]["total"],
                        "artist_genres": batch_artists[i]["genres"],
                        "artist_popularity": batch_artists[i]["popularity"],
                    }
            except AttributeError:
                logging.info("ERROR AT {}".format(artist_id_batch))

        # create df of artists data
        artists_df = pd.DataFrame(all_artists).T
        artists_df["artist_genres"] = artists_df.artist_genres.apply(
            lambda x: [i.replace(" ", "_") for i in x]
        )

        df = df.join(artists_df, on="artist_id")

        return artists_df, df

    else:
        logging.info(f"Can't get token for {username}")

def clean_data(df):
    high_level_genres = [
        "hip_hop",
        "pop",
        "rap",
        "electro",
        "edm",
        "metal",
        "chill",
        "choral",
        "blues",
        "broadway",
        "christmas",
        "punk",
        "dance",
        "deep",
        "disco",
        "dubstep",
        "grunge",
        "funk",
        "gospel",
        "latin",
        "lo-fi",
        "techno",
        "guitar",
        "soul",
        "jazz",
        "country",
        "piano",
        "drift",
        "sleep",
        "grime",
        "indie",
        "alt",
        "ambient",
        "r&b",
        "folk",
        "background_music",
        "classical",
        "rock",
        "trap",
        "singer-songwriter",
    ]

    df_features = df.copy(deep=True) 

    for genre in high_level_genres:
        df_features[genre] = (
            df_features["artist_genres"]
            .astype(str)
            .str.contains(genre, na=False, regex=True)
            .astype(int)
        )

    df_features = pd.concat(
        [
            df_features,
            pd.get_dummies(df_features["time_signature"], prefix="time_signature"),
        ],
        axis=1,
    )  
    df_features = df_features.drop(
        [
            "song_name",
            "time_signature",
            "time_signature_0", 
            "time_signature_1", 
            "time_signature_3",
            "time_signature_4", 
            "time_signature_5",
            "popularity",
            "album_name",
            "key",
            "album_id",
            "artist_id",
            "artist_genres",
            "artist_name",
            "artist_followers",
            "artist_popularity"
        ],
        axis=1,
    ) 

    df_features = df_features.dropna()
    for col in [
        "duration_ms",
        "explicit",
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "liveness",
        "loudness",
        "mode",
        "speechiness",
        "tempo",
        "valence",
    ]:
        df_features[col] = df_features[col].apply(float)

    df_features = df_features.drop('key_0', axis=1)

    return df_features
#end helper functions from brennerswenson https://github.com/brennerswenson/spotify-recommendations/blob/master/ml/helper_functions.py

def generate_spotipy_recomendations(username, token, sp):
    #top_artist = sp.current_user_top_artist(limit=1)
    #top_track = sp.current_user_top_tracks(limit=1)

    results = {}

    # Get user's saved tracks and extract relevant information
    results, df = get_saved_tracks(username, token, results, sp)

    # Get additional song information (audio features) for the saved tracks
    audio_features, df = get_song_info(results, df, username, token, sp)

    # Get artist information for the saved tracks
    artists_df, df = get_artist_info(df, username, token, sp)

    # Clean the data and prepare it for generating recommendations
    df_features = clean_data(df)

    # Identify user's most listened to artist, genre, and song
    most_listened_artist = df["artist_id"].value_counts().idxmax()
    most_listened_genre = df["artist_genres"].explode().value_counts().idxmax()
    most_listened_song = df["key_0"].value_counts().idxmax()

    # Use most listened artist, genre, and song as seeds for recommendations

    seed_artists = [most_listened_artist]
    seed_genres = [most_listened_genre]
    seed_tracks = [most_listened_song]

    # Retrieve recommended tracks using Spotipy's recommendations endpoint
    recommended_tracks = sp.recommendations(
        seed_artists=seed_artists,
        seed_genres=seed_genres,
        seed_tracks=seed_tracks,
        limit=100  # Get 100 recommended tracks
    )

    # Extract relevant information from recommended tracks into a list
    recommended_tracks_list = []
    for track in recommended_tracks["tracks"]:
        track_info = {
            "song_name": track["name"],
            "artist_name": track["artists"][0]["name"],
            "album_name": track["album"]["name"],
            "release_date": track["album"]["release_date"],
            "popularity": track["popularity"],
            "explicit": track["explicit"],
            "preview_url": track["preview_url"],
            "external_urls": track["external_urls"]["spotify"],
            "duration_ms": track["duration_ms"],  # Include duration_ms
            "type": track["type"],  # Include type
            "uri": track["uri"],  # Include uri
            "id": track["id"]  # Include id
        }
        recommended_tracks_list.append(track_info)

    # Create DataFrame from recommended_tracks_list
    recommended_df = pd.DataFrame(recommended_tracks_list)

    # Add an empty 'analysis_url' column initialized with None
    recommended_df['analysis_url'] = None 
    recommended_df['track_href'] = None

    print(recommended_df)

    # Get additional song information (audio features) for recommended tracks
    audio_features_recommended, recommended_df = get_song_info({}, recommended_df, username, token, sp)

    # Get artist information for recommended tracks
    artists_df_recommended, recommended_df = get_artist_info(recommended_df, username, token, sp)

    # Clean the recommended DataFrame for further analysis
    recommended_df_cleaned = clean_data(recommended_df)

    return recommended_tracks_list, recommended_df_cleaned

def process_saved_tracks(username, token, sp):
    results = {}

    # Get user's saved tracks and extract relevant information
    results, df = get_saved_tracks(username, token, results, sp)

    # Get additional song information (audio features) for the saved tracks
    audio_features, df = get_song_info(results, df, username, token, sp)

    # Get artist information for the saved tracks
    artists_df, df = get_artist_info(df, username, token, sp)

    # Clean the data and prepare it for generating recommendations
    df_features = clean_data(df)

    return df_features

def build_cosine_similarity_model(df_features):
    # Standardize the feature columns for cosine similarity calculation
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_features.drop(columns=["song_name"]))

    # Compute cosine similarity matrix
    cosine_sim_matrix = cosine_similarity(df_scaled, df_scaled)

    return cosine_sim_matrix

def apply_cosine_similarity(cosine_sim_matrix, recommended_df, selected_song_index, num_recommendations=20):
    # Sort indices based on cosine similarity to the selected song
    sim_scores = list(enumerate(cosine_sim_matrix[selected_song_index]))
    sim_scores_sorted = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Extract indices of top similar songs (excluding the selected song itself)
    top_indices = [i[0] for i in sim_scores_sorted[1:num_recommendations+1]]

    # Return filtered DataFrame with top recommended songs
    recommended_filtered = recommended_df.iloc[top_indices]

    return recommended_filtered

def recommend_top_songs(username, token, sp):
    # Generate Spotify recommendations
    recommended_tracks_list, recommended_df_cleaned = generate_spotipy_recomendations(username, token, sp)

    # Process saved tracks to obtain a feature matrix for cosine similarity
    df_features = process_saved_tracks(username, token, sp)

    # Build cosine similarity model from feature matrix
    cosine_sim_matrix = build_cosine_similarity_model(df_features)

    # Select a song index to use as a seed for recommendations (e.g., first song)
    selected_song_index = 0  # Choose the first song from the recommended list

    # Apply cosine similarity to filter down to 20 recommended songs
    recommended_filtered = apply_cosine_similarity(cosine_sim_matrix, recommended_df_cleaned, selected_song_index)

    return recommended_filtered


def recommend_top_songs_and_create_playlist(username, token, sp):
        # Generate Spotify recommendations
    recommended_tracks_list, recommended_df_cleaned = generate_spotipy_recomendations(username, token, sp)

    # Process saved tracks to obtain a feature matrix for cosine similarity
    df_features = process_saved_tracks(username, token, sp)

    # Build cosine similarity model from feature matrix
    cosine_sim_matrix = build_cosine_similarity_model(df_features)

    # Select a song index to use as a seed for recommendations (e.g., first song)
    selected_song_index = 0  # Choose the first song from the recommended list

    # Apply cosine similarity to filter down to 20 recommended songs
    recommended_filtered = apply_cosine_similarity(cosine_sim_matrix, recommended_df_cleaned, selected_song_index)

    # Create a new playlist named "reccos" on the user's Spotify account
    playlist_name = "reccos"
    playlist_description = "Recommended Songs Playlist"

    try:
        # Create the playlist
        playlist = sp.user_playlist_create(username, playlist_name, public=False, description=playlist_description)

        # Extract the playlist ID
        playlist_id = playlist["id"]

        # Add recommended songs to the newly created playlist
        track_ids = recommended_filtered["id"].tolist()[:20]  # Limit to first 20 unique track IDs
        sp.playlist_add_items(playlist_id, track_ids)

        print(f"Playlist '{playlist_name}' created successfully with {len(track_ids)} tracks!")
        print(f"Playlist ID: {playlist_id}")

        return playlist_id

    except spotipy.SpotifyException as e:
        print(f"Error creating playlist: {e}")
        return None