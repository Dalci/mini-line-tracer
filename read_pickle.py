import pickle
import cv2
import numpy as np

with open('test_lane.p', 'rb') as f:
    imgs = pickle.load(f)

for img in imgs:
    #img = img.reshape((16,16) ,order='C')

    print(img)

    res = cv2.resize(img, dsize=(320, 320), interpolation=cv2.INTER_LINEAR)
    cv2.imshow('image', res)
    
    cv2.waitKey(0)