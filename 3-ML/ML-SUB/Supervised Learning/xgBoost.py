from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import numpy as np

X = np.array([
    [25,50000],
    [35,65000],
    [45,80000],
    [20,20000],
    [30,40000],
    [50,90000]
])

y = np.array([0,1,1,0,0,1])

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)

model = XGBClassifier()

model.fit(X_train,y_train)

prediction = model.predict([[40,70000]])

print("Prediction:",prediction)