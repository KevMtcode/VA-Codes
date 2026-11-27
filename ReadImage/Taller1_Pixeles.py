import cv2

def read_image(image_path):
    imageBgr = cv2.imread(image_path, 1)
    return imageBgr
def main():
    image_path = "images/delfin.jpg" 
    imageBgr = read_image(image_path)
    if imageBgr is not None:
        print("Image read successfully in BGR format.")
    else:
        print("Failed to read the image in BGR format.")
    
    imageBgr = resize_image(imageBgr)
    print("Image size (BGR): ", get_image_size(imageBgr))
    num = int(input("Ingrese el punto del taller (1-5, 6 para salir): "))
    while num != 6:
        match num:
            case 1:
                primer_punto(imageBgr)
            case 2:
                segundo_punto(imageBgr)
            case 3:
                tercer_punto(imageBgr)
            case 4:
                cuarto_punto(imageBgr)
            case 5:
                quinto_punto(imageBgr)
        num = int(input("Ingrese el punto del taller (1-5, 6 para salir): "))

def primer_punto(imageBgr):
    show_image(imageBgr, "Imagen Original")
    imageBgr_1 = imageBgr.copy()
    #   Imagen azul:
    for i in range(get_image_size(imageBgr)[0]):  #Height
        for j in range(get_image_size(imageBgr)[1]):  #Width
            bgr("blue", imageBgr, imageBgr_1, j, i)
    show_image(imageBgr_1, "Imagen Azul")

    #   Imagen verde:
    for i in range(get_image_size(imageBgr)[0]):  
        for j in range(get_image_size(imageBgr)[1]):  
            bgr("green", imageBgr, imageBgr_1, j, i)
    show_image(imageBgr_1, "Imagen Verde")

    #   Imagen roja:
    for i in range(get_image_size(imageBgr)[0]):  
        for j in range(get_image_size(imageBgr)[1]):  
            bgr("red", imageBgr, imageBgr_1, j, i)
    show_image(imageBgr_1, "Imagen Roja")

def segundo_punto(imageBgr):
    show_image(imageBgr, "Imagen Original")
    imageBgr_2 = imageBgr.copy()
    height = get_image_size(imageBgr)[0]
    width = get_image_size(imageBgr)[1]
    #   Imagen azul:
    for i in range(height):  
        for j in range(width):  
            #Conteo del ancho hacia atrás --> 500 - 0 - 1 = 499; 500 - 1 - 1 = 498 ...
            get_pixel_value(imageBgr_2, (width-j-1), i)[0] = get_pixel_value(imageBgr, j, i)[0] #Restar 1 para no salirse de la imagen
            get_pixel_value(imageBgr_2, (width-j-1), i)[1] = get_pixel_value(imageBgr, j, i)[1]
            get_pixel_value(imageBgr_2, (width-j-1), i)[2] = get_pixel_value(imageBgr, j, i)[2]
    
    show_image(imageBgr_2, "Imagen Invertida respecto a y")

def tercer_punto(imageBgr):
    show_image(imageBgr, "Imagen Original")
    imageBgr_3 = imageBgr.copy()
    height = get_image_size(imageBgr)[0]
    width = get_image_size(imageBgr)[1]
    #   Imagen azul:
    for i in range(height):  #Height
        for j in range(width):  #Width
            #Conteo de la altura hacia atrás --> 300 - 0 - 1 = 299; 300 - 1 - 1 = 298 ...
            get_pixel_value(imageBgr_3, j, (height-i-1))[0] = get_pixel_value(imageBgr, j, i)[0] #Restar 1 para no salirse de la imagen
            get_pixel_value(imageBgr_3, j, (height-i-1))[1] = get_pixel_value(imageBgr, j, i)[1]
            get_pixel_value(imageBgr_3, j, (height-i-1))[2] = get_pixel_value(imageBgr, j, i)[2]
    
    show_image(imageBgr_3, "Imagen Invertida respecto a y")

