import tensorflow as tf
from keras.models import load_model

from utils.generator import data_generator
from model.model import define_model

import numpy as np

# model = define_model(150, 150)
model = load_model('./data/models/model3_13.h5')

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    # Restrict TensorFlow to only use the first GPU
    try:
        training_dir = './data/train/preprocess/'
        training_samples = 14034  # 17541 6000
        
        validation_dir = './data/validation/preprocess/'
        validation_samples = 3000 # 1950 400
        
        batch_size = 8
        
        epochs = 1000
        steps_per_epoch = np.floor(training_samples / batch_size)
        validation_steps = np.floor(validation_samples / batch_size)
        
        for i in range(epochs):
            train_generator = data_generator(training_dir, training_samples, batch_size)
            validation_generator = data_generator(validation_dir, validation_samples, batch_size)
            
            fit_history = model.fit_generator(train_generator, validation_data=validation_generator, validation_steps=validation_steps, epochs=1, steps_per_epoch=steps_per_epoch, verbose=1)
            model.save('./data/models/model4_' + str(i) + '.h5')
        
    except RuntimeError as e:
        # Visible devices must be set before GPUs have been initialized
        print(e)