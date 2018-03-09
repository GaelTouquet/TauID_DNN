#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 05:53:21 2018

@author: gtouquet
"""

from TauID_DNN.utils.DNN import Dense_DNN
from TauID_DNN.utils.ROCcurve import ROCcurve
import numpy as np

###Data preparation

background = np.load('../samples_numpy/QCD_justJet.npy')
signal = np.load('../samples_numpy/GGH500_justJet.npy')

n_signal_train = len(signal)/2
#n_QCD_train = len(background)/2

train = np.concatenate((background[:n_signal_train,:],signal[:n_signal_train,:]))

np.random.shuffle(train)

input_train, output_train = train[:,0:-1], train[:,-1]

test = np.concatenate((background[n_signal_train:len(signal),:],signal[n_signal_train:,:]))

np.random.shuffle(test)

input_test, output_test = test[:,0:-1], test[:,-1]

###


myDNN = Dense_DNN(load='../DNN_save_files/Dense_6_100_50_1_best')


output_dnn, wanted_output = myDNN.test(input_test, output_test)

roc = ROCcurve(output_dnn, wanted_output)
roc.draw(display=True, standard=True)
roc.save(myDNN.name)