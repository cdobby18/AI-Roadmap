from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

X = [[15,39],[16,81],[17,6],[18,77],[19,40],
     [20,90],[70,30],[75,10],[80,20],[85,95]]

inertia = []

for k in range(1, 10):
    model = KMeans(n_clusters=k, random_state=42)
    model.fit(X)
    inertia.append(model.inertia_)

plt.plot(range(1,10), inertia)
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.title("Elbow Method")
plt.show()