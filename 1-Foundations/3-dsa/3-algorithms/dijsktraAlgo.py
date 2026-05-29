# EASY
import heapq

graph = {
0: [(1,4),(2,2)],
1: [(0,4),(2,1),(3,5)],
2: [(0,2),(1,1),(3,8)],
3: [(1,5),(2,8)]
}

def dijkstra(graph,start):

    distances = {node:float('inf') for node in graph}
    distances[start] = 0

    pq = [(0,start)]

    while pq:

        current_distance,node = heapq.heappop(pq)

        for neighbor,weight in graph[node]:

            distance = current_distance + weight

            if distance < distances[neighbor]:

                distances[neighbor] = distance
                heapq.heappush(pq,(distance,neighbor))

    return distances

print(dijkstra(graph,0))

# MEDIUM 
import heapq

def dijkstra_path(graph,start):

    distances={node:float('inf') for node in graph}
    previous={node:None for node in graph}

    distances[start]=0

    pq=[(0,start)]

    while pq:

        dist,node=heapq.heappop(pq)

        for neighbor,weight in graph[node]:

            new_dist=dist+weight

            if new_dist<distances[neighbor]:

                distances[neighbor]=new_dist
                previous[neighbor]=node

                heapq.heappush(pq,(new_dist,neighbor))

    return distances,previous

# HARD
import heapq

def shortest_path(graph,start,end):

    pq=[(0,start,[])]

    visited=set()

    while pq:

        cost,node,path=heapq.heappop(pq)

        if node in visited:
            continue

        path=path+[node]

        if node==end:
            return cost,path

        visited.add(node)

        for neighbor,weight in graph[node]:

            if neighbor not in visited:
                heapq.heappush(pq,(cost+weight,neighbor,path))