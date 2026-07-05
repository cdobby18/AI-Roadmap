# 4 · Database

SQL fundamentals via MySQL (`mysql.connector`), numbered as "SQL LEVEL 1" through "LEVEL 7" in the file docstrings — that level number, not the filename, is the real reading order.

---

## Progress Checklist

- [x] `database.py` — LEVEL 1: DDL — `CREATE DATABASE`, `CREATE TABLE`, data types, `PRIMARY KEY`
- [x] `crudOperations.py` — LEVEL 2: CRUD — `INSERT`, `SELECT`, `UPDATE`, `DELETE`
- [x] `filterSort.py` — LEVEL 3: `WHERE`, `ORDER BY`, `LIMIT`
- [x] `aggregations.py` — LEVEL 4: `COUNT()`, `AVG()`, `GROUP BY`
- [x] `joins.py` — LEVEL 5: `INNER JOIN` across `users` and `orders`
- [x] `indexing.py` — LEVEL 6: `CREATE INDEX` for query optimization
- [x] `pyInteg.py` — LEVEL 7: `pd.read_sql()` — load a table straight into a Pandas DataFrame, then feature-engineer a column (`age_group`) — this is where the DB layer meets the ML layer

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| CRUD | Create/Read/Update/Delete — 90% of backend and AI data-pipeline work |
| `WHERE` / `ORDER BY` / `LIMIT` | How you carve a usable dataset out of a full table |
| `GROUP BY` | Pairs with `COUNT`/`AVG`/`SUM` for basic analytics before any ML |
| `INNER JOIN` | Real data is never in one table — this is how you recombine it |
| Index | Speeds up lookups on large tables — the cost is slower writes, so don't index everything |
| `pd.read_sql(query, connection)` | The bridge from a live database into a DataFrame you can model on |

---

## Gotcha

Every file connects with a hardcoded local password (`password="password"`) — fine for a learning script against `localhost`, but credentials like this belong in environment variables (see `5-http-apis/` and `8-Projects/phase-1-devilfruit/database.py` for the `.env` + `python-dotenv` pattern used in the actual capstone).
