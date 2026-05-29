import numpy as np
from sklearn.cluster import KMeans

# Features: [income, spending score]
X = np.array([
    [15, 39], [16, 81], [17, 6], [18, 77], [19, 40],
    [20, 90], [70, 30], [75, 10], [80, 20], [85, 95],
])

model = KMeans(n_clusters=2, random_state=42)
model.fit(X)

print("Cluster labels:", model.labels_)
print("Centroids:", model.cluster_centers_)
