from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import numpy as np

X = np.array([
    [2,3],
    [3,4],
    [5,6],
    [7,8],
    [1,1],
    [8,9]
])

y = np.array([0,0,1,1,0,1])

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

model = SVC(kernel='linear')

model.fit(X_train,y_train)

prediction = model.predict([[4,5]])

print("Prediction:",prediction)