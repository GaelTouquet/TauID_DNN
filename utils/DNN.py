#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 12:34:56 2018

@author: gtouquet
"""

from keras.models import Model, load_model
from keras.layers import Dense, Input
import tensorflow as tf
import numpy as np

class Dense_DNN(object):
    """Wrapper class for fully connected 'Dense' DNNs
    """
    
    def __init__(self, load=None, 
                 struct=[[6],[100,'tanh'],[50,'tanh'],[1,'sigmoid']],
                 loss='mean_squared_error',optimizer='adam'):
        if load:
            self.name = load
            self.model = load_model(load)
        else:
            self.name = '_'.join(['Dense']+[str(x[0]) for x in struct])
            inputs = Input(shape=(struct.pop(0)[0],))
            first_layer = struct.pop(0)
            x = Dense(first_layer[0], activation=first_layer[1])(inputs)
            for layer in struct:
                x = Dense(layer[0], activation=layer[1])(x)
            self.model = Model(inputs=inputs, outputs=x)
            self.model.compile(loss=loss, optimizer=optimizer)
            
    def train(self, input_train, output_train,
              epochs=1, batch_size=10,
              device='/gpu:0'):
        with tf.device(device):
            self.model.fit(input_train, output_train, 
                           epochs=epochs, batch_size=batch_size)
            self.save(self.name)
        
        
    def save(self, name=None):
        if not name:
            name = self.name
        self.model.save('../DNN_save_files/'+name)
        
    def test(self, input_test, output_test):
        y = self.model.predict(input_test)
        to_save = zip(y,output_test)
        np.save('../outputs/'+self.name+'_output',to_save)
        return y, output_test