from sklearn.cluster import DBSCAN
import numpy as np

X = np.array([
    [1,2],
    [2,2],
    [2,3],
    [8,7],
    [8,8],
    [25,80]  # noise point
])

model = DBSCAN(eps=3, min_samples=2)
labels = model.fit_predict(X)

print("Cluster labels:", labels)

Y = np.array([
    [10,10],
    [11,11],
    [12,12],
    [50,50],  # anomaly
    [51,51]
])

model = DBSCAN(eps=5, min_samples=2)
labels = model.fit_predict(Y)

anomalies = Y[labels == -1]

print("Anomalies detected:", anomalies)