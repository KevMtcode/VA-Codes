import cv2 

def read_image(image_path):
    imageBgr = cv2.imread(image_path, 1) #1: Color
    imageGray = cv2.imread(image_path, 0) #0: Grayscale
    return imageBgr, imageGray

def main():
    image_path = "images/VisionArtificial.jpg" # Name of the image only in this folder
    imageBgr, imageGray = read_image(image_path)

    if imageBgr is not None:
        print("Image read successfully in BGR format.")
    else:
        print("Failed to read the image in BGR format.")
    
    if imageGray is not None:
        print("Image read successfully in Grayscale format.")
    else:
        print("Failed to read the image in Grayscale format.")

    
    imageBgr = resize_image(imageBgr)
    imageGray = resize_image(imageGray)
    print("image size (BGR): ", get_image_size(imageBgr))
    print("image size (Grayscale): ", get_image_size(imageGray))

    for i in range(get_image_size(imageGray)[0]):
        for j in range(get_image_size(imageGray)[1]):
            if get_pixel_value(imageGray, j, i) < 128:
                imageGray[i,j] = 0 #Darken the image
            else:
                imageGray[i,j] = 255
    
    for i in range(get_image_size(imageBgr)[0]):  #Width
        for j in range(get_image_size(imageBgr)[1]):  #Height
            get_pixel_value(imageBgr, j, i)[0] = get_pixel_value(imageBgr, j, i)[2]  #Blue --> Red
            get_pixel_value(imageBgr, j, i)[2] = get_pixel_value(imageBgr, j, i)[0]  #Red --> Blue


    #value_pixel_bgr = get_pixel_value(imageBgr, 0, 0)  
    #print("Pixel value at (0, 0) in BGR image: ", value_pixel_bgr)    #value_pixel_bgr[0] to access to Blue
    #value_pixel_gray = get_pixel_value(imageGray, 0, 0)
    #print("Pixel value at (0, 0) in Grayscale image: ", value_pixel_gray)
    
    show_image(imageBgr, "BGR Image")
    show_image(imageGray, "Grayscale Image")

def show_image(image, title="Image"):
    cv2.imshow(title, resize_image(image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def resize_image(image):
    resized_image = cv2.resize(image, (600, 480))   # (width, height)
    return resized_image

def get_image_size(image):
    return image.shape[:2] #(height, width)

def get_pixel_value(image, x, y):   # Range of pixel's values: 0 - 255 
    return image[y, x] # OpenCV uses (y,x) for pixel access

if __name__ == "__main__":  #Start at main function
    main()
