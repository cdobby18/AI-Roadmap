# Phase 1 · Foundations

The starting point of the roadmap — core Python, OOP, classic data structures & algorithms, SQL, and the HTTP/async fundamentals every AI engineer eventually leans on to call an LLM API or run concurrent requests.

**Prerequisite:** None — this is the entry point.
**Next:** Phase 2 (FastAPI)

---

## Structure

| Folder | Topic | Priority |
|--------|-------|----------|
| `1-python-basics/` | Variables, control flow, collections, functions | Required |
| `2-oop/` | Classes, inheritance, dunder methods, the four pillars | Required |
| `3-dsa/` | Basic data structures, sorting, classic algorithms (DP/greedy/graph) | Required |
| `4-database/` | SQL via MySQL — DDL, CRUD, joins, indexing, SQL → Pandas | Required |
| `5-http-apis/` | `requests` — GET/POST, auth, error handling, Sessions | Required |
| `6-advanced-python/` | `asyncio` concurrency + modules/file I/O | Required |

---

## What AI Engineers Actually Need Here

All six sections are foundational and worth doing in full. Two are worth calling out specifically: `3-dsa/` is what actually gets tested in technical interviews (even at AI-focused companies, the whiteboard round is still classic CS), and `5-http-apis/` + the concurrency half of `6-advanced-python/` are what you'll use directly and constantly once you're calling LLM APIs — every `client.messages.create()` you'll write later is a `requests`-style HTTP call wearing an SDK.

---

## Master Progress Checklist

### 1 · Python Basics
- [x] Variables, operators, conditionals, loops
- [x] Lists, tuples, sets, dictionaries
- [x] Functions
- [x] Bonus: web scraping with `requests` + `BeautifulSoup`

### 2 · OOP
- [x] Classes & instances, class variables vs instance variables
- [x] `@classmethod` / `@staticmethod`
- [x] Inheritance + method overriding
- [x] Dunder methods (`__str__`, `__eq__`, `__lt__`, ...)
- [x] Property decorators (getter/setter/deleter)
- [x] Capstone: abstraction + inheritance + polymorphism + encapsulation in one file

### 3 · DSA
- [x] Basic structures: stack, queue, linked list, BST, heap
- [x] Sorting: bubble, selection, merge, quick
- [x] Algorithms: brute force, DP (fibonacci, coin change, knapsack), greedy, Dijkstra, Prim's, Kruskal's, TSP

### 4 · Database
- [x] DDL (create database/table)
- [x] CRUD
- [x] Filtering, sorting, aggregation, `GROUP BY`
- [x] Joins, indexing
- [x] SQL → Pandas pipeline

### 5 · HTTP & APIs
- [x] GET / POST requests
- [x] Headers, auth, `Session`
- [x] Error handling (timeouts, HTTP errors, rate limits)
- [x] Capstone: reusable `AIClient` class

### 6 · Advanced Python
- [x] Coroutines, `await`, `Future`, `Lock`, `TaskGroup`
- [x] Modules, default params, file I/O (text + JSON)

---

## Learning Path

```
1-python-basics → 2-oop → 3-dsa
                              ↓
6-advanced-python ← 5-http-apis ← 4-database
```

---

## Resources

| Resource | What | Format | Cost |
|----------|------|--------|------|
| Python official tutorial | Canonical reference for syntax and stdlib | Docs | Free |
| Real Python — OOP series | Deeper dives on classes, dunder methods, properties | Articles | Free |
| NeetCode | Best DSA practice with video explanations | Video + Practice | Free |
| W3Schools SQL | Fast syntax reference for every SQL clause | Docs | Free |
| Real Python — `requests` guide | The definitive guide to the `requests` library | Docs + Code | Free |
| Real Python — Async IO in Python | Explains the coroutine/task/event-loop model clearly | Article | Free |

---

## Capstone Project

**[DevilFruit Text Processor](../8-Projects/phase-1-devilfruit/)** — A CLI script that reads raw text, runs it through an OOP text-cleaning pipeline (lowercase → strip punctuation → collapse whitespace → strip numbers → remove stopwords → tokenize), detects its language, and persists every run to a MySQL database.

Applies every section of Phase 1 end-to-end: `fruit.py`'s `DevilFruit` class chains cleaning methods (2-oop) into a pipeline, `database.py` implements CRUD/filtering/aggregation/joins/indexing (4-database) behind a single `execute()` helper, and `grandline.py` ties it together as the entry point — reading `poneglyph.txt`, running the pipeline, saving the result, and reading it back to prove the round-trip works.
