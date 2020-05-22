#==============================================================================
## Plot and trim population count 
#==============================================================================
# Uses modules:
from netCDF4 import Dataset
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import h5py
import random
#==============================================================================

plume_filename = '/Users/dfinch/Documents/NO2_Plumes/NO2_Plumes.h5'
plume_openfile = h5py.File(plume_filename,'r')
plume_tiles = plume_openfile['NO2 Plumes']

good_plume_index = np.loadtxt('/Users/dfinch/Documents/NO2_Plumes/keep_index.csv', dtype = int)
bad_plume_index = np.loadtxt('/Users/dfinch/Documents/NO2_Plumes/conf_index.csv', dtype = int)
bonus_bad_plumes = plume_tiles[bad_plume_index,:,:]

plume_tiles = plume_tiles[good_plume_index,:,:]
rand_ind = random.sample(range(plume_tiles.shape[0]),500)
rand_ind.sort()
plume_subset = plume_tiles[rand_ind,:,:]


no_plume_filename ='/Users/dfinch/Documents/NO2_Plumes/No_Plumes.h5'
no_plume_openfile = h5py.File(no_plume_filename,'r')
no_plume_tiles = no_plume_openfile['NO2 Plumes']
no_plume_tiles = np.concatenate((no_plume_tiles,bonus_bad_plumes),axis = 0)
rand_ind = random.sample(range(no_plume_tiles.shape[0]),500)
rand_ind.sort()
no_plume_subset = no_plume_tiles[rand_ind,:,:]

all_tiles = np.concatenate((plume_subset,no_plume_subset),axis = 0)
labels = np.concatenate(([True]*500,[False]*500))

combo = list(zip(all_tiles,labels))
random.shuffle(combo)

tiles, labs = zip(*combo)
tiles = np.asarray(tiles)

hf = h5py.File('/Users/dfinch/Documents/NO2_Plumes/NO2_Plumes_Training.h5', 'w')
hf.create_dataset('NO2 Plumes Training Data', data=tiles)
hf.close()

np.savetxt('/Users/dfinch/Documents/NO2_Plumes/NO2_Plume_Training_Labels.csv',labs,fmt = '%i')
