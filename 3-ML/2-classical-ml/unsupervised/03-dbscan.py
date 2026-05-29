import numpy as np
from sklearn.cluster import DBSCAN

# Noise point is far away from clusters
X = np.array([
    [1, 2], [2, 2], [2, 3],
    [8, 7], [8, 8],
    [25, 80],  # noise
])

model = DBSCAN(eps=3, min_samples=2)
labels = model.fit_predict(X)

print("Cluster labels:", labels)   # -1 means noise
print("Noise points:", X[labels == -1])
