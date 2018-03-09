#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 15:57:29 2018

@author: gtouquet
"""

import numpy as np
from TauID_DNN.utils.ROCcurve import ROCcurve

nn_output = np.load('myfirstmodel_output_test.npy')
wanted_output = np.load('myfirstmodel_output_wanted.npy')

roc = ROCcurve(nn_output,wanted_output, verbose=True)

roc.draw(display=True, standard=True)