from keras.models import load_model

from skimage.color import lab2rgb
from PIL import Image

import numpy as np
import pickle

class Predictor(object):
    def __init__(self, model, preprocessor):
        self._preprocessor = preprocessor
        self._model = model

    def predict(self, image_path):
		l = self._preprocessor.preprocess(image_path)
		
        ab = self._model.predict(l)
        ab *= 128
        
        l = np.squeeze(l, axis = 3)
        result = np.zeros((self.size, self.size, 3))
        result[:,:,0] = l
        result[:,:,1:] = ab
        result = lab2rgb(result)
        
        return result.tolist()
		
		@classmethod
    def from_path(cls, model_dir):
        model_path = os.path.join(model_dir, 'model4_94.h5')
        model = load_model(model_path)

        preprocessor_path = os.path.join(model_dir, 'preprocessor.pkl')
        with open(preprocessor_path, 'rb') as f:
            preprocessor = pickle.load(f)

        return cls(model, preprocessor)
    