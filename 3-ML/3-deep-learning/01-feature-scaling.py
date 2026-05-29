"""
Feature scaling is required before feeding data into a neural network.
Raw features on different scales (e.g. age=25, income=50000) cause
unstable training — StandardScaler fixes this.
"""
import numpy as np
from sklearn.preprocessing import StandardScaler

X = np.array([
    [10, 1000],
    [20, 1500],
    [30, 2000],
    [40, 2500],
])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Original:\n", X)
print("Scaled:\n", X_scaled)
