# Copyright(c) Reserved 2020.
# Donghee Lee, University of Soul
#
__author__ = 'will'

import numpy as np
import cv2
import serial

#from picamera.array import PiRGBArray
#from picamera import PiCamera
SPEED = 250

class RC_Car_Interface():

    def __init__(self):
        # self.left_wheel = 0
        # self.right_wheel = 0
        self.ser = serial.Serial('/dev/ttyS0', 115200)
        if self.ser.writable():
            print('Serial is ready.')

        self.camera = PiCamera()
        self.camera.resolution = (320,320)         # set camera resolution to (320, 320)
        self.camera.color_effects = (128,128)      # set camera to black and white

    def finish_iteration(self):
        self.ser.write('END\n'.encode('ascii'))
        print('finish iteration')

    def turn_right(self, speed=SPEED):
        self.ser.write(f'R{speed}\n'.encode('ascii'))
        print('turn right speed to ', speed)

    def turn_left(self, speed=SPEED):
        self.ser.write(f'L{speed}\n'.encode('ascii'))
        print('turn left speed to ', speed)

    def rear_right(self, speed=SPEED):
        self.ser.write(f'r{speed}\n'.encode('ascii'))
        print('turn right rear speed to ',speed)

    def rear_left(self, speed=SPEED):
        self.ser.write(f'l{speed}\n'.encode('ascii'))
        print('turn left rear speed to ',speed)

    def go_forward(self, speed=SPEED):
        self.ser.write(f'B{speed}\n'.encode('ascii'))
        print(f'Go Forward. Speed = {speed}')

    def go_backward(self, speed=SPEED):
        self.ser.write(f'r{speed}\n'.encode('ascii'))
        print(f'Go Backward. Speed = {speed}')

    def halt(self):
        self.ser.write('0\n'.encode('ascii'))
        print('Halt!')
        
    def get_image_from_camera(self):
        img = np.empty((320, 320, 3), dtype=np.uint8)
        self.camera.capture(img, 'bgr')
        
        img = img[:,:,0]           # 3 dimensions have the same value because camera is set to black and white
                                   # remove two dimension data
        print(img)
        
        threshold = int(np.mean(img))*0.5
#        print(threshold)

        # Invert black and white with threshold
        ret, img2 = cv2.threshold(img.astype(np.uint8), threshold, 255, cv2.THRESH_BINARY_INV)

        img2 = cv2.resize(img2, (16,16), interpolation=cv2.INTER_AREA)
#        cv2.imshow("Image", img2)
#        cv2.waitKey(0)
        return img2

    def stop(self):     # robot stop
        print('stop')

# Test Only
# RC_Car_Interface().get_image_from_camera()