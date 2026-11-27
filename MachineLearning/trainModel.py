import cv2
import pandas as pd
#pip install scikit-learn openpypxl
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score
    
df = pd.read_excel('caractNums.xlsx', header=None, engine = 'openpyxl')
y = df.iloc[:, 0] #Todas las filas, primera columna
x = df.iloc[:, 1:] #Todas las filas, columna 1 hasta las demás columnas
#70% de los datos para train, 30% para test; si son pocos datos, 90% de los datos para train, 10% para test
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42) #random_state como semilla
model_mlp = MLPClassifier(hidden_layer_sizes=(10, 50, 20), max_iter=1000, activation='relu') #layers para las neuronas, iteraciones hasta encontrar el mínimo error
model_mlp.fit(x_train, y_train)

y_predict = model_mlp.predict(x_test)

print("accuracy: ", accuracy_score(y_test, y_predict))
print(classification_report(y_test, y_predict))

 
