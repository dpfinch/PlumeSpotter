#==============================================================================
## Make Images from plumes
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

for n,plume in enumerate(plume_tiles):
    plt.figure(figsize = (2,2))
    plt.imshow(plume)
    plt.axis('off')
    plt.tight_layout(pad = 0)
    plt.savefig('/Users/dfinch/Python/Plume_Detection/assets/Plume_images/plume_{}.png'.format(str(n).zfill(4)))
    plt.close()
