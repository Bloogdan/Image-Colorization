from keras.models import Model
from keras.layers import Conv2D, UpSampling2D, Input
from keras.layers.normalization import BatchNormalization

import numpy as np

def define_model(height, width):
    #Encoder
    encoder_input = Input(shape=(height, width, 1,))
    encoder_output = Conv2D(64, (3,3), activation='relu', padding='same', strides=2)(encoder_input)
    encoder_output = BatchNormalization()(encoder_output)
    
    encoder_output = Conv2D(128, (3,3), activation='relu', padding='same')(encoder_output)
    encoder_output = BatchNormalization()(encoder_output)
    
    encoder_output = Conv2D(256, (3,3), activation='relu', padding='same')(encoder_output)
    encoder_output = BatchNormalization()(encoder_output)
    
    encoder_output = Conv2D(256, (3,3), activation='relu', padding='same', strides=2)(encoder_output)
    encoder_output = BatchNormalization()(encoder_output)
    
    encoder_output = Conv2D(512, (3,3), activation='relu', padding='same')(encoder_output)
    encoder_output = BatchNormalization()(encoder_output)
    
    encoder_output = Conv2D(512, (3,3), activation='relu', padding='same')(encoder_output)
    encoder_output = BatchNormalization()(encoder_output)
    
    encoder_output = Conv2D(256, (3,3), activation='relu', padding='same')(encoder_output)
    encoder_output = BatchNormalization()(encoder_output)
    
    decoder_output = Conv2D(128, (3,3), activation='relu', padding='same')(encoder_output)
    decoder_output = BatchNormalization()(decoder_output)
	
	#Decoder
    decoder_output = UpSampling2D((2, 2))(decoder_output)
    decoder_output = Conv2D(64, (3,3), activation='relu', padding='same')(decoder_output)
    decoder_output = BatchNormalization()(decoder_output)
	
    decoder_output = UpSampling2D((2, 2))(decoder_output)
    decoder_output = Conv2D(32, (3,3), activation='relu', padding='same')(decoder_output)
    decoder_output = BatchNormalization()(decoder_output)
    
    decoder_output = Conv2D(16, (3,3), activation='relu', padding='same')(decoder_output)
    decoder_output = BatchNormalization()(decoder_output)
    
    decoder_output = Conv2D(2, (3, 3), activation='tanh')(decoder_output)
    decoder_output = BatchNormalization()(decoder_output)
    
    model = Model(inputs=encoder_input, outputs=decoder_output)
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['acc'])
    
    return model