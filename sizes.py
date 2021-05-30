import cv2 as cv
import numpy as np
import ast
from sympy import *
#from skimage.morphology import watershed
import math
from time import sleep
from picamera import PiCamera, Color

from capture_img import capture_image

array_cores = []
array_valores = []

#capture_image()
camera= PiCamera()
camera.resolution = (2592, 1944)
camera.start_preview()
sleep(2)
camera.capture('/home/pi/Desktop/legos.png')
camera.stop_preview()
# Load image
image = cv.imread(cv.samples.findFile("legos.png"))

# Reduce the image
height, width = image.shape[:2]
size = (int(width * 0.50), int(height * 0.50))  # bgr
image = cv.resize(image, size, interpolation=cv.INTER_AREA)


# Open file
arquivo = open("cores_3.txt", 'r+')
contente = arquivo.read()

# Import Dictionary
cores = ast.literal_eval(contente)

for x in cores:

    array_cores.append(str(x[:-2]))

#print(array_cores)

for x in cores.values():

    array_valores.append(x)

#print(array_valores)

count = 0

while count<len(array_valores):

    #print(array_cores[count])
    cor = array_cores[count]

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
    

    #cv.imshow('mask',mask)
    #cv.imshow('opening',closing)
    #cv.imshow('closing',closing)

    edges = cv.Canny(closing, 100, 200)

    contours, hierarchy = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    n_legos = 0;

    for contour in contours:
        approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
        area = cv.contourArea(contour)
        if area > 1000:
            n_legos = n_legos + 1;
            #print("Area:", area)

            # Retangulo com inclinacao
            rect = cv.minAreaRect(contour)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            cv.drawContours(image, [box], 0, (0, 0, 255), 2)
            #cv2.drawContours(image, [contour], 0, (0, 0, 255), 2)
            lado_1 = round(rect[1][1]/29)
            lado_2 = round(rect[1][0]/29)

            #print('Tamanho em pixeis: '+str(rect[1][1])+' x '+str(rect[1][0]))
            #print('Tamanho em encaixes: ' + str(lado_1) + ' x ' + str(lado_2))

            # Retangulo sem inclinacao
            #x, y, w, h = cv2.boundingRect(contour)
            #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            #cv2.drawContours(image, [contour], 0, (0, 0, 255), 2)

            # finding center point of shape
            M = cv.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
                #print("Centroide: "+str(x)+' ; '+str(y))
                #print(x, y)

            perimetro = cv.arcLength(contour, True)
            #print("Perimetro:", perimetro)


            cv.putText(image, cor, (x , y - 20), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv.putText(image, '('+str(lado_1)+'x'+str(lado_2)+')', (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    print(' ')
    print("Numero de legos "+ str(cor)+" = "+str(n_legos))
    print(' ')


while (1):

    # Display result image
    cv.imshow('image', image)
    #img_name = "result.png".format(0)
    cv.imwrite('Result.png', image)
    k = cv.waitKey(10) & 0xFF
    if k == ord('q'):
        break
