import cv2
import numpy as np
import ast

array_cores = []
array_valores = []

# Load image
image = cv2.imread(cv2.samples.findFile("legos4.png"))

# Reduce the image
height, width = image.shape[:2]
size = (int(width * 0.2), int(height * 0.20))  # bgr
image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)


# Open file
arquivo = open("cores.txt", 'r+')
contente = arquivo.read()

# Import Dictionary
cores = ast.literal_eval(contente)

for x in cores:

    array_cores.append(str(x[:-2]))

print(array_cores)

for x in cores.values():

    array_valores.append(x)

print(array_valores)

count = 0

while count<len(array_valores):

    print(array_cores[count])

    lower = np.fromstring(array_valores[count], sep=',')
    upper = np.fromstring(array_valores[count+1], sep=',')
    print(lower)
    print(upper)
    count = count + 2

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create mask
    mask = cv2.inRange(hsv, lower, upper)

    #ret, thresh = cv2.threshold(mask, 127, 255, 0)
    edges = cv2.Canny(mask,100,200)
    cv2.imshow('image_2',edges)
    cv2.imshow('image_3',mask)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        cv2.drawContours(image, [contour], 0, (0, 0, 255), 2)

while (1):

    # Display result image
    cv2.imshow('image', image)
    k = cv2.waitKey(10) & 0xFF
    if k == ord('q'):
        break
