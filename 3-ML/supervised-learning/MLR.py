import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Dataset: [size, bedrooms, age]
X = np.array([
    [50, 1, 10],
    [80, 2, 5],
    [100, 3, 7],
    [120, 3, 3],
    [150, 4, 1]
])

y = np.array([100000, 160000, 180000, 220000, 300000])

# Model
model = LinearRegression()

# Train
model.fit(X, y)

# Predictions
predictions = model.predict(X)

# Metrics
mae = mean_absolute_error(y, predictions)
mse = mean_squared_error(y, predictions)
rmse = np.sqrt(mse)
r2 = r2_score(y, predictions)

print("Predictions:", predictions)
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2 Score:", r2)