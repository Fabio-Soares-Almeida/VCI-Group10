# sizes.py
#
# System Global program
#

import cv2 as cv
import numpy as np
import ast
import time
from sympy import *
import math
from time import sleep
from picamera import PiCamera, Color
from picamera.array import PiRGBArray
from capture_img import capture_image

array_cores = []
array_valores = []

# Open file
arquivo = open("cores.txt", 'r+')
contente = arquivo.read()

# Import Dictionary
cores = ast.literal_eval(contente)

for x in cores:

    array_cores.append(str(x[:-2]))

for x in cores.values():

    array_valores.append(x)


# Camera Configuration
camera= PiCamera()
camera.resolution = (2592, 1952)
camera.sharpness = 70
camera.iso=100
sleep(2)
camera.shutter_speed= camera.exposure_speed
camera.exposure_mode = 'off'
camera.awb_mode= 'off'
camera.awb_gains= ((485/256), (397/256))
rawCapture = PiRGBArray(camera, size=(2592,1952))
time.sleep(0.1)
 
for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
   
    image=frame.array

    start = time.process_time()

    # Reduce the image
    height, width = image.shape[:2]
    size = (int(width * 0.50), int(height * 0.50))  # bgr
    image = cv.resize(image, size, interpolation=cv.INTER_AREA)

    count = 0

    while count<len(array_valores):


        cor = array_cores[count]
        id_cor = count

        lower = np.fromstring(array_valores[count], sep=',')
        upper = np.fromstring(array_valores[count+1], sep=',')
        count = count + 2

        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

        # Create mask
        mask = cv.inRange(hsv, lower, upper)

        # Pos-processing
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)

        edges = cv.Canny(closing, 100, 200)

        contours, hierarchy = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        n_legos = 0;

        for contour in contours:
            approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
            area = cv.contourArea(contour)
            if area > 1000:
                n_legos = n_legos + 1;

                rect = cv.minAreaRect(contour)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                cv.drawContours(image, [box], 0, (0, 0, 255), 2)
                lado_1 = round(rect[1][1]/29)
                lado_2 = round(rect[1][0]/29)

                # finding center point of shape
                M = cv.moments(contour)
                if M['m00'] != 0.0:
                    x = int(M['m10'] / M['m00'])
                    y = int(M['m01'] / M['m00'])

                perimetro = cv.arcLength(contour, True)

                cv.putText(image, cor, (x , y - 20), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                cv.putText(image, '('+str(lado_1)+'x'+str(lado_2)+')', (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv.putText(image, "Legos "+str(cor)+" = "+str(n_legos), (10 ,60+id_cor*15), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                                                                                                                                                                                                                                                                                                                                  
    
    tempo = time.process_time()-start
    r_tempo = round(tempo,4)
    cv.putText(image, "Process Time = "+str(r_tempo)+" s", (10 ,30), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    cv.imshow('image', image)

    rawCapture.truncate(0)
    
    if cv.waitKey(1) == ord('q'):
        break
    
cv.destroyAllWindows()