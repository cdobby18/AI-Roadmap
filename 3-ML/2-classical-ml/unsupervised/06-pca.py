import numpy as np
from sklearn.decomposition import PCA

X = np.array([
    [2.5, 2.4], [0.5, 0.7], [2.2, 2.9],
    [1.9, 2.2], [3.1, 3.0], [2.3, 2.7],
])

# Reduce to 1 dimension
pca = PCA(n_components=1)
X_reduced = pca.fit_transform(X)
print("Reduced data:", X_reduced)

# Check how much variance each component explains
pca_full = PCA()
pca_full.fit(X)
print("Explained variance ratio:", pca_full.explained_variance_ratio_)
