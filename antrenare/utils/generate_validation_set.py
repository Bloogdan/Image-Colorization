import os
import shutil
import random

from_path = '../data/train/preprocess/'
to_path = '../data/validation/preprocess/'

training_samples = 14034
files = os.listdir(from_path)
shuffled = list(range(training_samples))
random.shuffle(shuffled)

i = 0
for file_idx in shuffled:
    shutil.move(from_path + files[file_idx], to_path + files[file_idx])
    
    i+=1
    if(i > training_samples // 10):
        break