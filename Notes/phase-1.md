# Phase 1 — Foundations

## Goal
Build the Python, data structures, and systems foundation every AI engineer is expected to have before touching ML code. Interviewers use this phase to filter candidates who can only call libraries from those who actually understand what's underneath.

## What I need to know
- Variables, data types, operators
- Control flow: `if`, `for`, `while`
- Functions and reusable code
- Collections: `list`, `tuple`, `set`, `dict`
- Classes, objects, inheritance
- Core data structures: linked list, stack, queue, binary search tree, heap
- Sorting algorithms and their complexity
- Algorithm patterns: recursion, dynamic programming, greedy, graph traversal
- Big-O time and space complexity
- SQLite CRUD, joins, aggregations, and indexing
- Calling APIs with `requests`
- Modules, packages, and `asyncio`
- Decorators, generators, and context managers

## Key terms

### Python core
- `variable`: named storage for a value. It's how you keep track of data in memory.
- `function`: named block that takes input and returns output. Avoids repeating code and makes logic testable.
- `list`: ordered, changeable collection. Use it when order matters or you need to append/pop.
- `tuple`: ordered, immutable collection. Use it for fixed records like coordinates or model config values.
- `set`: unordered collection of unique values. Use it for membership tests, deduplication, or unique feature values — O(1) lookup vs O(n) for a list.
- `dict`: key/value mapping. Use it for fast lookup by name, like model settings or JSON-like data — O(1) average lookup.
- `immutable`: a value that can't change after creation (e.g. `tuple`, `str`). Safer when multiple parts of a program read the same value.
- `mutable`: data that can change after creation (e.g. `list`, `dict`). Use it when you need to update state, like accumulating examples.
- `class`: blueprint for objects. Bundles data and behavior together so complex systems stay organized.
- `object`: an instance of a class — the concrete thing holding values and methods.
- `decorator`: a function that wraps another function to add behavior without changing its code (e.g. logging, timing, caching). Common in FastAPI (`@app.get`) and testing (`@pytest.fixture`).
- `generator`: a function using `yield` that produces values lazily, one at a time, instead of building a full list in memory. Use it for large datasets or streaming data.
- `context manager`: an object supporting `with`, guaranteeing setup/teardown (like closing a file or DB connection) even if an exception happens.

### Data structures
- `array / list`: contiguous, indexable storage. O(1) index access, O(n) insert/delete in the middle.
- `linked list`: nodes connected by pointers. O(1) insert/delete at the head, O(n) to search — no random access.
- `stack`: LIFO (last in, first out). Use it for undo history, expression parsing, or DFS.
- `queue`: FIFO (first in, first out). Use it for task scheduling, BFS, or message buffering.
- `binary search tree (BST)`: nodes where left < parent < right. Search/insert/delete average O(log n), worst case O(n) if unbalanced.
- `heap`: a tree-based structure keeping the min (or max) accessible in O(1), with O(log n) insert/remove. Used for priority queues, scheduling, and algorithms like Dijkstra's.

### Algorithms
- `Big-O notation`: describes how runtime or memory grows as input size grows. Interviewers expect you to state the Big-O of your solution and explain why.
- `recursion`: a function calling itself on a smaller subproblem, with a base case to stop. Foundation for tree/graph problems and divide-and-conquer.
- `dynamic programming (DP)`: solving a problem by breaking it into overlapping subproblems and caching results (memoization) instead of recomputing (e.g. Fibonacci, coin change, knapsack).
- `greedy algorithm`: makes the locally optimal choice at each step, hoping it leads to a globally optimal solution (e.g. Kruskal's, Prim's for minimum spanning tree). Doesn't always give the optimal answer — know when it does.
- `BFS / DFS`: breadth-first search explores level by level (shortest path in unweighted graphs); depth-first search explores as deep as possible before backtracking (good for cycle detection, connectivity).
- `Dijkstra's algorithm`: finds the shortest path from one node to all others in a weighted graph with non-negative edges, using a min-heap.
- `sorting complexity`: bubble/selection sort are O(n²) and mainly for teaching; merge sort is O(n log n) and stable; quicksort is O(n log n) average but O(n²) worst case and usually faster in practice due to lower constant factors.

### Databases
- `CRUD`: Create, Read, Update, Delete — the basic operations any database-backed app performs.
- `join`: combines rows from two tables based on a related column. `INNER JOIN` returns only matches; `LEFT JOIN` keeps all rows from the left table even without a match.
- `aggregation`: functions like `COUNT`, `SUM`, `AVG` combined with `GROUP BY` to summarize rows into groups.
- `index`: a data structure (usually a B-tree) that speeds up lookups on a column at the cost of extra storage and slower writes. Add one on columns you filter or join on frequently.
- `HTTP GET`: request data from a server without changing anything.
- `HTTP POST`: send data to a server to create or update a resource.
- `async/await`: syntax for asynchronous code. Lets your program do other work while waiting for I/O like network calls or disk access.

