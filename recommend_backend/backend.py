from flask import Flask
import pandas as pd
import numpy as np
from tensorflow import keras
from flask import jsonify
from flask_cors import CORS, cross_origin
import requests # 发送http requests
from bs4 import BeautifulSoup   # 解析html
import json

from recommend_model.utils import get_model_3, get_array, get_data

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def Sort_Tuple(tup):   
    # reverse = None (Sorts in Ascending order)  
    # key is set to sort using second element of  
    # sublist lambda has been used  
    return(sorted(tup, key = lambda x: x[1]))

@app.route('/recommendation/<username>', methods=['GET', 'POST'])
@cross_origin()
def recommendation(username):
    all_anime_uids = pd.read_csv("../data/ratings.csv")["movieId"]  
    all_movies = pd.read_csv("../data/movies.csv")  
    all_links = pd.read_csv("../data/links.csv", dtype=str)
    all_links["movieId"] = pd.to_numeric(all_links["movieId"])
    # print(all_anime_uids)
    print(all_anime_uids.shape)
    all_anime_uids_int = [] # ListA
    for uid in all_anime_uids:
        all_anime_uids_int.append(int(uid))
    
    usernames = []  # Expand the username into len(all_anime_uids_int)
    i = 0
    while i < len(all_anime_uids_int):
        usernames.append(int(username))
        i = i + 1
    # print("--------------------- usernames: -------------------------")
    # print(usernames)
    # print(len(usernames))
    size = 100
    reload_model = keras.models.load_model("../recommend_model/connie_newmodel")

    df = pd.read_csv("../data/ratings.csv")
    movie_df = pd.read_csv("../data/movies.csv")

    user_ids = df["userId"].unique().tolist()
    user2user_encoded = {x: i for i, x in enumerate(user_ids)}
    userencoded2user = {i: x for i, x in enumerate(user_ids)}
    movie_ids = df["movieId"].unique().tolist()
    movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}
    movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}
    df["user"] = df["userId"].map(user2user_encoded)
    df["movie"] = df["movieId"].map(movie2movie_encoded)

    # Let us get a user and see the top recommendations.
    user_id = df.userId.sample(1).iloc[0]
    # user_id = username
    movies_watched_by_user = df[df.userId == user_id]
    movies_not_watched = movie_df[
        ~movie_df["movieId"].isin(movies_watched_by_user.movieId.values)
    ]["movieId"]
    movies_not_watched = list(
        set(movies_not_watched).intersection(set(movie2movie_encoded.keys()))
    )
    movies_not_watched = [[movie2movie_encoded.get(x)] for x in movies_not_watched]
    user_encoder = user2user_encoded.get(user_id)
    user_movie_array = np.hstack(
        ([[user_encoder]] * len(movies_not_watched), movies_not_watched)
    )
    ratings = reload_model.predict(user_movie_array).flatten()
    top_ratings_indices = ratings.argsort()[-10:][::-1]
    recommended_movie_ids = [
        movie_encoded2movie.get(movies_not_watched[x][0]) for x in top_ratings_indices
    ]

    print("Showing recommendations for user: {}".format(user_id))
    print("====" * 9)
    print("Movies with high ratings from user")
    print("----" * 8)
    top_movies_user = (
        movies_watched_by_user.sort_values(by="rating", ascending=False)
        .head(5)
        .movieId.values
    )
    movie_df_rows = movie_df[movie_df["movieId"].isin(top_movies_user)]
    for row in movie_df_rows.itertuples():
        print(row.title, ":", row.genres)

    print("----" * 8)
    print("Top 10 movie recommendations")
    print("----" * 8)
    recommended_movies = movie_df[movie_df["movieId"].isin(recommended_movie_ids)]
    for row in recommended_movies.itertuples():
        print(row.title, ":", row.genres)
    
    return jsonify(recommended_movies)

    # ratings = reload_model.predict([get_array(all_anime_uids_int[:size]), get_array(usernames[:size])])
    # # print(ratings)
    # ratings_1d = []
    # for rating in ratings:
    #     ratings_1d.append(str(rating[0]))
    # # create a map <movieId, rating>
    # movieId_rating = []
    # i = 0
    # while i < len(ratings_1d):
    #     movieId_rating.append((all_anime_uids_int[i], ratings_1d[i]))
    #     i = i + 1
    # movieId_rating = Sort_Tuple(movieId_rating)

    # movieId_top10 = []
    # i = 0
    # while i < 10:
    #     movieId_top10.append(movieId_rating[i][0])
    #     i = i + 1
    # i = 0
    # movieIdName_top10 = {}
    # while i < 10:
    #     movieId = movieId_top10[i]
    #     movie_name = all_movies.loc[all_movies['movieId'] == movieId].drop_duplicates(subset = ['movieId'])['title'].values[0]
    #     imdbId = all_links.loc[all_links['movieId'] == movieId].drop_duplicates(subset = ['movieId'])['imdbId'].values[0]
    #     url = "https://www.imdb.com/title/tt" + str(imdbId)
    #     page = requests.get(url)
    #     # print(page.content)
    #     s = BeautifulSoup(page.content, "html.parser")
    #     p = s.find_all("div", class_="poster")
    #     # print(p)
    #     img = p[0].find_all("img")
    #     movieIdName_top10[i] = [movieId, movie_name, url + " ", img[0]["src"] + " "]
    #     i = i + 1
    # print(jsonify(movieIds=movieIdName_top10))
    # print(json.dumps({"movieIds":movieIdName_top10}))
    # # return json.dumps({"movieIds":movieIdName_top10})
    # return jsonify(movieIds=movieIdName_top10)


@app.route('/')
def hello_world():
    return 'Hello, Connie!'
