from sklearn.preprocessing import StandardScaler
import numpy as np

X = np.array([
    [10, 1000],
    [20, 1500],
    [30, 2000],
    [40, 2500]
])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(X_scaled)