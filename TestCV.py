import cv2
import numpy as np
from matplotlib import pyplot as plt
# mouse callback function
def printScreen(count,frame):
    FN="Photo1"+str(count)+".jpg"
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
BLUE = [255,0,255]
replicate = cv2.copyMakeBorder(img,10,10,10,10,cv2.BORDER_REPLICATE)
reflect = cv2.copyMakeBorder(img,10,10,10,10,cv2.BORDER_REFLECT)
reflect101 = cv2.copyMakeBorder(img,10,10,10,10,cv2.BORDER_REFLECT_101)
wrap = cv2.copyMakeBorder(img,10,10,10,10,cv2.BORDER_WRAP)
constant= cv2.copyMakeBorder(img,10,10,10,10,cv2.BORDER_CONSTANT,value=BLUE)
plt.subplot(231),plt.imshow(img,'gray'),plt.title('ORIGINAL')
plt.subplot(232),plt.imshow(replicate,'gray'),plt.title('REPLICATE')
plt.subplot(233),plt.imshow(reflect,'gray'),plt.title('REFLECT')
plt.subplot(234),plt.imshow(reflect101,'gray'),plt.title('REFLECT_101')
plt.subplot(235),plt.imshow(wrap,'gray'),plt.title('WRAP')
plt.subplot(236),plt.imshow(constant,'gray'),plt.title('CONSTANT')
plt.show()
