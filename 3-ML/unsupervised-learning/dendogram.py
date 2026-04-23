import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt

X = [
    [10,20],[11,22],[12,18],
    [50,60],[52,58],[55,65]
]

dendrogram = sch.dendrogram(sch.linkage(X, method='ward'))

plt.title("Dendrogram")
plt.xlabel("Data Points")
plt.ylabel("Distance")
plt.show()