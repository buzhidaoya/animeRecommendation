import pandas as pd
import numpy as np
from keras.models import Sequential, Model
from keras.layers import Embedding, Reshape, Activation, Input, Dense, Flatten, Dropout
from keras.layers.merge import Dot, multiply, concatenate
from keras.utils import np_utils
from keras.utils.data_utils import get_file
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import skipgrams
from collections import defaultdict


def get_mapping(series):
    occurrences = defaultdict(int)
    for element in series:
        occurrences[element] += 1   # <unique items in series, 该item出现的次数>
    mapping = {}    # 给occurences里的那些keys做个编号
    i = 0
    for element in occurrences:
        i += 1
        mapping[element] = i    # 这里的element就是occurences里的key，即unique items in series
        # print("-------------------- element in mapping --------------------------")
        # print(element)

    return mapping  # 给series里的unique items编个号：<unique item : 编号>


def get_data():
    data = pd.read_csv("../anime_data/reviews.csv")

    mapping_work = get_mapping(data["anime_uid"])
    # print("*************** mapping_work *******************")
    # print(mapping_work)

    data["anime_uid"] = data["anime_uid"].map(mapping_work)
    # print("*************** data[anime_uid] *****************")
    # print(data["anime_uid"])

    mapping_users = get_mapping(data["profile"])
    # print("*************** mapping_users *******************")
    # print(mapping_users)

    data["profile"] = data["profile"].map(mapping_users)
    # print("*************** data[profile] *****************")
    # print(data["profile"])

    percentile_80 = np.percentile(data["uid"], 80)

    print(percentile_80)

    print(np.mean(data["uid"] < percentile_80))

    print(np.mean(data["uid"] > percentile_80))

    cols = ["profile", "anime_uid", "score"]

    train = data[data.uid < percentile_80][cols]

    print(train.shape)

    test = data[data.uid >= percentile_80][cols]

    print(test.shape)

    max_user = max(data["profile"].tolist())
    max_work = max(data["anime_uid"].tolist())

    return train, test, max_user, max_work, mapping_work


def get_model_1(max_work, max_user):
    dim_embeddings = 30
    bias = 3
    # inputs
    w_inputs = Input(shape=(1,), dtype='int32')
    w = Embedding(max_work + 1, dim_embeddings, name="work")(w_inputs)

    # context
    u_inputs = Input(shape=(1,), dtype='int32')
    u = Embedding(max_user + 1, dim_embeddings, name="user")(u_inputs)
    o = multiply([w, u])
    o = Dropout(0.5)(o)
    o = Flatten()(o)
    o = Dense(1)(o)

    rec_model = Model(inputs=[w_inputs, u_inputs], outputs=o)
    # rec_model.summary()
    rec_model.compile(loss='mae', optimizer='adam', metrics=["mae"])

    return rec_model


def get_model_2(max_work, max_user):
    dim_embeddings = 30
    bias = 9
    # inputs
    w_inputs = Input(shape=(1,), dtype='int32')
    w = Embedding(max_work + 1, dim_embeddings, name="work")(w_inputs)
    w_bis = Embedding(max_work + 1, bias, name="workbias")(w_inputs)

    # context
    u_inputs = Input(shape=(1,), dtype='int32')
    u = Embedding(max_user + 1, dim_embeddings, name="user")(u_inputs)
    u_bis = Embedding(max_user + 1, bias, name="userbias")(u_inputs)
    o = multiply([w, u])
    o = concatenate([o, u_bis, w_bis])
    o = Dropout(0.5)(o)
    o = Flatten()(o)
    o = Dense(1)(o)

    rec_model = Model(inputs=[w_inputs, u_inputs], outputs=o)
    # rec_model.summary()
    rec_model.compile(loss='mae', optimizer='adam', metrics=["mae"])

    return rec_model


def get_model_3(max_work, max_user):
    dim_embeddings = 30
    bias = 9
    # inputs
    w_inputs = Input(shape=(1,), dtype='int32')
    w = Embedding(max_work + 1, dim_embeddings, name="work")(w_inputs)
    w_bis = Embedding(max_work + 1, bias, name="workbias")(w_inputs)

    # context
    u_inputs = Input(shape=(1,), dtype='int32')  # 输入层
    u = Embedding(max_user + 1, dim_embeddings, name="user")(u_inputs)
    u_bis = Embedding(max_user + 1, bias, name="userbias")(u_inputs)
    o = multiply([w, u])
    o = Dropout(0.5)(o)
    o = concatenate([o, u_bis, w_bis])
    o = Flatten()(o)
    o = Dense(16, activation="relu")(o)
    o = Dense(1)(o)

    rec_model = Model(inputs=[w_inputs, u_inputs], outputs=o)
    rec_model.summary()
    rec_model.compile(loss='mae', optimizer='adam', metrics=["mae"])

    return rec_model


def get_array(series):
    return np.array([[element] for element in series])
