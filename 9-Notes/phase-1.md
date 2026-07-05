# Phase 1 — Foundations

## Goal
Build the Python foundation needed for every AI engineering task.

## What I need to know
- Variables, data types, operators
- Control flow: `if`, `for`, `while`
- Functions and reusable code
- Collections: `list`, `tuple`, `set`, `dict`
- Classes, objects, inheritance
- Simple algorithms and sorting
- SQLite CRUD and basic joins
- Calling APIs with `requests`
- Modules, packages, and `asyncio`

## Key terms
- `variable`: named storage for a value. This is the first thing you learn in programming and it is how you keep track of data in memory.
- `function`: named block that takes input and returns output. Functions help you avoid repeating code and make your logic easier to test.
- `list`: ordered, changeable collection of values. Use lists when the order matters or when you need to append items.
- `tuple`: ordered, immutable collection. Use tuples for fixed records like coordinates or model configuration values.
- `set`: unordered collection of unique values. Use sets for membership tests, deduplication, or unique feature values.
- `dict`: key/value mappings. Use dictionaries when you need fast lookup by name, such as model settings or JSON-like data.
- `immutable`: a value that cannot change once created (e.g. `tuple`). Immutable data is safer when multiple parts of a program read the same value.
- `mutable`: data that can change after creation (e.g. `list`, `dict`). Use mutable structures when you need to update state, like collecting examples or feature values.
- `class`: blueprint for objects. A class lets you bundle data and behavior together, which makes complex systems easier to manage.
- `object`: instance of a class. When you create a class, an object is the concrete thing that holds values and methods.
- `CRUD`: Create, Read, Update, Delete. These are the basic operations any database-backed app performs.
- `HTTP GET`: request data from a server. Use GET when you want to retrieve information without changing anything.
- `HTTP POST`: send data to a server. Use POST when you want to create or update a resource.
- `async/await`: syntax for asynchronous code. This lets your program do other work while waiting for I/O like network calls or disk access.

## When to use
- Use Python basics for data prep, feature engineering, and script automation.
- Use lists/dicts when storing model inputs and settings.
- Use classes when a model or data pipeline needs structure.
- Use SQLite for small project storage or quick prototypes.
- Use `requests` to fetch external data or call APIs.

## Interview review
- Explain why you choose one collection over another: `list` for ordered data, `dict` for lookup by key, `tuple` for fixed records.
- When asked about functions, mention readability, testability, and how they help you separate preprocessing from model logic.
- If they ask about `async`, say it is useful when the code waits on I/O rather than CPU work.
- For SQL, describe the difference between `SELECT` and `INSERT`, and when you would use an indexed column for faster lookups.

## Common pitfalls
- Using mutable defaults in function arguments like `def f(x, log=[])` can cause shared state bugs.
- Forgetting to close database connections; prefer `with sqlite3.connect(...) as conn:`.
- Assuming `requests.get()` is instantaneous; always check `status_code` and handle errors.

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

### SQLite pattern
```python
import sqlite3
conn = sqlite3.connect("data.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
conn.commit()
rows = cur.execute("SELECT * FROM users").fetchall()
conn.close()
```

### Requests pattern
```python
import requests
resp = requests.get("https://api.example.com/data")
if resp.ok:
    data = resp.json()
    print(data)
```

### Async pattern
```python
import asyncio

async def wait_and_print():
    await asyncio.sleep(1)
    print("done")

asyncio.run(wait_and_print())
```
