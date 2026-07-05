# DevilFruit Text Processor — Lessons

**Phase:** 1 — Python Foundations + DSA + SQL

---

## Skills This Project Actually Exercises

- **OOP + method chaining** — every cleaning method returns `self`, so a whole pipeline reads as one fluent call (`fruit.clean_all()`). This is the same pattern behind pandas' `.dropna().reset_index()` chains and SQLAlchemy's query builder — return `self` (or a new instance) from a mutator and chaining falls out for free.
- **Regex text cleaning** — `re.sub(r'[^\w\s]', '', text)` to strip punctuation, `re.sub(r'\d+', '', text)` for digits, `re.sub(r'\s+', ' ', text)` to collapse whitespace. These three patterns cover most "clean this string" needs before any NLP touches it.
- **`collections.Counter`** — `Counter(tokens).most_common(5)` for word frequency instead of hand-rolling a dict + max loop.
- **A real third-party library instead of hand-rolled logic** — `langdetect.detect()` for language detection. Knowing when to reach for a library (language detection, date parsing, etc.) instead of writing it yourself is itself a skill.
- **A single query-execution chokepoint** — `database.py` funnels every query through one `execute()` function that owns connection open/close and commit/rollback. Every other function just builds a query string and params. This is the cheapest version of the repository pattern: one place to change if the DB driver, retry logic, or logging ever changes.
- **SQL joins and aggregation from Python** — `INNER JOIN` (only rows with a match) vs `LEFT JOIN` (keep all users even with no processing history) are exercised directly, plus `COUNT`/`AVG`/`MAX`/`MIN`/`SUM` and `GROUP BY`.
- **Credentials via `.env`, never hardcoded** — `load_dotenv()` + `os.getenv(...)` for DB credentials, set up correctly from the very first project.

---

## Where This Sits in the Roadmap

This project is the concrete version of everything **Phase 1** (`1-Foundations/`) covers in isolation: OOP classes/`self`/magic methods (`4-database`, `2-oop`), SQLite/MySQL CRUD-joins-aggregation-indexing (`4-database`), and calling out to a library instead of an API. It's the first time those separate lessons get combined into one working program instead of staying as standalone exercises.

**Forward references:**
- The `execute()`-as-chokepoint pattern reappears conceptually in Phase 2's `store.py` (all reads/writes to `pirates_db`/`crews_db` funnel through a small set of functions) — same idea, in-memory instead of MySQL.
- Method chaining via `return self` is the same mental model as PyTorch's `nn.Sequential` in Phase 3 (`model.py`) — a pipeline built by composing steps, just declarative instead of chained calls.

---

## Common Pitfalls Worth Remembering

- `database.py` opens and closes a brand-new MySQL connection on *every single call* to `execute()`. Fine for a CLI script; would need a connection pool (or an ORM session) under real request volume — this is the kind of thing that looks correct in a demo and falls over under load.
- Stopword removal happens on the **already-lowercased, punctuation-stripped** text — order of operations in a cleaning pipeline matters; running `remove_stopwords()` before `lowercase()` would miss capitalized stopwords like "The" at a sentence start.
- `get_summary()` calls `self.tokenize()` if `self.tokens` is empty, so summary stats are safe to call even without running `clean_all()` first — but that also means summary stats on *uncleaned* text (with punctuation still attached) will look different from the pipeline's intended output. Always run `clean_all()` before trusting the summary.
