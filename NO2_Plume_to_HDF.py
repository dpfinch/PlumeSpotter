#==============================================================================
## Plot and trim population count 
#==============================================================================
# Uses modules:
from netCDF4 import Dataset
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import h5py
#==============================================================================

input_file = '/home/dfinch/NO2_TROPOMI_PLUMES/Multiple/Multi_Plume_Box_Coords.csv'
coords_df = pd.read_csv(input_file,index_col ='Unnamed: 0')

file_dir = '/geos/d21/sat_data/TROPOMI/NO2/'

filegroups = coords_df.groupby('filename')

tile_array = np.zeros([len(coords_df),28,28])

array_index = 0

for name, group in filegroups:
    year = name.split('____')[1][:4]
    month = name.split('____')[1][4:6]
    
    full_filename = '{}/{}/{}/{}'.format(file_dir,year, month,name)
    dataset = Dataset(full_filename)
    products = dataset.groups['PRODUCT']
    no2 = products.variables['nitrogendioxide_tropospheric_column'][0]

    for index in group.index:
        tile = group.loc[index]
        no2_plume = no2[tile['Lon imin']:tile['lon imax'],tile['Lat imin']:tile['Lat imax']]
        tile_array[array_index,:,:] = no2_plume
        array_index += 1

hf = h5py.File('/home/dfinch/NO2_TROPOMI_PLUMES/NO2_Plumes.h5', 'w')
hf.create_dataset('NO2 Plumes', data=tile_array)
hf.close()
