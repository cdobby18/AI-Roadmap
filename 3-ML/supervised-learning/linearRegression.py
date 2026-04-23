import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Dataset
house_size = np.array([50, 60, 80, 100, 120]).reshape(-1,1)
house_price = np.array([100000, 120000, 160000, 200000, 240000])

# Create model
model = LinearRegression()

# Train model
model.fit(house_size, house_price)

# Predict prices
predictions = model.predict(house_size)

# Evaluate model
mse = mean_squared_error(house_price, predictions)

print("Predictions:", predictions)
print("Slope:", model.coef_)
print("Intercept:", model.intercept_)
print("MSE:", mse)