def cuarto_punto(imageBgr):
    show_image(imageBgr, "Imagen Original")
    imageBgr_4 = imageBgr.copy()
    #   Esquina superior derecha azul:
    for i in range(0, get_image_size(imageBgr_4)[0]//2):  #Height
        for j in range(get_image_size(imageBgr_4)[1]//2, get_image_size(imageBgr_4)[1]):  #Width
            get_pixel_value(imageBgr_4, j, i)[1]  = 0
            get_pixel_value(imageBgr_4, j, i)[2]  = 0
    #   Esquina inferior izquierda verde:
    for i in range(get_image_size(imageBgr_4)[0]//2, get_image_size(imageBgr_4)[0]):  
        for j in range(0, get_image_size(imageBgr_4)[1]//2):  
            get_pixel_value(imageBgr_4, j, i)[0]  = 0
            get_pixel_value(imageBgr_4, j, i)[1]  = get_pixel_value(imageBgr, j, i)[1]
    #   Esquina inferior derecha roja:
    for i in range(get_image_size(imageBgr_4)[0]//2, get_image_size(imageBgr_4)[0]):  
        for j in range(get_image_size(imageBgr_4)[1]//2, get_image_size(imageBgr_4)[1]):  
            get_pixel_value(imageBgr_4, j, i)[0]  = 0
            get_pixel_value(imageBgr_4, j, i)[1]  = 0
            get_pixel_value(imageBgr_4, j, i)[2]  = get_pixel_value(imageBgr, j, i)[2]

    show_image(imageBgr_4, "Imagen dividida BGR")

def quinto_punto(imageBgr):
    show_image(imageBgr, "Imagen Original")
    imageBgr_5 = imageBgr.copy()
    n = int(input("Ingrese el tamaño de la cuadrícula: "))
    # Filas empezando con cuadros azules:
    square("blue", imageBgr, imageBgr_5, n, 0, 0)
    square("green", imageBgr, imageBgr_5, n, 1, 0)
    square("red", imageBgr, imageBgr_5, n, 2, 0)
    
    # Filas empezando con cuadros verdes:
    square("green", imageBgr, imageBgr_5, n, 0, 1)
    square("red", imageBgr, imageBgr_5, n, 1, 1)
    square("blue", imageBgr, imageBgr_5, n, 2, 1)
    
    # Filas empezando con cuadros rojos:
    square("red", imageBgr, imageBgr_5, n, 0, 2)
    square("blue", imageBgr, imageBgr_5, n, 1, 2)
    square("green", imageBgr, imageBgr_5, n, 2, 2)

    show_image(imageBgr_5, "Imagen cuadriculada")

def square(color, original_image, imageBgr, n, order_column, order_row):
    for row in range(order_row, get_image_size(imageBgr)[0]//n, 3):
        h = (row+1)*n
        for i in range(row*n, h):  
                for a in range (order_column, get_image_size(imageBgr)[1]//n, 3):
                    w = (a+1)*n
                    for j in range(a*n, w):  
                        bgr(color, original_image, imageBgr, j, i)
            
                if get_image_size(imageBgr)[1]%n != 0:  
                    #Para llenar los cuadros que faltaron si la cantidad de estos de nxn no fue exacta para el tamaño de la imagen
                    a+=3   #Si sale error, es debido a que el tamaño n de la cuadrícula es tan grande que el patrón BGR se sale de la imagen! --> aumentar el tammaño de imagen
                    w = get_image_size(imageBgr)[1]
                    for j in range(a*n, w):  
                        bgr(color, original_image, imageBgr, j, i)

    if get_image_size(imageBgr)[0]%n != 0:
        #Para llenar los cuadros que faltaron si la cantidad de estos de nxn no fue exacta para el tamaño de la imagen
        row+=3
        h = get_image_size(imageBgr)[0]
        for i in range(row*n, h): 
            for a in range (order_column, get_image_size(imageBgr)[1]//n, 3):
                w = (a+1)*n
                for j in range(a*n, w):  
                    bgr(color, original_image, imageBgr, j, i)
                     
def bgr(color, original_image, imageBgr, j, i):
    match color:
        case "blue":
            get_pixel_value(imageBgr, j, i)[0]  = get_pixel_value(original_image, j, i)[0] #Color original de la imagen
            get_pixel_value(imageBgr, j, i)[1]  = 0 #Apagar verde
            get_pixel_value(imageBgr, j, i)[2]  = 0 #Apagar rojo
        case "green":
            get_pixel_value(imageBgr, j, i)[0]  = 0 #Apagar azul
            get_pixel_value(imageBgr, j, i)[1]  = get_pixel_value(original_image, j, i)[1] #Color original de la imagen
            get_pixel_value(imageBgr, j, i)[2]  = 0 #Apagar rojo
        case "red":
            get_pixel_value(imageBgr, j, i)[0]  = 0 #Apagar azul
            get_pixel_value(imageBgr, j, i)[1]  = 0 #Apagar verde
            get_pixel_value(imageBgr, j, i)[2]  = get_pixel_value(original_image, j, i)[2] #Color original de la imagen

def show_image(image, title = "Image"):
    cv2.imshow(title, resize_image(image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def resize_image(image):
    resized_image = cv2.resize(image, (500, 300))  # (width, height)
    return resized_image

def get_image_size(image):
    return image.shape[:2] #(height, width)

def get_pixel_value(image, x, y):   # Range of pixels' values: 0 - 255 
    return image[y, x] # OpenCV uses (y,x) for pixel access

if __name__ == "__main__":  #Start at main function
    main()