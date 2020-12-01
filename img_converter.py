import numpy as np
import pickle
import cv2
import os

def convert_img(img):
    # thresholding
    threshold = int(np.mean(img)) * 0.5

    ret, cvtd_img = cv2.threshold(img.astype(np.uint8), threshold, 255, cv2.THRESH_BINARY_INV)

    converted_image = cv2.resize(cvtd_img, (16,16), interpolation=cv2.INTER_AREA)

    return converted_image

if __name__ == '__main__':

    current = os.path.dirname(__file__)
    print(current)

    img_list = os.listdir(os.path.join(current, 'sample lane'))
    #print('file list: ', img_list)

    cvt_list = []

    for img_file in img_list:
        img = cv2.imread(os.path.join(current, 'sample lane', img_file), cv2.IMREAD_GRAYSCALE)

        converted_image = convert_img(img)
        cvt_list.append(np.array(converted_image))
        #cv2.imshow("Converted Image", converted_image)
        #print(type(cvt_list))
        print(f'{img_file} converted.')
        
    with open('test_lane.p', 'wb') as f:   
        pickle.dump(cvt_list, f)

    print('All data saved.')