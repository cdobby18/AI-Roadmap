# EASY
edges = [
("A","B",1),
("A","C",3),
("B","C",2)
]

edges.sort(key=lambda x: x[2])

mst = []

for edge in edges:
    mst.append(edge)

print(mst)

#MEDIUM
class UnionFind:

    def __init__(self,n):
        self.parent=list(range(n))

    def find(self,x):
        if self.parent[x]!=x:
            self.parent[x]=self.find(self.parent[x])
        return self.parent[x]

    def union(self,x,y):
        rootX=self.find(x)
        rootY=self.find(y)
        if rootX!=rootY:
            self.parent[rootY]=rootX

edges = [
(0,1,4),
(0,2,3),
(1,2,1),
(1,3,2),
(2,3,4)
]

edges.sort(key=lambda x:x[2])

uf=UnionFind(4)
mst=[]

for u,v,w in edges:

    if uf.find(u)!=uf.find(v):
        uf.union(u,v)
        mst.append((u,v,w))

print(mst)

# HARD
edges = [
(0,1,10),
(0,2,6),
(0,3,5),
(1,3,15),
(2,3,4)
]

edges.sort(key=lambda x:x[2])

uf = UnionFind(4)
cost = 0

for u,v,w in edges:
    if uf.find(u)!=uf.find(v):
        uf.union(u,v)
        cost += w

print(cost)