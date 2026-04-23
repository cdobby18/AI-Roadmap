from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
import numpy as np

# Dataset: [study_hours, sleep_hours]
X = np.array([
    [2,5],
    [3,6],
    [5,5],
    [8,7],
    [1,4],
    [6,8],
    [7,7],
    [4,6]
])

# Pass or Fail
y = np.array([0,0,0,1,0,1,1,1])

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)

model = LogisticRegression()

model.fit(X_train,y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test,predictions)
precision = precision_score(y_test,predictions)
recall = recall_score(y_test,predictions)

print("Predictions:",predictions)
print("Accuracy:",accuracy)
print("Precision:",precision)
print("Recall:",recall)