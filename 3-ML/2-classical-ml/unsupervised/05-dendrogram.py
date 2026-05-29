import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch

X = [
    [10, 20], [11, 22], [12, 18],
    [50, 60], [52, 58], [55, 65],
]

sch.dendrogram(sch.linkage(X, method="ward"))

plt.title("Dendrogram — use horizontal cut to decide cluster count")
plt.xlabel("Data Points")
plt.ylabel("Distance")
plt.show()
