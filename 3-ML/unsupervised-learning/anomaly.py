from sklearn.ensemble import IsolationForest
import numpy as np

X = np.array([
    [10],
    [12],
    [11],
    [13],
    [100],  # anomaly
    [9]
])

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)

pred = model.predict(X)

print("Predictions:", pred)

Y = np.array([
    [100],
    [120],
    [110],
    [115],
    [10],   # anomaly
    [12]
])

model = IsolationForest(contamination=0.2, random_state=42)
model.fit(X)

pred = model.predict(Y)

anomalies = Y[pred == -1]

print("Anomalies:", anomalies)