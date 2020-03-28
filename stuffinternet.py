# first neural network with keras tutorial
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense

dataset = loadtxt('ignore/Unspec List2.csv', delimiter=',')
# split into input (X) and output (y) variables
X = dataset[:,0:9]
y = dataset[:,9]


model = Sequential()
model.add(Dense(12, input_dim=9, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
