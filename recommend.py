from utils import *
from sklearn.metrics import mean_absolute_error
import pickle


train, test, max_user, max_work, mapping_work = get_data()

pickle.dump(mapping_work, open('mapping_work.pkl', 'wb'))


#######################################################################
model = get_model_1(max_work, max_user)

# model.save("connie_model")

# test_load_model = keras.models.load_model("connie_model")

history = model.fit([get_array(train["anime_uid"]), get_array(train["profile"])], get_array(train["score"]), epochs=10,
                    validation_split=0.2, verbose=0)

# model.save_weights("model_1.h5")

predictions = model.predict([get_array(test["anime_uid"]), get_array(test["profile"])])

test_performance = mean_absolute_error(test["score"], predictions)

print(" Test Mae model 1 : %s " % test_performance)

#######################################################################
model = get_model_2(max_work, max_user)

history = model.fit([get_array(train["anime_uid"]), get_array(train["profile"])], get_array(train["score"]), epochs=10,
                    validation_split=0.2, verbose=0)

predictions = model.predict([get_array(test["anime_uid"]), get_array(test["profile"])])

test_performance = mean_absolute_error(test["score"], predictions)

print(" Test Mae model 2 : %s " % test_performance)

#######################################################################
model = get_model_3(max_work, max_user)

history = model.fit([get_array(train["anime_uid"]), get_array(train["profile"])], get_array(train["score"]), epochs=10,
                    validation_split=0.2, verbose=0)

# model.save("connie_model3")
# model.save("connie_model3.h5")

predictions = model.predict([get_array(test["anime_uid"]), get_array(test["profile"])])

test_performance = mean_absolute_error(test["score"], predictions)

print(" Test Mae model 3 : %s " % test_performance)