import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

# Features: [study_hours, sleep_hours] — Label: pass (1) / fail (0)
X = np.array([
    [2, 5], [3, 6], [5, 5], [8, 7],
    [1, 4], [6, 8], [7, 7], [4, 6],
])
y = np.array([0, 0, 0, 1, 0, 1, 1, 1])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Predictions:", predictions)
print("Accuracy:", accuracy_score(y_test, predictions))
print("Precision:", precision_score(y_test, predictions, zero_division=0))
print("Recall:", recall_score(y_test, predictions, zero_division=0))
