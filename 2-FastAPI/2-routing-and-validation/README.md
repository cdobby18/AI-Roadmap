# 2 · Routing & Validation

This is where FastAPI's real value shows up: Pydantic validates every request body before your function body even runs, and `response_model` guarantees what you send back matches a schema — no more hand-checking dict shapes.

---

## Progress Checklist

- [x] `main.py` — `ItemCreate` / `ItemUpdate` / `ItemResponse` Pydantic schemas, `Field()` constraints (`min_length`, `gt`, `ge`), `response_model` on every route, `HTTPException` with proper status codes, partial updates via `.dict(exclude_unset=True)`

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `BaseModel` | Declares the shape of a request/response — validates and serializes automatically |
| `Field(..., gt=0)` | Field-level constraints beyond just type — `...` marks required |
| `Optional[str] = None` | Optional field — used everywhere in `ItemUpdate` for partial updates |
| `response_model=` | FastAPI validates *and* filters the return value against this schema |
| `HTTPException(status_code=, detail=)` | Standardized error responses instead of ad-hoc dicts |
| `.dict(exclude_unset=True)` | Only pulls fields the client actually sent — the trick behind `PUT` partial updates |
| Status codes | `201 Created` on POST, `204 No Content` on DELETE, `404 Not Found` when the ID doesn't exist |

---

## Gotcha

Returning `{"error": "..."}, 404` (a tuple) like `1-basics/main.py` does is *not* how you set a status code in FastAPI — it just returns the tuple as JSON with a `200`. `HTTPException` is the actual mechanism, and this file is the first one to use it correctly.
