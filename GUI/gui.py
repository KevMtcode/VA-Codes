from logger import Logger
import tkinter as tk
from PIL import Image, ImageTk #pip install pillow
import tkinter.font as font
from tkinter import ttk
import cv2 #pip install opencv-python
import camera 
import numpy as np

class Application(ttk.Frame):
    def __init__(self, master=None): #Todo lo gráfico irá en el master
        super().__init__(master)
        # variables globales:
        self.logReport = Logger("logGUI")
        self.logReport.logger.info("init GUI")
        self.frame = None
        self.imgTk = None
        self.master = master

        # Resolución o tamaño de la imagen:
        self.width = 1080 
        self.height = 720
        self.master.geometry("%dx%d" % (self.width, self.height))
        
        self.createWidgets() # Crear Widgets
        self.createFrame(10, 30, 320, 480) # Recuadro para la cámara

        self.master.mainloop()
    
    def createFrame(self, xpos, ypos, width, height): # Video
        self.labelVideo_1 = tk.Label(
            self.master,
            borderwidth = 2,
            relief="solid" #Borde continuo
        )
        self.labelVideo_1.place(x=xpos, y=ypos)
        self.createImageZeros(width, height) #Imagen de ceros negra
        self.labelVideo_1.configure(image=self.imgTk) #Imágenes a color del mismo tamaño de imgTk
        self.labelVideo_1.image = self.imgTk
    
    def createImageZeros(self, w, h):
        self.frame = np.zeros([h, w, 3], dtype=np.uint8)
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  # Tkinter solo recibe imágenes en RGB
        imgArray = Image.fromarray(self.frame)
        self.imgTk = ImageTk.PhotoImage(image = imgArray)

    def createWidgets(self):
        # Título:
        self.fontLabelText = font.Font(
            family='Helvetica', size = 8, weight = 'bold' #Fuente para el texto
        )
        self.labelNameCamera = tk.Label(
            self.master, text = "Camera 1", fg = '#000000'
        )
        self.labelNameCamera['font'] = self.fontLabelText
        self.labelNameCamera.place(x=10, y=10)

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

        self.btnInitCamera = tk.Button(
            self.master,
            text="Stop",
            bg = "#7A0000",
            fg = '#ffffff',
            width = 12,
            command = self.initCameraStop
        )
        self.btnInitCamera.place(x=200, y=600)

    def initCamera(self):
        self.camera_1 = camera.RunCamera() # Ruta del video, () se obtiene la cámara por defecto
        self.camera_1.start() #start de camera.py
        self.showVideo()
        print("Start Camera 1")
    
    def showVideo(self):
        if(self.camera_1.frame is not None):
            imgTk = self.convertToFrameTk(self.camera_1.frame) # Ventana convertida a Tkinter 
            self.labelVideo_1.configure(image=imgTk) #Imágenes a color del mismo tamaño de imgTk
            self.labelVideo_1.image = imgTk
        self.labelVideo_1.after(1, self.showVideo) #Para actualizarse cada 1ms y mostrar video continuo
            
    
    def convertToFrameTk(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Tkinter solo recibe imágenes en RGB
        imgArray = Image.fromarray(frame) #Y Tkinter lo tiene como un array
        return ImageTk.PhotoImage(image = imgArray)


    def initCameraStop(self):
        print("Stop Camera 1")


def main():
    root = tk.Tk()
    root.title("GUI CAMERA")
    appRunCamera = Application(master=root)

