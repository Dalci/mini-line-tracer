import numpy as np
import pickle
import cv2
import os

def convert_img(img):
    # thresholding
    img = np.reshape(img, (16,16))
    threshold = int(np.mean(img)) * 0.5

    ret, cvtd_img = cv2.threshold(img.astype(np.uint8), threshold, 255, cv2.THRESH_BINARY)

    #print(cvtd_img)
    return cvtd_img
    #converted_image = cv2.resize(cvtd_img, (16,16), interpolation=cv2.INTER_AREA)

    #return converted_image

if __name__ == '__main__':

    #current = os.path.dirname(__file__)
    #print(current)

    img_list = list()

    #with open(os.path.join(current,'list_empty.p'), 'rb') as f:
    with open('lane2.p', 'rb') as f:
        img_list = pickle.load(f)

    cvt_list = []

    for label, img in img_list:
        #cv2.imshow("Image", np.reshape(img, (16,16)))
        #cv2.waitKey(0)

        converted_image = convert_img(img)
        re_img = np.reshape(np.array(converted_image), (16,16))
        cvt_list.append([label, re_img])
        
        #cv2.imshow("Converted Image", converted_image)
        #cv2.waitKey(0)
        #print(converted_image)
        #print(f'{img_file} converted.')
        
    with open('lane2_thres.p', 'wb') as f:   
        pickle.dump(cvt_list, f)

    print('All data saved.')