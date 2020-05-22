#==============================================================================
## Plot and trim population count 
#==============================================================================
# Uses modules:
from netCDF4 import Dataset
from matplotlib import pyplot as plt
##import cartopy
##import cartopy.crs as ccrs
##import cartopy.feature as cfeature
import numpy as np
##import Country_mask
##import pandas as pd
##from geopy.distance import distance
import numpy.ma as ma
from global_land_mask import globe
#==============================================================================

def get_background_stats():
    # Get an area in the middle of the Pacific Ocean to use as very clean background
    fname = '/Users/dfinch/Documents/S5P_OFFL_L2__NO2____20191222T223925_20191223T002055_11358_01_010302_20191224T152624.nc'
    dataset = Dataset(fname)
    products = dataset.groups['PRODUCT']
    no2 = products.variables['nitrogendioxide_tropospheric_column']
    clean_no2_subset = no2[0,2400:2500,:] 
    mean = np.mean(clean_no2_subset)
    std = np.std(clean_no2_subset)
    dataset.close()
    return mean,std

clean_mean, clean_std = get_background_stats()


fname = '/Users/dfinch/Documents/S5P_OFFL_L2__NO2____20181101T155632_20181101T173802_05452_01_010200_20181107T173227.nc'
dataset = Dataset(fname)
products = dataset.groups['PRODUCT']
no2 = products.variables['nitrogendioxide_tropospheric_column'][0]
lat = products.variables['latitude'][0]
lon = products.variables['longitude'][0]
qa = products.variables['qa_value'][0]

qa_limit = 0.5 # 0.5 for cloudy scenes. 0.75 for cloud free

no2_data = no2.filled(np.nan)
no2_data[qa < qa_limit] = np.nan

##land_mask = globe.is_land(lat,lon)
##no2_data[~land_mask] = np.nan

high_no2 = no2_data - (clean_mean + clean_std)
high_no2[high_no2 <= 0] = np.nan

x_res = 75 # pixels - will make 6 boxes across swath
y_res = 59 # - will make 55 boxes down swath

for x in range(0,450,x_res):
    for y in range(118,3127,y_res): # Trim off the ends of the swatch since these will be messed up by the poles anyway
        data_subset = no2_data[y:y+y_res,x:x_res]
        land_mask = globe.is_land(lat[y:y+y_res,x:x_res],lon[y:y+y_res,x:x_res])
        if land_mask.sum() < 10:
            print(land_mask.sum())
            continue
        if np.count_nonzero(~np.isnan(data_subset)) < 200:
                continue
        plt.pcolormesh(lon[y:y+y_res,x:x+x_res],lat[y:y+y_res,x:x+x_res],data_subset)
        plt.savefig('/Users/dfinch/Desktop/temp.png')
        plt.close()
        while True:
            answer = input('Y or N?')
            if answer.lower() in ['n','no','']:
                action = 'disguarding'
                break
            elif answer.lower() in ['y','yes']:
                action = 'keeping'
                break
            else:
                answer = True
        print(action)
        
## ============================================================================
## END OF PROGAM
## ============================================================================
