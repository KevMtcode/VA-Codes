import cv2
import numpy as np

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

def main():
    image_path = r"C:\Users\varga\OneDrive - Universidad EIA\Documents\Universidad EIA\Sexto Semestre\Vision_Artificial-Electiva\VA_Codes\Contornos-Video\leukemia.jpg"  # Replace with your image path
    imageBgr, imageGray = read_image(image_path)
    
    mask = binaryColor(imageBgr, 107, 0, 104, 246, 91, 255) #Binarizar
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #Encontrar los contornos
    maskColor = np.zeros(imageBgr.shape[:])
    
    # Filtro espacial (suavizar el contorno al hacer que los pixeles vecinos se parezcan a los centrales):
    mask_median = cv2.medianBlur(mask, 5) # preserva mejor el borde; el filtro de la mediana debe ser impar
    kernel = np.ones((5,5), np.float32) / 25
    mask_filter2d = cv2.filter2D(mask, -1, kernel) # (n, m) de tamaño nxm, asemeja los pixeles al promedio de estos
    mask_gaussian = cv2.GaussianBlur(mask, (5,5), 0) # (n, m) de tamaño nxm, gaussiana es como borrosa, para mayor suavización y detección de bordes
   
    # Filtro morfológico:
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)) #KERNEL
    mask_erode = cv2.erode(mask, kernel, iterations = 1) #Por erosión (reduce el tamaño del objeto detectado), para quitar puntos blancos aislados o en el borde
    mask_dilate = cv2.dilate(mask_erode, kernel, iterations = 1) #Por dilatación (aumentar el tamaño original o recuperarlo después de erosión), para conectar partes blancas casi unidas
    mask_closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) #Dilatación seguida de erosión, para cerrar huecos pequeños y permanecer con el tamaño casi original
    mask_opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)#Erosión seguida de dilatación, para eliminar ruído

    # Análisis de contornos:
    count_real = 0
    if(len(contours) > 0):
        for cnt in contours: #Para dibujar cada contorno encerrados en rectángulos
            x,y,w,h = cv2.boundingRect(cnt) #Un contorno es un array de coordenadas (x,y)
            area = cv2.contourArea(cnt) #Encontrar el área de los pixeles de los contornos
            if area > 40: #Por ejemplo
                count_real += 1
                cv2.drawContours(maskColor, contours, -1, (0, 0, 255), 3) #Dibujar la forma original de los contornos

                #Draw rectangle:
                cv2.rectangle(imageBgr, (x,y), (x+w, y+h), (0, 255, 0), 2) #Encerrar los contornos en rectángulos
                cv2.imshow('Contours', imageBgr)
                cv2.imshow('Contours in maskColor', maskColor) #Cómo se ven los contornos realmente
                cv2.waitKey(0)
    print(f'Number of contours found: {count_real}')

    cv2.imshow('Imagen binaria', mask) #Imagen binaria
    cv2.imshow('Imagen con contornos', imageBgr) #Imagen con contornos
    cv2.imshow('Con filtro de mediana', mask_median) #Imagen suavizada por filtro usado por mediana
    #cv2.imshow('Imagen erosionada', mask_erode)
    #cv2.imshow('Imagen dilatada', mask_dilate)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()