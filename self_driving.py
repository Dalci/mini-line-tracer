# Copyright Reserved (2020).
# Donghee Lee, Univ. of Seoul
#
__author__ = 'will'

from rc_car_interface import RC_Car_Interface
from tf_learn import DNN_Driver
import numpy as np
import time
import cv2

class SelfDriving:

    def __init__(self):
        self.rc_car_cntl = RC_Car_Interface()
        self.dnn_driver = DNN_Driver()

        self.rc_car_cntl.halt()
    
        self.velocity = 0
        self.direction = 0
    
        self.dnn_driver.tf_learn()
        print('Start Learning...')
    
    def rc_car_control(self, degree):
        #calculate left and right wheel speed with direction

        if degree < -30.0:
            self.rc_car_cntl.turn_right()
        if degree > 30.0:
            self.rc_car_cntl.turn_left()
        else:
            self.rc_car_cntl.go_forward()

    def drive(self):
        while True:

# For test only, get image from DNN test images
#            img from get_test_img() returns [256] array. Do not call np.reshape()
#            img = self.dnn_driver.get_test_img()
#            direction = self.dnn_driver.predict_direction(img)

            img = self.rc_car_cntl.get_image_from_camera()
# predict_direction wants [256] array, not [16,16]. Thus call np.reshape to convert [16,16] to [256] array
            img = np.reshape(img,img.shape[0]**2)

            direction = self.dnn_driver.predict_direction(img)         # predict with single image
            print(direction[0][0])
            self.rc_car_control(direction[0][0])

            # For debugging, show image
#            cv2.imshow("target",  cv2.resize(img, (280, 280)) )
#            cv2.waitKey(0)

            time.sleep(0.001)

        self.rc_car_cntl.stop()
        cv2.destroyAllWindows()

SelfDriving().drive()
