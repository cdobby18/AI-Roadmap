# 1 · Python Basics

The core syntax everything else in this roadmap is built on. Nothing fancy — variables, control flow, and the four built-in collection types you'll use in every script from here on.

---

## Progress Checklist

- [x] `variables.py` — int, float, string, bool
- [x] `operators.py` — comparison + boolean logic (`and`, `not`)
- [x] `condiState.py` — if / elif / else
- [x] `loops.py` — `for` with `range()`, `while` with a counter
- [x] `lists.py` — index, negative index, append/insert/remove/pop
- [x] `tuples.py` — fixed-size, immutable (`point[0] = 5` raises an error)
- [x] `sets.py` — dedupes automatically, `add()` / `remove()`
- [x] `dictionaries.py` — access/update/add/delete keys
- [x] `functions.py` — `def`, docstring, return value
- [x] `guide.py` — bonus: web scraping with `requests` + `BeautifulSoup` (GET a page, parse HTML, pull the first 20 links)

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| List vs Tuple | List is mutable, tuple isn't — use a tuple for data that shouldn't change (e.g. a coordinate) |
| Set | Unordered, no duplicates — good for membership checks and dedup |
| Dict | Key-value store — `del person["key"]` to remove |
| `for i in range(n)` | Counted loop |
| `while` | Loop until a condition flips — needs a manual counter/break |

---

## Note

`guide.py` is labeled "DAY 6" in-file and is actually a web scraping script (`requests` + `BeautifulSoup` against the UCI ML Repository) rather than a basics topic — it reads as an early detour into HTTP/parsing before Section 5 (`5-http-apis/`) formalizes it.
