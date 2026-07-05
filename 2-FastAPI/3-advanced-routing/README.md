# 3 · Advanced Routing

Once an app has more than one resource, jamming every route into `main.py` stops scaling. This section splits routes into their own module with `APIRouter`, adds cross-cutting middleware, and swaps the in-memory list for JSON-file persistence — the shape a real service takes before it earns a database.

---

## Progress Checklist

- [x] `main.py` — wires the app together: mounts the custom timing middleware, adds `CORSMiddleware`, includes `issues_router`
- [x] `schemas.py` — `IssueCreate` / `IssueUpdate` / `IssueOut`, with `IssuesStatus` and `IssuePriority` as `str, Enum` fields (constrained values, shown as dropdowns in `/docs`)
- [x] `storage.py` — `load_data()` / `save_data()` reading and writing `issues.json` — a stand-in for a real DB layer
- [x] `middleware/timer.py` — `timing_middleware`, measures request duration and adds an `X-Process-Time` response header
- [x] `routes/issues.py` — `APIRouter(prefix="/api/v1/issues", tags=["issues"])`, full CRUD for issues backed by `storage.py`

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `APIRouter(prefix=, tags=)` | Group related routes in their own file, mount once via `app.include_router()` |
| `app.middleware("http")(fn)` | Register a plain async function as middleware — runs on every request/response |
| `CORSMiddleware` | Lets a browser-based frontend (React, Vue) on a different origin call this API |
| `str, Enum` schema field | Pydantic validates against a fixed set of values *and* FastAPI renders them as a dropdown in Swagger |
| `routes/` importing `schemas.py` / `storage.py` at the top level | Modules live at the project root, not nested under `routes/` — mirrors how the same-name files are imported directly (`from schemas import ...`) |

---

## Gotcha: middleware order

`main.py` registers the timer middleware first, then `CORSMiddleware`. It's tempting to assume "added first = runs first," but Starlette builds the stack in **reverse** registration order — the *last* middleware added ends up outermost. So here, `CORSMiddleware` is actually the outer layer and `timing_middleware` sits just inside it, closer to the router. Practical effect: `X-Process-Time` measures route-handling time, not CORS overhead — if you need the timer to wrap everything (including CORS), it would need to be added *last*, not first.
