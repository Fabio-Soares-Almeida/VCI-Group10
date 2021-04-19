import cv2
import numpy as np
from matplotlib import pyplot as plt
# mouse callback function
def printScreen(count,frame):
    FN="Photo"+str(count)+".jpg"
    cv2.imwrite(FN, frame)
    print("It works")
cv2.namedWindow("Cam-Test")
vc = cv2.VideoCapture(1) # 1 - Connection to webcam with USB, 0 - Connection to webcam of pc

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
count=0
while rval:
    cv2.imshow("Cam-Test", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key==ord("p"):
        printScreen(count,frame)
        count=count+1
    if key == 27: # exit on ESC
        break
vc.release()
cv2.destroyWindow("Cam-Test")
img = cv2.imread(cv2.samples.findFile("Photo0.jpg"))
cv2.imshow("Display window", img)
k = cv2.waitKey(0)
print(img.size)
print(img.shape)
b,g,r = cv2.split(img)
cv2.imshow("Display window Blue", b)
k = cv2.waitKey(0)
cv2.imshow("Display window Green", g)
k = cv2.waitKey(0)
cv2.imshow("Display window Red", r)
k = cv2.waitKey(0)

