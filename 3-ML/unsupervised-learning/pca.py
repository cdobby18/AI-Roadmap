from sklearn.decomposition import PCA
import numpy as np

X = np.array([
    [2.5, 2.4],
    [0.5, 0.7],
    [2.2, 2.9],
    [1.9, 2.2],
    [3.1, 3.0],
    [2.3, 2.7]
])

pca = PCA(n_components=1)

X_reduced = pca.fit_transform(X)

print("Reduced Data:", X_reduced)

X = np.array([
    [2.5, 2.4],
    [0.5, 0.7],
    [2.2, 2.9],
    [1.9, 2.2],
    [3.1, 3.0],
    [2.3, 2.7]
])

pca = PCA()

pca.fit(X)

print("Explained Variance Ratio:", pca.explained_variance_ratio_)