from skimage.color import rgb2lab, rgb2gray, gray2rgb
from keras.preprocessing.image import img_to_array, load_img
from keras.applications import vgg16
from keras.models import Sequential

from os import listdir
from pickle import dump

import numpy as np

raw_path = '../data/train/image/'
preprocess_path = '../data/train/preprocess/'

def is_grey_scale(og_img):
    img = og_img.convert('RGB')
    w,h = img.size
    for i in range(w):
        for j in range(h):
            r,g,b = img.getpixel((i,j))
            if r != g != b: return False
    return True

progress = 0
for file in listdir(raw_path):
    img_path = raw_path + file
    img = load_img(img_path, target_size=(150, 150)) 
	if is_grey_scale(img) == True:
		continue
    
    img_arr_rgb = img_to_array(img) 
    img_arr_lab = rgb2lab(img_arr_rgb / 255)
    
    data=dict()
    data['img_arr_lab'] = img_arr_lab
    file_save_name = preprocess_path + file.split('.')[0] +'preproc.pk'
    
    fid = open(file_save_name, 'wb')
    dump(data, fid)
    fid.close()
    
    progress += 1
    if progress % 100 ==0:
        print(file)

