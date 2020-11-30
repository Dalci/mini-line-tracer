import numpy as np
import pandas as pd
import cv2
import os

path = os.path.dirname(__file__)
print(path)
i = 1
img = cv2.imread(os.path.join(path, 'sample lane', f'lane{i} 2020-11-25.jpg'), cv2.IMREAD_GRAYSCALE)

#img = np.reshape(img, np.array(16, 16))
resized_img = cv2.resize(img, dsize=(320, 320), interpolation=cv2.INTER_AREA)
cv2.imshow('img', resized_img)
cv2.waitKey(0)
print(resized_img)
