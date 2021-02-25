import tensorflow as tf
from keras.models import load_model

model = load_model('./data/models/model4_45.h5')

tf.saved_model.save(model, './model/')