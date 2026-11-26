import threading #Para que siga procesando la cámara independientemente de la GUI
import cv2
from logger_actividad5 import Logger
import time

# Acá en camera.py se hace el procesamiento de imágenes:

class RunCamera(): # Obtener frames de la cámara en paralelo al funcionamiento de GUI
    def __init__(self, src=0, name="camera_1"):
        self.loggerReport = Logger("logCamera")
        try:
            self.name = name
            self.src = src
            self.ret = None
            self.frame = None
            self.stopped = False
            
            #Variables para el procesamiento del video:
            self.count_g8 = 0
            self.count_go = 0
            self.area_0 = 0
            self.mask = None

            self.loggerReport.logger.info("Init constructor RunCamera") #Para poner mensajes
        except Exception as e:
            self.loggerReport.logger.error("Error in RunCamera ", e) #Poner el error en string

    def binaryGray(self, image, method = 0, Umin=0, Umax=255):
        if method == 0:
            # Use a fixed threshold value
            ret, imgBinary = cv2.threshold(image, Umin, 255, cv2.THRESH_BINARY)
        else:
            imgBinary = cv2.inRange(image, Umin, Umax)
        return imgBinary

    def count_pieces(self, frame): #Función para el procesamiento del video
        #cv2.imshow('Frame', imageBinary)
        imageGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        maskbin = self.binaryGray(imageGray, 1, 32, 180) #Binarizar
        self.mask = cv2.medianBlur(maskbin, 5) #Filtrar! Que no detecte lo que no es

        #Clasificar en dos grupos y contar las piezas:
        contours_cla, _ = cv2.findContours(self.mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) #Encontrar los todos contornos
        if(len(contours_cla) > 0):
            for cnt_cla in contours_cla: 
                x_cla,y_cla,w_cla,h_cla = cv2.boundingRect(cnt_cla)
                area = cv2.contourArea(cnt_cla)
                #cv2.drawContours(frame, contours_cla, -1, (0, 0, 255), 3) #Dibujar la forma original de los contornos.
                if x_cla > 120 and x_cla < 350: #Que la pieza esté en el centro y completa
                    if len(contours_cla) == 3 and area > 7370 and area < 7610:
                        #print("Grupo 8")
                        self.count_g8 +=1
                        if (abs(area - self.area_0) < 100): #Se volvió a contar la pieza
                            self.count_g8-=1
                        #print(area)
                        #print(area_0)
                        self.area_0 = area
                            
                    if len(contours_cla) == 2 and area > 13450 and area < 22000:
                        #print("Grupo O")
                        self.count_go +=1
                        #print(area)
        return self.mask
        
    def start(self):
        try:
            self.stream = cv2.VideoCapture(self.src)
            time.sleep(1) #Por si se demora en arrancar la cámara
            self.ret, self.frame = self.stream.read() #Guardar los frames del video
            if(self.stream.isOpened()):
                self.loggerReport.logger.info("Creating Thread in start camera")
                self.my_thread = threading.Thread(target=self.get, name=self.name, daemon=True)
                self.my_thread.start()
            else:
                self.loggerReport.logger.warning("start camera no initialized")
        except Exception as e:
            self.loggerReport.logger.error("Error in start Camera ", e) #Poner el error en string
    
    def get(self):
        while not self.stopped:
            if not self.ret:
                pass
            else:
                try:
                    self.ret, self.frame = self.stream.read()
                    if not self.ret or self.frame is None:
                        self.loggerReport.logger.warning("Frame vacío en RunCamera.get() o video terminado")
                        return None
                    self.count_pieces(self.frame) #____ Función para el procesamiento del video acá___
                except Exception as e:
                    self.loggerReport.logger.error("Error in get Camera ", e)


    