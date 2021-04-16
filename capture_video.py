#programa que captura o vídeo e  gaurda o vídeo e 3 imagens: normal, gray e hsv

def acquire():
    import cv2
    import numpy as np

    print("Press S to save an image")
    print("Press Q to quit\n")

    cap = cv2.VideoCapture(0)                           # chose pc camera

    while(cv2.waitKey(20) & 0xFF != ord('q')):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)   # convert to gray
        hsv  = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)    # convert to hsv

        cv2.imshow('frame', frame)                      # show img normal
        cv2.imshow('HSV', hsv)                          # show img in hsv
        cv2.imshow('Gray', gray)                        # show img in gray

        if cv2.waitKey(20) & 0xFF == ord('s'):          # save images
            cv2.imwrite('normal.png',frame)             # when 's' is pressed
            cv2.imwrite('hsv.png',hsv)
            cv2.imwrite('gray.png',gray)

    cap.release()
    cv2.destroyAllWindows()

def save():
    import cv2
    import numpy as np

    print("Press Q to quit\n")
    cap = cv2.VideoCapture(0)       #chose pc camera

    fourcc = cv2.VideoWriter_fourcc (*'XVID')
    output = cv2.VideoWriter ('./video_compressed.avi',fourcc,20.0, (640,480))

    while(True):
        ret, frame = cap.read()
        if ret == True:
                output.write(frame)
                cv2.imshow('video',frame)
                if cv2.waitKey(20) & 0xFF == ord('q'):          # stop capure
                    break

    cap.release()
    output.release()
    cv2.destroyAllWindows()