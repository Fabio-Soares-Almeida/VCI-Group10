def capture_image():
    import cv2 as cv

    cam = cv.VideoCapture(0)

    cv.namedWindow("test")

    img_counter = 0

    while img_counter == 0:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv.imshow("test", frame)

        k = cv.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            img_name = "image_test.png".format(img_counter)
            cv.imwrite(img_name, gray)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()

    cv.destroyAllWindows()