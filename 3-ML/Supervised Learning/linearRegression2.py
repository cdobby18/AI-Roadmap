import numpy as np

# Dataset
X = np.array([50, 60, 80, 100, 120])
y = np.array([100000, 120000, 160000, 200000, 240000])

# Initialize parameters
w = 0
b = 0

learning_rate = 0.0001
epochs = 1000
n = len(X)

for i in range(epochs):

    y_pred = w * X + b

    dw = (-2/n) * np.sum(X * (y - y_pred))
    db = (-2/n) * np.sum(y - y_pred)

    w = w - learning_rate * dw
    b = b - learning_rate * db

print("Weight:", w)
print("Bias:", b)

predictions = w * X + b
print("Predictions:", predictions)