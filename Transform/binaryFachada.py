import cv2

def read_image(image_path):
    # Read the image from the specified
    imageBgr = cv2.imread(image_path, 1)
    imageGray = cv2.imread(image_path, 0)
    return imageBgr, imageGray

def binaryColor(image,  Bmin, Gmin, Rmin, Bmax, Gmax, Rmax ):
    imgBinary = cv2.inRange(image, (Bmin,Gmin,Rmin), (Bmax,Gmax,Rmax))
    return imgBinary

def show_image(image, title="Image"):
    cv2.imshow(title, cv2.resize(image, (600, 480)))
    # cv2.imshow(title, resize_image(image))

def drawRectangle(image, x, y, width, height, b, g, r, thickness):
    cv2.rectangle(image, (x, y), (x + width, y + height), (b, g, r), thickness)
    return image

def get_pixel_value(image, x, y):   # Range of pixels' values: 0 - 255 
    return image[y, x]

def get_image_size(image):
    return image.shape[:2] 

def main():
    image_path = "images/imagenFachada.png"  # Replace with your image path
    imageBgr, imageGray = read_image(image_path)
    imageHSV = cv2.cvtColor(imageBgr, cv2.COLOR_BGR2HSV)
    imageBinary = binaryColor(imageHSV, 12, 123, 135, 35, 253, 247) #Identified zone of interest considering HSV parameteres
    imageBinaryBGR = cv2.cvtColor(imageBinary, cv2.COLOR_GRAY2BGR) #Binary to BGR
    imageBinaryHSV = cv2.cvtColor(imageBinaryBGR, cv2.COLOR_BGR2HSV) #Binary to HSV
    while True:
        # Original image:
        mask_0 = (imageBinary == 0) 
        imageBinaryHSV[mask_0] = imageHSV[mask_0]
        
        # Painting the house: 
        if cv2.getTrackbarPos('Colores', 'Fachada') <= 55:
            mask = (imageBinary == 255)   # Boolean maks where there area white pixels.
            imageBinaryHSV[mask] = (120, 100, 150) #Paint Blue in HSV
        elif cv2.getTrackbarPos('Colores', 'Fachada') > 55 and cv2.getTrackbarPos('Colores', 'Fachada') <= 155:
            imageBinaryHSV[mask] = (0, 150, 150) #Paint Red in HSV
        else:
            imageBinaryHSV[mask] = (60, 160, 160) #Paint Green in HSV

        imageBinBGR = cv2.cvtColor(imageBinaryHSV, cv2.COLOR_HSV2BGR)
        drawRectangle(imageBinBGR, 200, 100, 700, 150, 200, 100, 100, -20)  #Blue  #negative thickness to fill the rectangle 
        drawRectangle(imageBinBGR, 950, 100, 700, 150, 100, 100, 200, -20)  #Red 
        drawRectangle(imageBinBGR, 1700, 100, 700, 150, 60, 160, 59, -20)  #Green
        show_image(imageBinBGR, "Fachada")  #Same title for the window as the one that has the created trackbar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def create_trackbarColor():
    cv2.namedWindow('Fachada')
    cv2.createTrackbar('Colores', 'Fachada', 0, 255, lambda x: None)

def transformSpaceColor(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Example conversion to HSV

if __name__ == "__main__":
    create_trackbarColor()
    main()