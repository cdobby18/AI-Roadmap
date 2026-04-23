from sklearn.cluster import KMeans
import numpy as np

# Dataset: [income, spending score]
X = np.array([
    [15, 39],
    [16, 81],
    [17, 6],
    [18, 77],
    [19, 40],
    [20, 90],
    [70, 30],
    [75, 10],
    [80, 20],
    [85, 95]
])

model = KMeans(n_clusters=2, random_state=42)

model.fit(X)

labels = model.labels_
centroids = model.cluster_centers_

print("Cluster labels:", labels)
print("Centroids:", centroids)