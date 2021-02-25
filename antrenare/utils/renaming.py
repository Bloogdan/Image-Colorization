from os import rename, listdir
from shutil import move

frompath = '../data/validation/buildings/'
topath = '../data/validation/'

i = 0
for file in listdir(frompath):
    new_name = 'buildings' + file
    
    rename(frompath + file, frompath + new_name)
    move(frompath + new_name, topath)