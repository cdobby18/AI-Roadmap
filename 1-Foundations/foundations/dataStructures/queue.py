# EASY
from collections import deque

queue = deque()

queue.append("Alice")
queue.append("Bob")
queue.append("Charlie")

print("Queue:", queue)

served = queue.popleft()

print("Served:", served)
print("Queue after serving:", queue)

# MEDIUM
from collections import deque

printer_queue = deque()

printer_queue.append("Document1")
printer_queue.append("Document2")
printer_queue.append("Document3")

while printer_queue:

    job = printer_queue.popleft()

    print("Printing:", job)

# HARD
class CircularQueue:

    def __init__(self, size):
        self.queue = [None] * size
        self.size = size
        self.front = -1
        self.rear = -1


    def enqueue(self, data):

        if (self.rear + 1) % self.size == self.front:
            print("Queue is full")
            return

        if self.front == -1:
            self.front = 0

        self.rear = (self.rear + 1) % self.size
        self.queue[self.rear] = data


    def dequeue(self):

        if self.front == -1:
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