# EASY
import heapq

heap = []

heapq.heappush(heap, 10)
heapq.heappush(heap, 5)
heapq.heappush(heap, 20)
heapq.heappush(heap, 3)

print("Heap:", heap)

smallest = heapq.heappop(heap)

print("Smallest element:", smallest)
print("Heap after removal:", heap)

# MEDIUM
import heapq

numbers = [4,10,3,5,1,8,12,7]

largest = heapq.nlargest(3, numbers)

print("3 largest numbers:", largest)

# HARD
import heapq

tasks = []

heapq.heappush(tasks, (2,"Write report"))
heapq.heappush(tasks, (1,"Fix critical bug"))
heapq.heappush(tasks, (3,"Email client"))

while tasks:
    task = heapq.heappop(tasks)
    print("Processing:", task[1])