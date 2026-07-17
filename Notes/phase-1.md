# Phase 1 — Foundations

## Core Python

**Variables & types:** Python is dynamically typed. Mutable types (list, dict, set) change in place; immutable (int, str, tuple) create new objects on every operation. Consequence for AI: string concatenation with `+` in a loop is O(n²) — use `''.join()`.

**Collections:**
- `list` — ordered, O(n) lookup. Use when order matters or you need index access.
- `dict` — O(1) lookup by key. Use for JSON-like data, configs, feature maps.
- `set` — O(1) membership test. Use for dedup, "have I seen this before."
- `tuple` — immutable, hashable. Use for fixed records, dict keys.

**Why set/dict are O(1):** hash table. Tradeoff: ~3x more memory than a list. Always use set over list for `in` checks in interviews.

**Functions:** `*args` captures positional extras, `**kwargs` captures keyword extras (used everywhere in ML — model constructors, Trainer, plot params). `lambda` is for simple sort keys / DataFrame apply — never for complex logic.

**Comprehensions** ([x for x in y]) are faster than manual for+append because the append runs in C, not Python bytecode.

**Generators** (yield): Lazy evaluation — one item at a time, O(1) memory vs O(n) for a list. Use for large files, streaming LLM tokens, infinite sequences. Generator expressions `(x for x in y)` use less memory than list comprehensions.

**Context managers** (with): Guarantee cleanup (close file, disable gradients, release lock) even on exception. `torch.no_grad()` is a context manager.

**Async/await:** Cooperative multitasking for I/O-bound work. `async def` returns a coroutine — it runs only when awaited. Not useful for CPU/GPU-bound model inference. Use multiprocessing for CPU work, threading for blocking I/O with libraries that don't support async.

**Decorators:** Functions that wrap functions. Used for cross-cutting concerns: logging, timing, caching, auth. `@app.get("/route")` in FastAPI is a decorator that registers the handler.

**`if __name__ == "__main__":`** — code runs only on direct execution, not import. Use for CLI entry points and demos.

## DSA

**Big-O:** Describes how runtime scales with input size, ignoring constants.
- O(1): dict lookup, array index
- O(log n): binary search, heap push/pop
- O(n): iterating a list
- O(n log n): efficient sorting
- O(n²): nested loops, naive attention
- O(2ⁿ): brute-force subset problems

**Attention is O(n²) in sequence length — the fundamental transformer bottleneck.** FAISS retrieval is O(log n) with IVF indexes.

**Data structures:**
- Stack (LIFO) — Python list is already a stack: append/pop. Use for DFS, undo, expression parsing.
- Queue (FIFO) — `collections.deque` with append/popleft. Use for BFS, task scheduling.
- Heap — `heapq` module. O(1) min, O(log n) push/pop. Use for priority queues, top-k, Dijkstra.
- Hash table — foundation of dict/set. Python uses random seed per process to prevent hash-flooding DoS.

**Sorting:** Python uses Timsort (hybrid merge+insertion), O(n log n) worst, O(n) on nearly-sorted data. Never implement your own.

**Algorithm patterns:**
- Two pointers — O(n) on sorted arrays.
- Sliding window — O(n) for contiguous subarray problems.
- Recursion — always needs a base case. Without memoization, exponential blowup (naive Fibonacci).
- DP — recursion + memoization (`@lru_cache`). Use when problem has optimal substructure + overlapping subproblems.
- BFS (queue) — shortest path in unweighted graphs, level-order traversal.
- DFS (stack/recursion) — cycle detection, topological sort, connectivity.
- Binary search — O(log n) on sorted data.

## SQL

**CRUD + parameterized queries:** Always use `?` placeholders. Never f-strings — SQL injection.

**JOINs:** INNER JOIN returns only matches; LEFT JOIN keeps all left-side rows (NULLs for missing right-side). Used everywhere in data analysis and ML feature engineering.

**WHERE vs HAVING:** WHERE filters rows before grouping; HAVING filters groups after.

**Indexing:** Speeds up reads on WHERE/JOIN/ORDER BY columns. Tradeoff: slower writes, more disk. Index high-cardinality columns in read-heavy tables. Skip on write-heavy logs or low-cardinality columns.

**ACID:** Atomicity, Consistency, Isolation, Durability. Transactions ensure all-or-nothing execution.

**SQL vs NoSQL:** SQL for relational data, complex joins, transactions. NoSQL for flexible schema, high write throughput, horizontal scale. PostgreSQL with pgvector also handles vector search.

## HTTP APIs

**Key status codes:** 200 (OK), 201 (Created), 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 422 (validation error), 429 (rate limited), 500 (server error), 503 (unavailable).

**Auth headers:** `Authorization: Bearer <token>` for JWT. `Content-Type: application/json` for JSON APIs.

## Common Pitfalls
- Mutable default args (`def f(x, l=[])`) — same list reused across calls. Use `None` + init inside.
- `== None` vs `is None` — use `is` for singletons.
- Modifying a list while iterating it — iterate over a copy.
- Not closing files/DB connections — use context managers.
- Bare `except:` — catch specific exceptions.
- Forgetting `resp.raise_for_status()` — silent failures.

## Interview Must-Knows
- Why set/dict have O(1) lookup (hash table, tradeoff: memory).
- Difference between INNER and LEFT JOIN.
- When to add an index.
- How async works vs threading vs multiprocessing.
- Common coding: reverse linked list, detect cycle, BFS/DFS, binary search, two-sum (hash map), valid parentheses (stack), max subarray (Kadane's, O(n)).
