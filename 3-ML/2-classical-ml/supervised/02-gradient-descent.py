"""
Linear regression implemented manually with gradient descent.
Useful for understanding what sklearn does under the hood.
"""
import numpy as np

X = np.array([50, 60, 80, 100, 120])
y = np.array([100000, 120000, 160000, 200000, 240000])

w = 0
b = 0
learning_rate = 0.0001
epochs = 1000
n = len(X)

for _ in range(epochs):
    y_pred = w * X + b
    dw = (-2 / n) * np.sum(X * (y - y_pred))
    db = (-2 / n) * np.sum(y - y_pred)
    w -= learning_rate * dw
    b -= learning_rate * db

print("Weight:", w)
print("Bias:", b)
print("Predictions:", w * X + b)
