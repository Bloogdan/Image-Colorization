from keras.models import Sequential, load_model
from keras.applications import vgg16

from skimage.color import rgb2lab, lab2rgb, gray2rgb, rgb2gray
from skimage.io import imsave
from PIL import Image

import numpy as np

class Predictor(object):
    def __init__(self, model_path, size):
        self.size = size
        self.model = load_model(model_path)

    def predict(self, image_path):
        
        im = Image.open(image_path)
        old_size = im.size
           
        ratio = float(self.size) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        im = im.resize(new_size, Image.ANTIALIAS)
           
        new_im = Image.new("RGB", (self.size, self.size))
        new_im.paste(im, ((self.size - new_size[0]) // 2, (self.size - new_size[1]) // 2))
           
        im_arr = np.array(new_im, dtype="float")
        im_arr *= 1.0 / 255
           
        lab = rgb2lab(im_arr)
        l = lab[:,:,0]
        l = np.expand_dims(l, axis = 0)
        l = np.expand_dims(l, axis = 3)    
               
        ab = self.model.predict(l)
        ab *= 128
           
        l = np.squeeze(l, axis = 3)
        result = np.zeros((self.size, self.size, 3))
        result[:,:,0] = l
        result[:,:,1:] = ab
        result = lab2rgb(result)
        # imsave('./data/results/image_2/model4_15_' + str(idx) + '.png', result)
        
        return np.array(result)
    