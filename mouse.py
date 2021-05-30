def mouse_click():
    import cv2
    global init

    # Variables
    init = [0,0,0]

    # Load image
    img = cv2.imread(cv2.samples.findFile("legos.png"))


    # Reduce the image
    height, width = img.shape[:2]
    size = (int(width * 0.5), int(height * 0.5))  # bgr
    img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)

    # Convert BGR to HSV
    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Mouse left button action
    def getposHsv(event, x, y, flags, param):
        global init
        if event == cv2.EVENT_LBUTTONDOWN:
            print("HSV is", HSV[y, x])
            init[0]=HSV[y,x][0]
            init[1] = HSV[y, x][1]
            init[2] = HSV[y, x][2]

    # Display the result image
    cv2.imshow('image', img)

    # Call mouse left button action
    cv2.setMouseCallback("image", getposHsv)

    while(1):
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
        elif k == ord('s'):
            print('init is',init)
            return init
    cv2.destroyAllWindows()

