import numpy as np

y_true = np.array([3,5,7])

y_pred = np.array([2.5,5.5,6])

loss = np.mean((y_true - y_pred)**2)

print(loss)