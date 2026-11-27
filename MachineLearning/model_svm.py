import cv2
import pandas as pd
#pip install scikit-learn openpypxl
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

df = pd.read_excel('caractNums.xlsx', header=None, engine = 'openpyxl')
y = df.iloc[:, 0] #Todas las filas, primera columna
x = df.iloc[:, 1:] #Todas las filas, columna 1 hasta las demás columnas

scaler = StandardScaler()
x_s = scaler.fit_transform(x) #datos escalados, para mejor accuracy

x_train, x_test, y_train, y_test = train_test_split(x_s, y, test_size=0.1, random_state=42)

model_svm = SVC(kernel='rbf', C=1.0)
model_svm.fit(x_train, y_train)
y_predict = model_svm.predict(x_test)
print("accuracy: ", accuracy_score(y_test, y_predict))
print(classification_report(y_test, y_predict, zero_division=0))