## When to use
- Use Python basics for data prep, feature engineering, and script automation.
- Use `set`/`dict` instead of `list` when you need repeated membership checks — this is a very common "how would you optimize this" interview follow-up.
- Use a stack for backtracking/undo problems, a queue for order-preserving processing, a heap when you repeatedly need the min/max.
- Use recursion + memoization (DP) when a brute-force solution recomputes the same subproblem many times.
- Use SQLite/SQL for small project storage, and add indexes once queries start filtering on a column often.
- Use `requests` to fetch external data or call APIs.
- Use generators when processing data too large to fit in memory (e.g. reading a huge file or streaming tokens).
- Use decorators for cross-cutting concerns (timing, logging, auth checks) instead of repeating code in every function.

## Interview review
- Explain why you choose one collection over another: `list` for ordered data, `dict`/`set` for O(1) lookup, `tuple` for fixed, hashable records.
- Be ready to state the time/space complexity of anything you write, and explain the tradeoff (e.g. "hash map trades memory for O(1) lookup").
- Common whiteboard-style prompts to be ready for: reverse a linked list, detect a cycle, implement a stack with O(1) min, BFS/DFS a graph, binary search, merge two sorted lists, find the kth largest element (heap).
- If asked "how would you speed this up," the expected answer is almost always: better data structure, indexing, or caching — not "add more hardware."
- For SQL, describe the difference between `INNER JOIN` and `LEFT JOIN`, and when you'd add an index (frequent `WHERE`/`JOIN` columns) versus when you wouldn't (small tables, write-heavy tables).
- If asked about `async`, say it's useful when the code waits on I/O rather than CPU-bound work; for CPU-bound work you'd reach for multiprocessing instead.
- If asked about generators vs lists, say generators trade upfront computation and memory for lazy, one-at-a-time evaluation.

## Common pitfalls
- Using mutable default arguments like `def f(x, log=[])` — the same list is reused across calls, causing shared-state bugs. Use `None` and initialize inside the function.
- Forgetting to close database/file connections; prefer `with sqlite3.connect(...) as conn:` (a context manager).
- Assuming `requests.get()` always succeeds; check `status_code` / use `resp.raise_for_status()`.
- Using a `list` for frequent `in` checks instead of a `set` — this is O(n) per check instead of O(1).
- Writing recursion without a base case, or without memoization when subproblems repeat (leads to exponential blowup, e.g. naive Fibonacci).
- Adding an index to every column "just in case" — indexes speed up reads but slow down writes and cost storage.

## How to use

### Simple function
```python
def add(a, b):
    return a + b

print(add(4, 5))
```

### Common collections
```python
nums = [1, 2, 3]
config = {"lr": 0.001, "batch_size": 32}
flags = {True, False}
pair = (10, 20)
```

### Class pattern
```python
class Dataset:
    def __init__(self, rows):
        self.rows = rows

    def count(self):
        return len(self.rows)
```

### Stack and queue
```python
stack = []
stack.append(1)     # push
stack.append(2)
stack.pop()          # pop -> 2 (LIFO)

from collections import deque
queue = deque()
queue.append(1)      # enqueue
queue.append(2)
queue.popleft()       # dequeue -> 1 (FIFO)
```

### Binary search tree insert
```python
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root
```

### Heap as a priority queue
```python
import heapq

heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
print(heapq.heappop(heap))  # 1 (smallest first)
```

### Recursion with memoization (DP)
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

### Sorting (merge sort)
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
```

### Graph BFS
```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order
```

### SQLite pattern
```python
import sqlite3
with sqlite3.connect("data.db") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    conn.commit()
    rows = cur.execute("SELECT * FROM users").fetchall()
```

### Join, aggregation, and index
```sql
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.name;

CREATE INDEX idx_orders_user_id ON orders(user_id);
```

### Requests pattern
```python
import requests
resp = requests.get("https://api.example.com/data")
resp.raise_for_status()
data = resp.json()
```

### Async pattern
```python
import asyncio

async def wait_and_print():
    await asyncio.sleep(1)
    print("done")

asyncio.run(wait_and_print())
```

### Decorator
```python
import time
from functools import wraps

def timed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        print(f"{fn.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

@timed
def slow_add(a, b):
    return a + b
```

### Generator
```python
def batch(iterable, size):
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
```
