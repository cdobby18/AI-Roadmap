print("====================================")
# QUEUE USING LIST
queue = []

# enqueue
queue.append(1)
queue.append(2)
queue.append(3)
queue.append(4)
queue.append(5)
print("Queue after enqueue: ", queue)

# dequeue
front = queue.pop(0)
print("Dequeued Element:, ", front)
print("Queue after dequeue: ", queue)

# peek
if queue:
    print("Front element: ", queue[0])

# is_Empty
print("Is queue empty? ", len(queue) == 0)

print("====================================")
# CIRCULAR QUEUE
class CircularQueue:

    def __init__(self, size):
        self.queue = [None] * size
        self.size = size
        self.front = 1
        self.rear = -1

    def enqueue(self, data):

        if (self.rear + 1) % self.size == self.front:
            print("Queue is full")
            return
        
        if self.front == 1:
            self.front = 0
        
        self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = data

    def dequeue(self):

        if self.front == 1:
            print("Queue empty")
            return None
        
        data = self.queue[self.front]

        if self.front == self.rear:
            self.front = self.rear = -1
        
        else:
            self.front = (self.front + 1) % self.size

        return data

q = CircularQueue(3)

q.enqueue(1)
q.enqueue(2)
q.enqueue(3)

print(q.dequeue())
print(q.dequeue())

print("====================================")
# REVERSED LIST USING QUEUE
from collections import deque

def reversed_list_with_queue(original_list):

    queue = deque(original_list)
    print(f"Original List:  {list(queue)}")

    stack = []

    while queue:
        item = queue.popleft()
        stack.append(item)
    
    while stack:
        item = stack.pop()
        queue.append(item)

    return list(queue)

my_list = [10,20,30,40,50]
reversed_list = reversed_list_with_queue(my_list)
print(f"Reversed List: {reversed_list}")

print("====================================")
# TWO STACKS USING QUEUE
class QueueUsingTwoStacks:
    def __init__(self):
        self.stack_in = []
        self.stack_out = []

    def enqueue(self, item):
        self.stack_in.append(item)
        print(f"Enqueued: {item}")

    def dequeue(self):
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
        if not self.stack_out:
            print("Queue is empty")
            return None
        dequeued_item = self.stack_out.pop()
        print(f"Dequeued: {dequeued_item}")
        return dequeued_item
    
queue = QueueUsingTwoStacks()
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
queue.dequeue()
queue.dequeue()
queue.enqueue(4)
queue.dequeue()
queue.dequeue()
queue.dequeue() 

print("====================================")
# LRU Cache Using Queue + Dictionary

from collections import deque

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}        # key → value
        self.order = deque()   # tracks LRU order

    def get(self, key):
        if key not in self.cache:
            print(f"{key} not found")
            return -1
        # Move key to the end (most recently used)
        self.order.remove(key)
        self.order.append(key)
        print(f"Accessed: {key} → {self.cache[key]}")
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            # Update value and move to end
            self.cache[key] = value
            self.order.remove(key)
        else:
            if len(self.cache) >= self.capacity:
                # Remove least recently used
                lru_key = self.order.popleft()
                del self.cache[lru_key]
                print(f"Removed LRU: {lru_key}")
            self.cache[key] = value
        self.order.append(key)
        print(f"Inserted/Updated: {key} → {value}")

lru = LRUCache(3)
lru.put(1, 'A')
lru.put(2, 'B')
lru.put(3, 'C')
lru.get(2)
lru.put(4, 'D')  
lru.get(1)       
lru.get(3)