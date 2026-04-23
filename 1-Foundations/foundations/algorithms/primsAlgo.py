# EASY
import heapq

graph = {
0: [(1,2),(3,6)],
1: [(0,2),(2,3),(3,8),(4,5)],
2: [(1,3),(4,7)],
3: [(0,6),(1,8)],
4: [(1,5),(2,7)]
}

visited=set()

pq=[(0,0)]

cost=0

while pq:

    weight,node=heapq.heappop(pq)

    if node in visited:
        continue

    visited.add(node)

    cost+=weight

    for neighbor,w in graph[node]:
        if neighbor not in visited:
            heapq.heappush(pq,(w,neighbor))

print(cost)

# MEDIUM 
import heapq

graph = [
[0,2,0,6,0],
[2,0,3,8,5],
[0,3,0,0,7],
[6,8,0,0,9],
[0,5,7,9,0]
]

n=len(graph)

visited=[False]*n

pq=[(0,0)]

cost=0

while pq:

    weight,node=heapq.heappop(pq)

    if visited[node]:
        continue

    visited[node]=True
    cost+=weight

    for neighbor in range(n):
        if graph[node][neighbor]!=0 and not visited[neighbor]:
            heapq.heappush(pq,(graph[node][neighbor],neighbor))

print(cost)

# HARD
import heapq

def prim(graph,start):

    visited=set()

    pq=[(0,start,-1)]

    mst=[]

    while pq:

        weight,node,parent = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)

        if parent!=-1:
            mst.append((parent,node,weight))

        for neighbor,w in graph[node]:
            if neighbor not in visited:
                heapq.heappush(pq,(w,neighbor,node))

    return mst