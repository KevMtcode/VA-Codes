import cv2
import numpy as np
from glob import glob
import xlsxwriter

vector_folders_nums = ['Ant_izq', 'Ant_der', 'Colm_izq', 'Colm_der', 'Cen_izq', 'Cen_der'] # Al usar varias carpetas
row = 0
col = 1
workbook = xlsxwriter.Workbook('caractNums_video.xlsx')
worksheet = workbook.add_worksheet('caracts_video') #Características
vector_caracts = np.array([])

def binarizeImg(imgGray):
    return cv2.inRange(imgGray, 0, 100)

def extractContours(imgBinary):
    cnt = []
    contours, _ = cv2.findContours(imgBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    big_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]

    if len(big_contours) == 0:
        return None
    return big_contours[0]

def extractPatterns(imgRoiBin, cnt, width, height): #Extraer Patrones o características
    x1_area = cv2.contourArea(cnt)
    x2_perimeter = cv2.arcLength(cnt, True)
    x3_circularity = x1_area/x2_perimeter**2
    M = cv2.moments(cnt) #Momentos
    Hu = cv2.HuMoments(M) #Momentos de Hu
    Hu = -np.sign(Hu) * np.log10(np.abs(Hu)) #Normalización logarítmica de los momentos de Hu para estabilidad
    x4 = Hu[0][0]
    x5 = Hu[1][0]
    x6 = Hu[2][0]
    x7 = Hu[3][0]
    x8 = Hu[4][0]
    x9 = Hu[5][0]
    x10 = Hu[6][0]

    #Roi: extraer densidades de pixeles en posiciones X y Y
    roi_1 = imgRoiBin[0:10, 0:10] #0 hasta 10 en X y Y como los "pedazos" a analizar de la imagen
    x11 = cv2.countNonZero(roi_1)/100  #se divide entre el área elegida de "pedazos"(diferencia intervalo*diferencia intervalo) ; Se puede hacer más patrones de estos con for para recorrer toda la imagen
    roi_1 = imgRoiBin[0:20, 0:20] 
    x12 = cv2.countNonZero(roi_1)/400
    roi_1 = imgRoiBin[20:40, 30:50] 
    x13 = cv2.countNonZero(roi_1)/400
    roi_1 = imgRoiBin[20:40, 20:40] 
    x14 = cv2.countNonZero(roi_1)/400
    roi_1 = imgRoiBin[10:30, 0:20] 
    x15 = cv2.countNonZero(roi_1)/400
    roi_1 = imgRoiBin[0:30, 20:50] 
    x16 = cv2.countNonZero(roi_1)/900
    roi_1 = imgRoiBin[10:30, 20:40] 
    x17 = cv2.countNonZero(roi_1)/400
    roi_1 = imgRoiBin[10:30, 10:30] 
    x20 = cv2.countNonZero(roi_1)/400
    
    x18 = width/100
    x19 = height/100
    x21 = width/height
    x22 = cv2.contourArea(cnt) / (width * height)

    list_carac = [x1_area, x2_perimeter, x3_circularity, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22]
    features = np.array(list_carac, dtype = np.float32) #Volver la lista dato tipo float
    return features
    
def extractCaracts(): # Obtención de las características de imágenes de varias carpetas a archivo Excel 
    global row, col, vector_caracts
    for n in range(0, len(vector_folders_nums)):
        pathVideo = "MachineLearning/Lab3y4videos/"+vector_folders_nums[n]+"*.mp4"
        for imgPath in glob(pathVideo): #videos
            print("Grabando video: ", imgPath)
            capture = cv2.VideoCapture(imgPath)
            ret, frame = capture.read() 
            while capture.isOpened():
                ret, frame = capture.read() #Imágenes en el video
                #NO puede haber algo antes de if not ret, porque luego no detecta frame
                if not ret: #Si esto es verdad, es porque no encuentra video o ya se acabó
                    print("No se puede recibir el frame. Saliendo...")
                    break
                imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                imgBinary = binarizeImg(imgGray)
                imgBinaryInv = cv2.bitwise_not(imgBinary)
                cnt = extractContours(imgBinaryInv)
                if cnt is not None:
                    x,y,w,h = cv2.boundingRect(cnt)
                    if x < 50 or x+h > (imgBinary.shape[1]-50):
                        continue
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3) #Rectángulo color azul y espesor 3
                    cv2.imshow("imgColor", cv2.resize(frame, (302, 240)))
                    cv2.waitKey(1)
                    imgRoiBin = imgBinaryInv[y:y+h, x:x+w] #y hasta y+h, x hasta x+w
                    imgRoiBin = cv2.copyMakeBorder(imgRoiBin, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value = 0) #borde simétrico
                    imgWidth = imgRoiBin.shape[1]
                    imgHeight = imgRoiBin.shape[0]
                    imgRoiBin = cv2.resize(imgRoiBin, (40, 60)) #Todas las imágenes en el mismo tamaño o resolución
                    vector_caracts = extractPatterns(imgRoiBin, cnt, width=imgWidth, height=imgHeight)
                    for caract in vector_caracts: #Guardar datos en la hoja de excel
                        worksheet.write(row, 0, n)
                        worksheet.write(row, col, caract) 
                        col+=1 #todas las columnas
                    col = 1
                    row+=1 #Nuevo fila
                cv2.imshow("imgBinary", cv2.resize(imgBinaryInv, (302, 240)))
                cv2.waitKey(1)
    cv2.destroyAllWindows()
    workbook.close()
    print("Finsih extract caracts")

extractCaracts()