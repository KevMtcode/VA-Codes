import cv2
import numpy as np
from glob import glob
import xlsxwriter

vector_folders_nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] # Al usar varias carpetas
row = 0
col = 1
workbook = xlsxwriter.Workbook('caractNums.xlsx')
worksheet = workbook.add_worksheet('caracts') #Características
vector_caracts = np.array([])

def binarizeImg(imgGray):
    return cv2.inRange(imgGray, 0, 127)

def extractContours(imgBinary):
    cnt = []
    contours, _ = cv2.findContours(imgBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0: #Para filtrar puntos extraños
        cnt = max(contours, key = cv2.contourArea)
        if cv2.contourArea(cnt) > 100:
            return cnt 
        else:
            return []
    return cnt

def extractPatterns(imgRoiBin, cnt): #Extraer Patrones o características
    x1_area = cv2.contourArea(cnt)
    x2_perimeter = cv2.arcLength(cnt, True)
    x3_circularity = x1_area/x2_perimeter**2
    M = cv2.moments(cnt) #Momentos
    Hu = cv2.HuMoments(M) #Momentos de Hu
    x4 = Hu[0][0]
    x5 = Hu[1][0]
    x6 = Hu[2][0]
    x7 = Hu[3][0]
    x8 = Hu[4][0]
    x9 = Hu[5][0]
    x10 = Hu[6][0]

    #Roi: extraer densidades de pixeles en posiciones X y Y
    roi_1 = imgRoiBin[0:10, 0:10] #0 hasta 10 en X y Y como los "pedazos" a analizar de la imagen
    x11 = cv2.countNonZero(roi_1)/100  #se divide entre el área elegida de "pedazos"(10*10) ; Se puede hacer más patrones de estos con for para recorrer toda la imagen
    roi_1 = imgRoiBin[0:20, 0:20] 
    x12 = cv2.countNonZero(roi_1)/400
    roi_1 = imgRoiBin[0:30, 0:30] 
    x13 = cv2.countNonZero(roi_1)/900
    roi_1 = imgRoiBin[0:40, 0:40] 
    x14 = cv2.countNonZero(roi_1)/1600

    list_carac = [x1_area, x2_perimeter, x3_circularity, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14]
    features = np.array(list_carac, dtype = np.float32) #Volver la lista dato tipo float
    return features
    
def extractCaracts(): # Obtención de las características de imágenes de varias carpetas a archivo Excel 
    global row, col, vector_caracts
    for n in range(0, len(vector_folders_nums)):
        for imgPath in glob("MachineLearning/num/"+vector_folders_nums[n]+"/*.png"): #archivos png
            imgGray = cv2.imread(imgPath, 0)
            imgColor = cv2.imread(imgPath, 1)
            imgBinary = binarizeImg(imgGray)
            cnt = extractContours(imgBinary)
            if len(cnt) > 0:
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(imgColor, (x, y), (x+w, y+h), (255, 0, 0), 3) #Rectángulo color azul y espesor 3
                cv2.imshow("imgColor", cv2.resize(imgColor, (302, 240)))
                cv2.waitKey(1)
                imgRoiBin = imgBinary[y:y+h, x:x+w] #y hasta y+h, x hasta x+w
                imgRoiBin = cv2.copyMakeBorder(imgRoiBin, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value = 0) #borde simétrico
                imgRoiBin = cv2.resize(imgRoiBin, (40, 60)) #Todas las imágenes en el mismo tamaño
                vector_caracts = extractPatterns(imgRoiBin, cnt)
                for caract in vector_caracts: #Guardar datos en la hoja de excel
                    worksheet.write(row, 0, n)
                    worksheet.write(row, col, caract) 
                    col+=1 #todas las columnas
                col = 1
                row+=1 #Nuevo fila
            cv2.imshow("imgBinary", cv2.resize(imgBinary, (302, 240)))
            cv2.waitKey(1)
    cv2.destroyAllWindows()
    workbook.close()
    print("Finsih extract caracts")

extractCaracts()