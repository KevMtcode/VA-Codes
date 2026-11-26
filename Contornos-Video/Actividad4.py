import cv2
import numpy as np

def binaryGray(image, method = 0, Umin=0, Umax=255):

    if method == 0:
        # Use a fixed threshold value
        ret, imgBinary = cv2.threshold(image, Umin, 255, cv2.THRESH_BINARY)
    else:
        imgBinary = cv2.inRange(image, Umin, Umax)
    return imgBinary

def main():
    capture = cv2.VideoCapture(r'C:\Users\varga\OneDrive - Universidad EIA\Documents\Universidad EIA\Sexto Semestre\Vision_Artificial-Electiva\VA_Codes\Contornos-Video\video_1_12.avi') #poner la ruta del video en formato mp4, avi
    count = 0
    count24 = 0 
    count_g8 = 0
    count_go = 0
    area_0 = 0
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret: 
            print("Saliendo del video...")
            break
        #cv2.imshow('Frame', imageBinary)
        imageGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        maskbin = binaryGray(imageGray, 1, 32, 180) #Binarizar
        mask = cv2.medianBlur(maskbin, 5) #Filtrar! Que no detecte lo que no es
        
        #Contar el número de piezas que pasan por la banda:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #Encontrar los contornos
        if(len(contours) > 0):
            for cnt in contours: 
                x,y,w,h = cv2.boundingRect(cnt)
                if x < 10 and w > 20 : # La pieza ya pasó por el final de la cámara (parte izquierda)
                    count+=1
                    if w==24:   #Este solo es para un recuadro que tiene el mismo ancho al llegar a x=0
                        count24+=1
                    if count24==2:
                        count-=1
                        count24=0
                #xc,yc,wc,hc = cv2.boundingRect(contours[-1]) #Coordenadas del último contorno detectado en el último frame
                if x == 86 and y == 110: #Última pieza que no llega hasta x = 0
                    count+=1
                #cv2.drawContours(mask, contours, -1, (0, 0, 255), 3) #Dibujar la forma original de los contornos
                #cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2) #Encerrar los contornos en rectángulos
                #cv2.imshow('Objetos identificados', frame)
                cv2.imshow('Contornos', mask) #Cómo se ven los contornos realmente
                cv2.waitKey(0)

        #Clasificar en dos grupos y contar las piezas:
        contours_cla, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) #Encontrar los todos contornos
        if(len(contours_cla) > 0):
            for cnt_cla in contours_cla: 
                x_cla,y_cla,w_cla,h_cla = cv2.boundingRect(cnt_cla)
                area = cv2.contourArea(cnt_cla)
                #cv2.drawContours(frame, contours_cla, -1, (0, 0, 255), 3) #Dibujar la forma original de los contornos.
                if x_cla > 120 and x_cla < 350: #Que la pieza esté en el centro y completa
                    if len(contours_cla) == 3 and area > 7370 and area < 7610:
                        #print("Grupo 8")
                        count_g8 +=1
                        if (abs(area - area_0) < 100): #Se volvió a contar la pieza
                            count_g8-=1
                        #print(area)
                        #print(area_0)
                        area_0 = area
                            
                    if len(contours_cla) == 2 and area > 13450 and area < 22000:
                        #print("Grupo O")
                        count_go +=1
                        #print(area)
                
    print(f'Número de piezas encontradas: {count}')
    print(f'Número de piezas del Grupo 8: {count_g8}')
    print(f'Número de piezas del Grupo O: {count_go}')

if __name__ == "__main__":
    main()

