# min_max.py
#
# System Calibration program
# This program allows us to creat all the mask for the color that the system can identify
#
# Running process:
#   - Pick a point with the left mouse button
#   - Press 's' to save the point picked
#   / A new window opens
#   - Click in a point of the image to include it in the mask (if click in a point and realize that you don't want the result, you can press 'r' and the mask return to the previous state)
#   - After the mask is fine press 's' to save it
#   - Write the name of the file where the masks will be saved
#   - Write the color of the maks created
#   - Check the message with the indication that the color has been recorded
#   - Repeat the process for all desired colors

import cv2
import numpy as np
import ast
from mouse import mouse_click

# Variables
global init
init = [0,0,0]
cores = {}

# Call mouse_click() function in order to obtaining the initial limit values of the mask
init_val = mouse_click()

def nothing(x):
    pass

# Load image
image = cv2.imread(cv2.samples.findFile("legos3.png"))

# Mouse right button action
def getposHsv_right(event, x, y, flags, param):
    global hMin,sMin,vMin,hMax,sMax,vMax,hMin_p,sMin_p,vMin_p,hMax_p,sMax_p,vMax_p
    if event == cv2.EVENT_RBUTTONDOWN:
        print("HSV is", hsv[y, x])

        #   Save the current values before update to allows us to return to previus mask state
        hMin_p = hMin
        sMin_p = sMin
        vMin_p = vMin
        hMax_p = hMax
        sMax_p = sMax
        vMax_p = vMax

        #   See if the HSV values of the picked pixel is outside the limits of the mask, and if so, update them
        if(hsv[y, x][0] < hMin):
            hMin=hsv[y, x][0]
        if(hsv[y, x][1] < sMin):
            sMin = hsv[y, x][1]
        if(hsv[y, x][2] < vMin):
            vMin = hsv[y, x][2]
        if(hsv[y, x][0] > hMax):
            hMax = hsv[y, x][0]
        if(hsv[y, x][1] > sMax):
            sMax = hsv[y, x][1]
        if(hsv[y, x][2] > vMax):
            vMax = hsv[y, x][2]



# Reduce the image
height, width = image.shape[:2]
size = (int(width * 0.4), int(height * 0.15))  # bgr
image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)

# Create a window
cv2.namedWindow('image')

# Create the trackbars for see the color change
cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
cv2.createTrackbar('VMax', 'image', 0, 255, nothing)


# Initialize HSV min/max values with the returned by the mouse_click function
hMin = init_val[0]-10
sMin = init_val[1]-5
vMin = init_val[2]-5
hMax = init_val[0]+10
sMax = init_val[1]+5
vMax = init_val[2]+5


while(1):

    # Call mouse right button action
    cv2.setMouseCallback("image", getposHsv_right)

    #  Set the limit values of the mask in to trackbars
    cv2.setTrackbarPos('HMin', 'image', hMin)
    cv2.setTrackbarPos('SMin', 'image', sMin)
    cv2.setTrackbarPos('VMin', 'image', vMin)
    cv2.setTrackbarPos('HMax', 'image', hMax)
    cv2.setTrackbarPos('VMax', 'image', sMax)
    cv2.setTrackbarPos('SMax', 'image', vMax)

    # Set minimum and maximum HSV values to display
    lower = np.array([int(hMin), int(sMin), int(vMin)])
    upper = np.array([int(hMax), int(sMax), int(vMax)])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create the mak
    mask = cv2.inRange(hsv, lower, upper)

    # Create an image using the mask
    result = cv2.bitwise_and(image, image, mask=mask)

    # Display the result image
    cv2.imshow('image', result)
    k = cv2.waitKey(10) & 0xFF
    if k == ord('q'):
        break
    # if you press 'r' the mask return to the previous state
    elif k == ord('r'):
        print(hMin_p,sMin_p,vMin_p,hMax_p,sMax_p,vMax_p)
        hMin = hMin_p
        sMin = sMin_p
        vMin = vMin_p
        hMax = hMax_p
        sMax = sMax_p
        vMax = vMax_p

    # if maks is fine and you wont to save it
    elif k == ord('s'):

        # read the name of the file, open it and read the dictionary
        try:
            nome_arquivo = input('Nome do ficheiro:')
            arquivo = open(nome_arquivo, 'r+')
            contente = arquivo.read()
            cores = ast.literal_eval(contente)
            arquivo.seek(0)
            arquivo.truncate(0)
        # if file does not exist, create it
        except FileNotFoundError:
            arquivo = open(nome_arquivo, 'w+')



        print("Cor a gravar:")
        color = input()

        # see if the color already exists
        if(str(color+'_l') in cores):
            print('Cor já existe')
            break
        else:
            texto_l = (str(hMin) + ',' + str(sMin) + ',' + str(vMin))
            texto_u = (str(hMax) + ',' + str(sMax) + ',' + str(vMax))
            cores[color+'_l'] = texto_l
            cores[color+'_u'] = texto_u

        # write the dictionary in to the file
        arquivo.write(str(cores))
        arquivo.close()
        print("Cor gravada:", color)

        # call the mouse_click function again to repeat the all the process for every color you want
        init_val=mouse_click()
        hMin = init_val[0] - 10
        sMin = init_val[1] - 5
        vMin = init_val[2] - 5
        hMax = init_val[0] + 10
        sMax = init_val[1] + 5
        vMax = init_val[2] + 5

cv2.destroyAllWindows()