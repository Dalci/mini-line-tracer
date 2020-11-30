import pickle
import cv2
import numpy as np

with open('list.p', 'rb') as f:
    imgs = pickle.load(f)

for row in imgs[:7]:
    img = row[1]

    img = img.reshape((16,16) ,order='C')

    print(img)

    res = cv2.resize(img, dsize=(320, 320), interpolation=cv2.INTER_LINEAR)
    cv2.imshow('image', res)
    
    cv2.waitKey(0)