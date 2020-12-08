import numpy as np
import tensorflow as tf
from keras.models import load_model
import pickle
import cv2

class DNN_Driver():
    def __init__(self):
        self.model = None

    def load(self):
        self.model = load_model("mlt_model")
		
    def predict_direction(self, img):
        #print(img.shape)
        img = np.array([np.reshape(img,img.shape[0]**2)])
        ret =  self.model.predict(np.array([img]))
        return ret[0][0][0]

dd = DNN_Driver()
dd.load()
with open('test_lane.p', 'rb') as f:
    imgs = pickle.load(f)

for img in imgs:
    cv2.imshow('image', img)
    cv2.waitKey(0)
    print('prediction = ', dd.predict_direction(img))