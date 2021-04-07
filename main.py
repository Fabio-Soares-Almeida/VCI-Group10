import cv2 as cv
#from acquire import acquire

#def acquire():

#----------------------------------------- ACQUIRE --------------------------------------------------------
cap = cv.VideoCapture(0)                           # chose pc camera

while(cv.waitKey(20) & 0xFF != ord('q')):
    ret, frame = cap.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)   # convert to gray
    hsv  = cv.cvtColor(frame,cv.COLOR_BGR2HSV)    # convert to hsv

    cv.imshow('frame', frame)                      # show img normal
    cv.imshow('HSV', hsv)                          # show img in hsv
    cv.imshow('Gray', gray)                        # show img in gray

    if cv.waitKey(20) & 0xFF == ord('s'):          #save images
        cv.imwrite('normal.png',frame)             #When 's' is pressed
        cv.imwrite('hsv.png',hsv)
        cv.imwrite('gray.png',gray)

cap.release()
cv.destroyAllWindows()

#----------------------------------------- CALIBRATION --------------------------------------------------------

#def cal(x):
 #   pass



#cv.namedWindow('Change Color')
#high = 'Max'
#low  = 'Min'

#wnd = 'Colorbar'

#cv.createTrackbar("Max","Change Color",0,255, cal)

#cv.createTrackbar("Min","Change Color",0,255, cal)

#img  = cv.imread(input("Name: "))
#print("Press S -> save an image")
#print("Press Q -> quit\n")

#while(cv.waitKey(30) & 0xFF != ord('q')) :
    #i1   = cv.getTrackbarPos("Max","Change Color")
    #i2  = cv.getTrackbarPos("Min","Change Color")

    #ret,cal1 = cv.threshold(img,i1,i2,cv.THRESH_BINARY)
    #ret,cal2 = cv.threshold(img,i1,i2,cv.THRESH_TOZERO)
    #cv.imshow ("image_cal_1", cal1 )
    #cv.imshow ("image_cal 2", cal2 )
    #if cv.waitKey(30) & 0xFF == ord('s'):                   #Save images
        #cv.imwrite('calibrated_1.png',calibration1)         #when 's' is pressed
        #cv.imwrite('calibrated_2.png',calibration2)

#cv.destroyAllWindows()

