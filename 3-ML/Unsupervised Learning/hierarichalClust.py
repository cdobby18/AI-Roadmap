from sklearn.cluster import AgglomerativeClustering
import numpy as np

X = np.array([
    [10,20],
    [11,22],
    [12,18],
    [50,60],
    [52,58],
    [55,65]
])

model = AgglomerativeClustering(n_clusters=2)

labels = model.fit_predict(X)

print("Cluster labels:", labels)