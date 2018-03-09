from TauID_DNN.utils.DNN import Dense_DNN
from TauID_DNN.utils.ROCcurve import ROCcurve
import numpy as np

###Data preparation

background = np.load('../samples_numpy/QCD.npy')
signal = np.load('../samples_numpy/GGH500.npy')

n_signal_train = len(signal)/2
#n_QCD_train = len(background)/2

train = np.concatenate((background[:n_signal_train,:],signal[:n_signal_train,:]))

np.random.shuffle(train)

input_train, output_train = train[:,0:-1], train[:,-1]

test = np.concatenate((background[n_signal_train:len(signal),:],signal[n_signal_train:,:]))

np.random.shuffle(test)

input_test, output_test = test[:,0:-1], test[:,-1]

###

myDNN = Dense_DNN(struct=[[1601],[5000,'tanh'],[5000,'tanh'],[5000,'tanh'],[1,'sigmoid']])

myDNN.train(input_train, output_train, epochs=350, batch_size=10, device='/gpu:1')

output_dnn, wanted_output = myDNN.test(input_test, output_test)

roc = ROCcurve(output_dnn, wanted_output)
roc.draw(display=False, standard=True)
roc.save(myDNN.name)