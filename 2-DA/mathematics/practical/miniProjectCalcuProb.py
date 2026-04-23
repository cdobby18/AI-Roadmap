import numpy as np

X = np.array([1,2,3,4,5])
y = np.array([50,55,65,70,80])

w = 0
b = 0

lr = 0.01

for epoch in range(1000):

    y_pred = w*X + b

    error = y_pred - y

    loss = np.mean(error**2)

    dw = np.mean(2*error*X)
    db = np.mean(2*error)

    w = w - lr*dw
    b = b - lr*db

print("Weight:",w)
print("Bias:",b)