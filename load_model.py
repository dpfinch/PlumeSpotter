
# Author: Tianran Zhang
# Contact: tianran.zhang@kcl.ac.uk 
# Date: 2019-05-12 21:12:46
# Last Modified by:  Doug Finch
# Last Modified time: 2020-05-218 14:27

                                  #########       
                                 ##       ###     
                        #########      ######     
                    ####             ##           
                  ###                 ##          
               ###              ########          
            ####    #######    ##                 
       #####   #####     ##  ###                  
       ########          ########   


from __future__ import absolute_import, division, print_function
import os
import sys
import h5py
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

print ("tensorflow version" + tf.__version__)
tf.random.set_seed(42)

image_size  = 28
image_layer = 1
input_size  = image_size**2*image_layer
output_size = 2

def create_model():
    K = 4
    L = 8
    M = 12
    N = 200
    model = tf.keras.models.Sequential()
    model.add(keras.layers.Conv2D(K,(5,5),strides=[1,1], padding="same", activation=tf.keras.activations.relu,input_shape=(image_size,image_size,image_layer,)))
   #  model.add(keras.layers.MaxPooling2D((2,2)))
    model.add(keras.layers.Conv2D(L,(5,5),strides=[2,2], padding="same", activation=tf.keras.activations.relu))
   #  model.add(keras.layers.MaxPooling2D((2,2)))
    model.add(keras.layers.Conv2D(M,(4,4),strides=[2,2], padding="same", activation=tf.keras.activations.relu))
   #  model.add(keras.layers.MaxPooling2D((2,2)))
    model.add(keras.layers.Dense(N, activation=tf.keras.activations.relu))
    model.add(keras.layers.Flatten())

    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(output_size, activation=tf.keras.activations.softmax))
  
    model.compile(optimizer=tf.keras.optimizers.Adam(),loss=tf.keras.losses.sparse_categorical_crossentropy,metrics=['accuracy'])
    return model

def load_test_data(dir_data):
    h5 = h5py.File(os.path.join(dir_data,"NO2_Plumes_Training.h5"),'r')
    train_data   = h5['NO2 Plumes Training Data'][:]
    h5.close()
    train_size   = train_data.shape[0]
    train_labels = pd.read_csv(os.path.join(dir_data,"NO2_Plume_Training_Labels.csv"))['labels'].values
    train_data = np.nan_to_num(train_data)
    train_data = train_data/np.max(train_data)
    train_data = train_data.reshape(-1,image_size,image_size,image_layer)
    test_index_list = pd.read_csv(os.path.join(dir_data,"eval_list.csv"))['index'].values
    return (train_data[test_index_list,:,:,:],train_labels[test_index_list])

def load_model(weightsPath):
    model = create_model()
    model.load_weights(weightsPath)
    return model

def create_plot(pind,inputarr,y,ypre):
    dir_figure = '/home/dfinch/Datastore/plume_finder/pre_figs/'
    fig = plt.figure()
    plt.imshow(inputarr)
    fig.savefig(os.path.join(dir_figure,"ind%04d_value%d_pre%3.2f.png"%(pind,y,ypre[1])))
    plt.close()
    return


if __name__=="__main__":
    dir_data = '/Users/dfinch/DataSync/Plume_Spotting/'
    weightsPath  = os.path.join(dir_data,"model.h5")
    model = load_model(weightsPath)
    
    test_data,test_labels = load_test_data(dir_data)
    loss, acc = model.evaluate(test_data,test_labels)
    print("Restored model, accuracy: {:5.2f}%".format(100*acc))
    
    ypre_list = model.predict(test_data)
    test_index_list = pd.read_csv(os.path.join(dir_data,"eval_list.csv"))['index'].values
##    Nlen = len(ypre_list)
##    for i in np.arange(Nlen):
##        inputarr = test_data[i,:,:,0]
##        y        = test_labels[i]
##        ypre     = ypre_list[i]
##        pind     = test_index_list[i]
##        create_plot(pind,inputarr,y,ypre)


