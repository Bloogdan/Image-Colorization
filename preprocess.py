from skimage.color import rgb2lab
from PIL import Image

import numpy as np

class Preprocessor(object):

    def __init__(self):

    def preprocess(self, data):
        im = Image.open(data)
        old_size = im.size
           
        ratio = float(self.size) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        im = im.resize(new_size, Image.ANTIALIAS)
           
        new_im = Image.new("RGB", (self.size, self.size))
        new_im.paste(im, ((self.size - new_size[0]) // 2, (self.size - new_size[1]) // 2))
        
        im_arr = np.array(new_im, dtype="float")
        im_arr *= 1.0 / 255
        print(im_arr.shape)
        
        lab = rgb2lab(im_arr)
        l = lab[:,:,0]
        l = np.expand_dims(l, axis = 0)
        l = np.expand_dims(l, axis = 3)  
		
        return l