from keras.models import Sequential
from keras.layers import Dense

import numpy as np
import tensorflow as tf
import cv2

outputs = 1

from get_image import *

trX,trY = get_training_data()
teX = get_test_data()

seed = 0
np.random.seed(seed)
tf.random.set_seed(seed)

model=Sequential()
model.add(Dense(512, input_dim=np.shape(trX)[1], activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam')

model.fit(trX, trY, epochs=30, batch_size=1)

Y_prediction = model.predict(teX).flatten()

for i in range(100):
    #label = teY[i]
    #cv2.imshow() 
    pred = Y_prediction[i]
    print("pred:{:.2f}".format(float(pred)))


def get_direction(img):
    print(img.shape)

    ret =  model.predict(img)
    return ret

# Predict direction with single image
print('shape: ', teX[10].shape)
dir=get_direction(np.array([teX[10]]))          # single 이미지를 위해서는 한 번 둘러싸야됨.

print(dir[0][0])

cv2.imshow('predicted image', np.reshape(teX[10], (16,16)))
cv2.waitKey(0)

#model.save("mlt_model")