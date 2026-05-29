"""
Don't stop at accuracy. For imbalanced datasets, precision/recall/F1
are far more informative. Always look at the confusion matrix first.
"""
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X = np.array([
    [2, 5], [3, 6], [5, 5], [8, 7],
    [1, 4], [6, 8], [7, 7], [4, 6],
])
y = np.array([0, 0, 0, 1, 0, 1, 1, 1])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, predictions))
print("Precision:", precision_score(y_test, predictions, zero_division=0))
print("Recall:", recall_score(y_test, predictions, zero_division=0))
print("F1:", f1_score(y_test, predictions, zero_division=0))
print("AUC-ROC:", roc_auc_score(y_test, probabilities))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))
#          predicted 0  predicted 1
# actual 0     TN           FP
# actual 1     FN           TP

print("\nFull Report:")
print(classification_report(y_test, predictions, zero_division=0))
