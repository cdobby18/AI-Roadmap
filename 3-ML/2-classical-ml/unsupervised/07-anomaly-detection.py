import numpy as np
from sklearn.ensemble import IsolationForest

X = np.array([[10], [12], [11], [13], [100], [9]])  # 100 is the anomaly

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)

predictions = model.predict(X)  # 1 = normal, -1 = anomaly
anomalies = X[predictions == -1]

print("Predictions:", predictions)
print("Anomalies detected:", anomalies)
