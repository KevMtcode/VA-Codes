from logger_parcial import Logger
import tkinter as tk
from PIL import Image, ImageTk #pip install pillow
import tkinter.font as font
from tkinter import ttk
import cv2 #pip install opencv-python
import classifier
import numpy as np

class Application(ttk.Frame):
    def __init__(self, master=None): #Todo lo gráfico irá en el master
        super().__init__(master)
        # variables globales:
        self.logReport = Logger("logGUI")
        self.logReport.logger.info("init GUI")
        self.frame = None
        self.imgTk = None # Video
        self.imgTk2 = None # Imagen pieza perforada
        self.imgTk3 = None # Imagen pieza no perforada
        self.imgTk4 = None # Imagen pieza mal fabricada
        self.master = master

        # Resolución o tamaño de la imagen:
        self.width = 1080 
        self.height = 720
        self.master.geometry("%dx%d" % (self.width, self.height))
        
        self.widgetText("Video_2", 10, 450) # Texto
        self.createFrame(1, 10, 30, 450, 400) 
        self.createButton(150, 500)
        self.widgetText("Piezas perforadas", 480, 30) 
        self.createFrame(2, 480, 50, 150, 150)
        self.widgetText("Cantidad:", 500, 210)
        self.widgetText("Piezas no perforadas", 690, 30) 
        self.createFrame(3, 690, 50, 150, 150)
        self.widgetText("Cantidad:", 710, 210)
        self.widgetText("Piezas mal fabricadas", 900, 30) 
        self.createFrame(4, 900, 50, 150, 150)
        self.widgetText("Cantidad:", 920, 210)
        self.widgetText("Total:", 480, 300)

        self.master.mainloop() 
    
    def createFrame(self, video, xpos, ypos, width, height): # Video
        match (video):
            case 1:
                self.labelVideo_1 = tk.Label(
                    self.master,
                    borderwidth = 2,
                    relief="solid" #Borde continuo
                )
                self.labelVideo_1.place(x=xpos, y=ypos)
                self.createImageZeros(1, width, height) #Imagen de ceros negra
                self.labelVideo_1.configure(image=self.imgTk) #Imágenes a color del mismo tamaño de imgTk
                self.labelVideo_1.image = self.imgTk
            case 2:
                self.labelVideo_2 = tk.Label(
                    self.master,
                    borderwidth = 2,
                    relief="solid" #Borde continuo
                )
                self.labelVideo_2.place(x=xpos, y=ypos)
                self.createImageZeros(2, width, height) #Imagen de ceros negra
                self.labelVideo_2.configure(image=self.imgTk2) #Imágenes a color del mismo tamaño de imgTk
                self.labelVideo_2.image = self.imgTk2
            case 3:
                self.labelVideo_3 = tk.Label(
                    self.master,
                    borderwidth = 2,
                    relief="solid" #Borde continuo
                )
                self.labelVideo_3.place(x=xpos, y=ypos)
                self.createImageZeros(3, width, height) #Imagen de ceros negra
                self.labelVideo_3.configure(image=self.imgTk3) #Imágenes a color del mismo tamaño de imgTk
                self.labelVideo_3.image = self.imgTk3
            case 4:
                self.labelVideo_4 = tk.Label(
                    self.master,
                    borderwidth = 2,
                    relief="solid" #Borde continuo
                )
                self.labelVideo_4.place(x=xpos, y=ypos)
                self.createImageZeros(4, width, height) #Imagen de ceros negra
                self.labelVideo_4.configure(image=self.imgTk4) #Imágenes a color del mismo tamaño de imgTk
                self.labelVideo_4.image = self.imgTk4
        
    
    def createImageZeros(self, video, w, h):
        self.frame = np.zeros([h, w, 3], dtype=np.uint8)  # imagen negra
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        imgArray = Image.fromarray(self.frame)
        match (video):
            case 1:
                self.imgTk = ImageTk.PhotoImage(image=imgArray)
            case 2:
                self.imgTk2 = ImageTk.PhotoImage(image=imgArray)
            case 3:
                self.imgTk3 = ImageTk.PhotoImage(image=imgArray)
            case 4:
                self.imgTk4 = ImageTk.PhotoImage(image=imgArray)
    
    def widgetText(self, title, xpos, ypos):
        self.fontLabelText = font.Font(
            family='Helvetica', size = 10, weight = 'bold' #Fuente para el texto
        )
        self.labelNameCamera = tk.Label(
            self.master, text = title, fg = '#000000'
        )
        self.labelNameCamera['font'] = self.fontLabelText
        self.labelNameCamera.place(x=xpos, y=ypos)

    def createButton(self, xpos, ypos):
        # Botones:
        self.btnInitCamera = tk.Button(
            self.master,
            text="Start",
            bg = '#007A39',
            fg = '#ffffff',
            width = 12,
            command = self.initCamera
        )
        self.btnInitCamera.place(x=xpos, y=ypos) #Lugar del botón dependiendo del tamaño de la resolución dada width and height

    def initCamera(self):
        self.Classifier_1 = classifier.Classifier(r"C:\Users\varga\OneDrive - Universidad EIA\Documents\Universidad EIA\Sexto Semestre\Vision_Artificial-Electiva\VA_Codes\ExamenParcial\video_2.mp4") # Ruta del video, () se obtiene la cámara por defecto
        self.Classifier_1.start() #start de camera_actividad5.py
        self.showVideo()
        print("Start Classifier")
    
        
    def showVideo(self): #Actualiza cada frame para mostrar video continuo
        if(self.Classifier_1.frame is not None):
            #Video:
            frame, _ = self.Classifier_1.processFrame()
            imgresize =cv2.resize(self.Classifier_1.frame, (450, 400))
            imgTk = self.convertToFrameTk(1, imgresize) # Ventana convertida a Tkinter 
            self.labelVideo_1.configure(image=imgTk)
            self.labelVideo_1.image = imgTk
            if (self.Classifier_1.frame_empacar is not None):
                #Imagen pieza perforada:
                imgresize2 =cv2.resize(self.Classifier_1.frame_empacar, (150, 150))
                imgTk2 = self.convertToFrameTk(1, imgresize2)
                self.labelVideo_2.configure(image=imgTk2) 
                self.labelVideo_2.image = imgTk2
            if (self.Classifier_1.frame_perforar is not None):
                #Imagen pieza no perforada:
                imgresize3 =cv2.resize(self.Classifier_1.frame_perforar, (150, 150))
                imgTk3 = self.convertToFrameTk(1, imgresize3)
                self.labelVideo_3.configure(image=imgTk3) 
                self.labelVideo_3.image = imgTk3
            if (self.Classifier_1.frame_refabricar is not None):
                #Imagen pieza mal fabricada:
                imgresize4 =cv2.resize(self.Classifier_1.frame_refabricar, (150, 150))
                imgTk4 = self.convertToFrameTk(1, imgresize4)
                self.labelVideo_4.configure(image=imgTk4) 
                self.labelVideo_4.image = imgTk4


            self.widgetText(self.Classifier_1.piezas_empaque, 600, 210) 
            self.widgetText(self.Classifier_1.piezas_perforado, 800, 210) 
            self.widgetText(self.Classifier_1.piezas_fabricacion, 1000, 210)
            self.widgetText(self.Classifier_1.numero_piezas, 550, 300)

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
