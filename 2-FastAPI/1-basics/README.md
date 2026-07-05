# 1 · Basics

The smallest possible FastAPI app — one file, in-memory list, a handful of routes. The point isn't the CRUD logic, it's getting comfortable with the decorator style, Uvicorn's reload loop, and the free `/docs` UI before anything gets complicated.

---

## Progress Checklist

- [x] `main.py` — `FastAPI()` app instance, GET/POST/DELETE routes over an in-memory `items` list, path parameters (`/items/{item_id}`) vs query parameters (`/search?keyword=&min_price=`)

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `FastAPI(title=, description=, version=)` | App instance — metadata shows up in `/docs` |
| `@app.get` / `@app.post` / `@app.delete` | Route decorators bind a function to a path + HTTP method |
| Path parameter | `{item_id}` in the route — required, part of the URL |
| Query parameter | Function args not in the path — optional, appended after `?` |
| `uvicorn main:app --reload` | Runs the ASGI app, auto-restarts on file changes |
| `/docs` | Swagger UI — auto-generated from your route signatures, no extra code |
