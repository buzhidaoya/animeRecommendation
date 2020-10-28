from flask import Flask
import pandas as pd
import numpy as np
from tensorflow import keras
from flask import jsonify

from recommend_model.utils import get_model_3, get_array, get_data

app = Flask(__name__)

def Sort_Tuple(tup):   
    # reverse = None (Sorts in Ascending order)  
    # key is set to sort using second element of  
    # sublist lambda has been used  
    return(sorted(tup, key = lambda x: x[1]))

@app.route('/recommendation/<username>')
def recommendation(username):
    all_anime_uids = pd.read_csv("../data/ratings.csv")["movieId"]  
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
    reload_model = keras.models.load_model("../recommend_model/connie_model3")
    ratings = reload_model.predict([get_array(all_anime_uids_int[:size]), get_array(usernames[:size])])
    # print(ratings)
    ratings_1d = []
    for rating in ratings:
        ratings_1d.append(str(rating[0]))
    # create a map <movieId, rating>
    movieId_rating = []
    i = 0
    while i < len(ratings_1d):
        movieId_rating.append((all_anime_uids_int[i], ratings_1d[i]))
        i = i + 1
    movieId_rating = Sort_Tuple(movieId_rating)

    movieId_top10 = []
    i = 0
    while i < 10:
        movieId_top10.append(movieId_rating[i][0])
        i = i + 1
    return jsonify(movieIds=movieId_top10)
    


@app.route('/')
def hello_world():
    return 'Hello, Connie!'
