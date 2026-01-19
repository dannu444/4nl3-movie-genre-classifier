import pandas as pd
import requests
import time
import os

tmdb_api_key = "a8ebfa44b6e96530303358f42c0c8287" 
data_dir = "./data"

#load data
number_of_rows = 1000
df_movies = pd.read_csv(f"{data_dir}/ml-20m/movies.csv", nrows=number_of_rows)
df_links = pd.read_csv(f"{data_dir}/ml-20m/links.csv", nrows=number_of_rows)

df_combined = pd.merge(df_movies, df_links, on='movieId')
df_combined['plot'] = None
print(f"Combined dataframe shape: {df_combined.shape}")

def fetch_movie_data(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    params = {"api_key": tmdb_api_key}
    try:
        print(f"Fetching data for TMDb ID: {tmdb_id}")
        response = requests.get(url, params=params)
        response.raise_for_status() # verify if successful response
        data = response.json()
        plot = data.get("overview", "")
        return plot
    except requests.RequestException as e:
        print(f"Error fetching TMDb ID {tmdb_id}: {e}")
        pass
   

# fetch plots and adjust genres to only one genre
for index, row in df_combined.iterrows():
    tmdb_id = row['tmdbId']
    plot = fetch_movie_data(tmdb_id) # fetch movie plot 
    if plot:
        df_combined.at[index, 'plot'] = plot
    df_combined.at[index, 'genres'] = row['genres'].split('|')[0]  # adjust to keep only first genre
    time.sleep(0.25)  # for TMDb rate limit

# drop rows with missing plots and remove unnecessary columns
df_combined.dropna(subset=['plot'], inplace=True)
df_combined = df_combined[['title', 'genres', 'plot']]
print(f"Dataframe shape after fetching plots and cleaning: {df_combined.shape}")

# convert table to csv
df_combined.rename(columns={'genres': 'genre'}, inplace=True)
df_combined.to_csv(f"{data_dir}/output.csv", index=False)