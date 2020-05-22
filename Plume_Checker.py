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

keep_index = []
conf_index = []

for n,plume in enumerate(plume_tiles):
    plt.imshow(plume)
    plt.savefig('/Users/dfinch/Desktop/plume_test.png')
    plt.close()

    answer = input('Keep?')
    if answer in ['y','']:
        keep_index.append(n)
        print(len(keep_index))
    elif answer == 'c':
        conf_index.append(n)
    else:
        continue
        
