import cv2 as cv
img=cv.imread('groundtruth-rot0-4.png')
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
#_,threshold = cv.threshold(gray, 120, 255, cv.THRESH_BINARY)
threshold = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
contours,_ = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
threshold = cv.resize(threshold, (700, 700))
cv.imshow('Hmmm',threshold)
cv.waitKey(0)
print(contours)
for contour in contours:
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
    cv.drawContours(img, [contour], 0, (0, 0, 255), 5)
    # using drawContours() function

# finding center point of shape
    M = cv.moments(contour)
    if M['m00'] != 0.0:
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])

# putting shape name at center of each shape
    if len(approx) == 3:
        cv.putText(img, 'Triangle', (x, y),
        cv.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 255), 2)

    elif len(approx) == 4:
        cv.putText(img, 'Quadrilateral', (x, y),
        cv.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 255), 2)

    elif len(approx) == 5:
        cv.putText(img, 'Pentagon', (x, y),
        cv.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 255), 2)

    elif len(approx) == 6:
        cv.putText(img, 'Hexagon', (x, y),
        cv.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 255), 2)

    else:
        cv.putText(img, 'circle', (x, y),
        cv.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 255), 2) #Neste caso considera-se "circulo" a figuras geometricas com mais de 6 vertices
img = cv.resize(img, (700, 700))
# displaying the image after drawing contours
cv.imshow('shapes', img)
cv.waitKey(0)
cv.destroyAllWindows()
