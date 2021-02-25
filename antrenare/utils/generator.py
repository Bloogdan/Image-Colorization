import random
import numpy as np
from pickle import load
from os import listdir

def data_generator(training_dir, training_samples, batch_size):
    
    current_batch_size=0
    while 1:
        files = listdir(training_dir)
        shuffled = list(range(training_samples))
        random.shuffle(shuffled)
        for file_idx in shuffled:
            
            if current_batch_size == 0:
                X, Y = list(), list()
                
            file_path = training_dir + files[file_idx]
            fid = open(file_path, 'rb')
            file = load(fid)
            img_arr_lab = file['img_arr_lab']
            
            img_arr_lab_ab = np.zeros_like(img_arr_lab[:,:,1:])
            img_arr_lab_ab = img_arr_lab[:,:,1:] / 128
            img_arr_lab_l  = np.zeros_like(img_arr_lab[:,:,0])
            img_arr_lab_l  = img_arr_lab[:,:,0]
            
            img_arr_lab_l_expandD = np.expand_dims(img_arr_lab_l, axis=2)
            
            X.append(img_arr_lab_l_expandD)
            Y.append(img_arr_lab_ab)
            
            current_batch_size += 1
            if current_batch_size == batch_size:
                current_batch_size = 0
                yield [np.array(X), np.array(Y)] 