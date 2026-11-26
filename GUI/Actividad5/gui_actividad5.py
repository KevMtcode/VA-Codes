from logger_actividad5 import Logger
import tkinter as tk
from PIL import Image, ImageTk #pip install pillow
import tkinter.font as font
from tkinter import ttk
import cv2 #pip install opencv-python
import camera_actividad5
import numpy as np

class Application(ttk.Frame):
    def __init__(self, master=None): #Todo lo gráfico irá en el master
        super().__init__(master)
        # variables globales:
        self.logReport = Logger("logGUI")
        self.logReport.logger.info("init GUI")
        self.frame = None
        self.imgTk = None # Video 1
        self.imgTk2 = None # Video 2
        self.master = master

        # Resolución o tamaño de la imagen:
        self.width = 1080 
        self.height = 720
        self.master.geometry("%dx%d" % (self.width, self.height))
        
        self.widgetText("Piezas identificadas", 550, 10) # Texto
        self.createFrame(2, 550, 30, 500, 500) # Recuadro para la pieza contada
        self.widgetText("Video_1_12", 10, 10) # Texto
        self.createButton()
        self.createFrame(1, 10, 30, 500, 500) # Recuadro para el video
        self.widgetText("Grupo 8: ", 500, 550) # Texto
        self.widgetText("Grupo O: ", 500, 580) # Texto

        self.master.mainloop()
    
    def createFrame(self, video, xpos, ypos, width, height): # Video
        if(video==1):
            self.labelVideo_1 = tk.Label(
                self.master,
                borderwidth = 2,
                relief="solid" #Borde continuo
            )
            self.labelVideo_1.place(x=xpos, y=ypos)
            self.createImageZeros(1, width, height) #Imagen de ceros negra
            self.labelVideo_1.configure(image=self.imgTk) #Imágenes a color del mismo tamaño de imgTk
            self.labelVideo_1.image = self.imgTk
        else:
            self.labelVideo_2 = tk.Label(
                self.master,
                borderwidth = 2,
                relief="solid" #Borde continuo
            )
            self.labelVideo_2.place(x=xpos, y=ypos)
            self.createImageZeros(2, width, height) #Imagen de ceros negra
            self.labelVideo_2.configure(image=self.imgTk2) #Imágenes a color del mismo tamaño de imgTk
            self.labelVideo_2.image = self.imgTk2
    
    def createImageZeros(self, video, w, h):
        self.frame = np.zeros([h, w, 3], dtype=np.uint8)  # imagen negra
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        imgArray = Image.fromarray(self.frame)
        if video == 1:
            self.imgTk = ImageTk.PhotoImage(image=imgArray)
        else:
            self.imgTk2 = ImageTk.PhotoImage(image=imgArray)
    
    def widgetText(self, title, xpos, ypos):
        self.fontLabelText = font.Font(
            family='Helvetica', size = 10, weight = 'bold' #Fuente para el texto
        )
        self.labelNameCamera = tk.Label(
            self.master, text = title, fg = '#000000'
        )
        self.labelNameCamera['font'] = self.fontLabelText
        self.labelNameCamera.place(x=xpos, y=ypos)

    def createButton(self):
        # Botones:
        self.btnInitCamera = tk.Button(
            self.master,
            text="Start",
            bg = '#007A39',
            fg = '#ffffff',
            width = 12,
            command = self.initCamera
        )
        self.btnInitCamera.place(x=100, y=600) #Lugar del botón dependiendo del tamaño de la resolución dada width and height

        # self.btnInitCamera = tk.Button(
        #     self.master,
        #     text="Stop",
        #     bg = "#7A0000",
        #     fg = '#ffffff',
        #     width = 12,
        #     command = self.initCameraStop
        # )
        # self.btnInitCamera.place(x=200, y=600)

    def initCamera(self):
        self.camera_1 = camera_actividad5.RunCamera(r"C:\Users\varga\OneDrive - Universidad EIA\Documents\Universidad EIA\Sexto Semestre\Vision_Artificial-Electiva\VA_Codes\GUI\Actividad5\video_1_12.avi") # Ruta del video, () se obtiene la cámara por defecto
        self.camera_1.start() #start de camera_actividad5.py
        self.showVideo()
        print("Start Camera 1")
    
        
    def showVideo(self): #Actualiza cada frame para mostrar video continuo
        if(self.camera_1.frame is not None):
            imgresize =cv2.resize(self.camera_1.frame, (500, 500))
            imgTk = self.convertToFrameTk(1, imgresize) # Ventana convertida a Tkinter 
            self.labelVideo_1.configure(image=imgTk) #Imágenes a color del mismo tamaño de imgTk
            self.labelVideo_1.image = imgTk

            imgresize2 =cv2.resize(self.camera_1.mask, (500, 500))
            imgTk2 = self.convertToFrameTk(2, imgresize2) # Ventana Binary convertida a Tkinter 
            self.labelVideo_2.configure(image=imgTk2) #Imágenes a color del mismo tamaño de imgTk2
            self.labelVideo_2.image = imgTk2

            self.widgetText(self.camera_1.count_g8, 600, 550) # Variable de cantidad de piezas 8
            self.widgetText(self.camera_1.count_go, 600, 580) # Variable de cantidad de piezas O 
        
        self.after(1, self.showVideo) #Para actualizarse cada 1ms
            
    
    def convertToFrameTk(self, img, frame): #1, BGR; 2, Binary and GrayScale
        if(img==1):    
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Tkinter solo recibe imágenes en RGB
            imgArray = Image.fromarray(frame) #Y Tkinter lo tiene como un array
        else:
            framebin = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)  # Tkinter solo recibe imágenes en RGB
            imgArray = Image.fromarray(framebin) #Y Tkinter lo tiene como un array
        return ImageTk.PhotoImage(image = imgArray)
    
def main():
    root = tk.Tk()
    root.title("GUI CAMERA")
    appRunCamera = Application(master=root)
