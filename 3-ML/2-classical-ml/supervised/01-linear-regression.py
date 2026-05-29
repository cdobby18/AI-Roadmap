import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Dataset: house size → price
X = np.array([50, 60, 80, 100, 120]).reshape(-1, 1)
y = np.array([100000, 120000, 160000, 200000, 240000])

model = LinearRegression()
model.fit(X, y)

predictions = model.predict(X)
mse = mean_squared_error(y, predictions)

print("Predictions:", predictions)
print("Slope:", model.coef_)
print("Intercept:", model.intercept_)
print("MSE:", mse)
