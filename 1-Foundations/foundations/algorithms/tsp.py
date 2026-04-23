# EASY
from itertools import permutations

cities = ['A','B','C']

dist = {
('A','B'):2,
('A','C'):3,
('B','A'):2,
('B','C'):4,
('C','A'):3,
('C','B'):4
}

min_path=None
min_cost=float('inf')

for perm in permutations(cities):

    cost=0

    for i in range(len(perm)-1):
        cost += dist[(perm[i],perm[i+1])]

    cost += dist[(perm[-1],perm[0])]

    if cost < min_cost:
        min_cost = cost
        min_path = perm

print(min_path,min_cost)

# MEDIUM
def tsp_nearest_neighbor(graph,start):

    visited=[start]
    current=start
    total_cost=0

    while len(visited)<len(graph):

        nearest=None
        min_dist=float('inf')

        for city,dist in graph[current].items():

            if city not in visited and dist < min_dist:
                nearest=city
                min_dist=dist

        visited.append(nearest)
        total_cost+=min_dist
        current=nearest

    total_cost += graph[current][start]

    return visited,total_cost

# HARD
from functools import lru_cache

def tsp_dp(dist):

    n=len(dist)

    @lru_cache(None)
    def visit(mask,pos):

        if mask==(1<<n)-1:
            return dist[pos][0]

        ans=float('inf')

        for city in range(n):

            if mask & (1<<city)==0:

                new_cost = dist[pos][city] + visit(mask | (1<<city), city)

                ans=min(ans,new_cost)

        return ans

    return visit(1,0)