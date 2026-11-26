import cv2
import numpy as np

#capture = cv2.VideoCapture(0) #Si es USB, poner adentro como int(0, 1 o 2); (0) siendo la webcam
capture = cv2.VideoCapture(r'C:\Users\varga\OneDrive - Universidad EIA\Documents\Universidad EIA\Sexto Semestre\Vision_Artificial-Electiva\VA_Codes\Contornos-Video\video_1_12.avi') #poner la ruta del video en formato mp4, avi
# capture = cv2.VideoCapture("protocolo + ip de la cámara") #protocolo rtsp, http, ftp

while capture.isOpened():
    ret, frame = capture.read() #Imágenes en el video
    #NO puede haber algo antes de if not ret, porque luego no detecta frame
    if not ret: #Si esto es verdad, es porque no encuentra video o ya se acabó
        print("No se puede recibir el frame. Saliendo...")
        break
    cv2.imshow('Frame', frame)
    if cv2.waitKey(60) == ord('q'): #waiKey(tiempo en ms)
        break
