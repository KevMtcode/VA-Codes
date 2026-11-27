import cv2

def read_image(image_path):
    # Read the image from the specified
    imageBgr = cv2.imread(image_path, 1)
    imageGray = cv2.imread(image_path, 0)
    return imageBgr, imageGray

def binaryGray(image, method = 0, Umin=0, Umax=255):

    if method == 0:
        # Use a fixed threshold value
        ret, imgBinary = cv2.threshold(image, Umin, 255, cv2.THRESH_BINARY)
    else:
        imgBinary = cv2.inRange(image, Umin, Umax)
    return imgBinary

def binaryColor(image,  Bmin, Gmin, Rmin, Bmax, Gmax, Rmax ):
    imgBinary = cv2.inRange(image, (Bmin,Gmin,Rmin), (Bmax,Gmax,Rmax))
    return imgBinary

def show_image(image, title="Image"):
    cv2.imshow(title, cv2.resize(image, (600, 480)))
    # cv2.imshow(title, resize_image(image))

def main():
    image_path = r"images_quiz\images\nivel_2\A30_133.bmp"  # Replace with your image path
    #image_path = "images/test.png"  # Replace with your image path
    imageBgr, imageGray = read_image(image_path)
    while True:
        #get trackbar values
        # Umin = cv2.getTrackbarPos('Umin', 'Binary Image') # for imageGray
        # Umax = cv2.getTrackbarPos('Umax', 'Binary Image') # for imageGray
        #Bmin = cv2.getTrackbarPos('Bmin', 'Binary Image')
        #Bmax = cv2.getTrackbarPos('Bmax', 'Binary Image')
        #Gmin = cv2.getTrackbarPos('Gmin', 'Binary Image')
        #Gmax = cv2.getTrackbarPos('Gmax', 'Binary Image')
        #Rmin = cv2.getTrackbarPos('Rmin', 'Binary Image')
        #Rmax = cv2.getTrackbarPos('Rmax', 'Binary Image')
        Hmin = cv2.getTrackbarPos('Hmin', 'Binary Image')
        Hmax = cv2.getTrackbarPos('Hmax', 'Binary Image')
        Smin = cv2.getTrackbarPos('Smin', 'Binary Image')
        Smax = cv2.getTrackbarPos('Smax', 'Binary Image')
        Vmin = cv2.getTrackbarPos('Vmin', 'Binary Image')
        Vmax = cv2.getTrackbarPos('Vmax', 'Binary Image')
        # imageBinary = binaryGray(imageGray, 1, Umin, Umax)
        imageHSV = transformSpaceColor(imageBgr)
        #imageBinary = binaryColor(imageBgr, Bmin, Gmin, Rmin, Bmax, Gmax, Rmax)
        imageBinary = binaryColor(imageHSV, Hmin, Smin, Vmin, Hmax, Smax, Vmax)
        #show_image(imageHSV, "HSV Image")
        # show_image(imageGray, "Grayscale Image")
        show_image(imageBinary, "Binary Image")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def create_trackbarGray():
    cv2.namedWindow('Binary Image')
    cv2.createTrackbar('Umin', 'Binary Image', 0, 255, lambda x: None)
    cv2.createTrackbar('Umax', 'Binary Image', 0, 255, lambda x: None)

def create_trackbarColor():
    cv2.namedWindow('Binary Image')
    #cv2.createTrackbar('Bmin', 'Binary Image', 0, 255, lambda x: None)
    #cv2.createTrackbar('Bmax', 'Binary Image', 0, 255, lambda x: None)
    #cv2.createTrackbar('Gmin', 'Binary Image', 0, 255, lambda x: None)
    #cv2.createTrackbar('Gmax', 'Binary Image', 0, 255, lambda x: None)
    #cv2.createTrackbar('Rmin', 'Binary Image', 0, 255, lambda x: None)
    #cv2.createTrackbar('Rmax', 'Binary Image', 0, 255, lambda x: None)

    cv2.createTrackbar('Hmin', 'Binary Image', 0, 255, lambda x: None)
    cv2.createTrackbar('Hmax', 'Binary Image', 0, 255, lambda x: None)
    cv2.createTrackbar('Smin', 'Binary Image', 0, 255, lambda x: None)
    cv2.createTrackbar('Smax', 'Binary Image', 0, 255, lambda x: None)
    cv2.createTrackbar('Vmin', 'Binary Image', 0, 255, lambda x: None)
    cv2.createTrackbar('Vmax', 'Binary Image', 0, 255, lambda x: None)

def transformSpaceColor(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # BGR to HSV

if __name__ == "__main__":
    #create_trackbarGray()
    create_trackbarColor()
    main()