import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Features: [age, income] — Label: approved (1) / denied (0)
X = np.array([
    [25, 50000], [35, 65000], [45, 80000],
    [20, 20000], [30, 40000], [50, 90000],
])
y = np.array([0, 1, 1, 0, 0, 1])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print("Predictions:", predictions)
print("Accuracy:", accuracy_score(y_test, predictions))
