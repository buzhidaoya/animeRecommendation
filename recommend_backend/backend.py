from flask import Flask
import pandas as pd
import numpy as np
from tensorflow import keras
from flask import jsonify

from recommend_model.utils import get_model_3, get_array, get_data

app = Flask(__name__)


@app.route('/recommendation/<username>')
def recommendation(username):
    all_anime_uids = pd.read_csv("../../data/ratings.csv")["movieId"]  # ListA
    all_anime_uids_int = []
    for uid in all_anime_uids:
        all_anime_uids_int.append(int(uid))
    
    usernames = []
    i = 0
    while i < len(all_anime_uids_int):
        usernames.append(int(username))
        i = i + 1
    reload_model = keras.models.load_model("../recommend_model/connie_model3")
    ratings = reload_model.predict([get_array(all_anime_uids_int[:100]), get_array(usernames[:100])])
    print(ratings)
    ratings_1d = []
    for rating in ratings:
        ratings_1d.append(str(rating[0]))
    return jsonify(ratings=ratings_1d)
    


@app.route('/')
def hello_world():
    return 'Hello, Connie!'
