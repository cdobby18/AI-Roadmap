# Grand Line API — Context

**Phase:** 2 — FastAPI + Auth + Background Tasks
**Theme:** The World Government needs a system to track pirates, crews, and bounties across the Grand Line.

> Uses in-memory Python lists as the data store — no SQLite/SQLAlchemy/`.env` needed.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Framework | FastAPI |
| Server | Uvicorn (ASGI) |
| Auth | JWT via `python-jose` |
| Validation | Pydantic v2 |
| Rate limiting | `slowapi` |
| Storage | In-memory (Python lists) |

---

## Project Structure

```
phase-2-grandlineAPI/
├── main.py                    # App entry point — wires everything together
├── requirements.txt
└── app/
    ├── config.py               # App constants (secret key, credentials)
    ├── models.py                # TypedDict definitions (type hints for dicts)
    ├── store.py                 # In-memory data store (pirates_db, crews_db)
    ├── auth/
    │   ├── jwt_handler.py        # Token creation and decoding
    │   └── jwt_bearer.py         # FastAPI dependency for protected routes
    ├── middleware/
    │   ├── logger.py             # Request/response logging middleware
    │   └── rate_limiter.py       # slowapi limiter instance
    ├── routes/
    │   ├── auth.py                # POST /auth/login
    │   ├── pirates.py             # Pirate CRUD endpoints
    │   └── crews.py               # Crew CRUD + nested /crews/{id}/pirates
    └── schemas/
        ├── pirate.py              # PirateCreate, PirateUpdate, PirateResponse
        └── crew.py                # CrewCreate, CrewUpdate, CrewResponse
```

---

## Request Lifecycle

```
Client → SlowAPIMiddleware (rate limit, 429 if exceeded)
       → log_requests middleware (records start time)
       → FastAPI router matches path + method
       → Depends(get_current_marine) on protected routes (validates JWT)
       → route handler reads/writes store.py lists, builds response
       → Pydantic response_model validates + serializes
       → log_requests middleware logs method/path/status/duration
       → Client receives response
       → BackgroundTasks (if any) run after the response is sent
```

---

## Auth Flow

```
1. POST /auth/login  (form: username=marine&password=justice)
2. Server checks credentials against config.py constants,
   calls create_access_token({"sub": "marine"})
   returns {"access_token": "<jwt>", "token_type": "bearer"}
3. Client sends Authorization: Bearer <jwt> on future requests
4. get_current_marine() dependency decodes the JWT, extracts "sub"
   → valid: route runs / invalid or expired: 401
```

Tokens expire after 30 minutes (`config.py`).

---

## Rate Limits

| Route | Limit | Reason |
|---|---|---|
| `POST /auth/login` | 10/minute | Prevent brute-force attacks |
| All GET routes | 60/minute | Normal read traffic |
| POST / PUT / DELETE | 30/minute | Writes are more expensive |

---

## Background Tasks

`POST /pirates` returns 201 immediately, then runs `recalculate_bounty(pirate_id)` (bounty × 1.1) **after** the response is sent — fire-and-forget.

---

## API Reference

**Base URL:** `http://localhost:8000` · **Docs:** `http://localhost:8000/docs`

### Auth
| Method | Path | Auth | Body |
|---|---|---|---|
| POST | `/auth/login` | No | form: username, password |

### Pirates
| Method | Path | Auth | Body |
|---|---|---|---|
| GET | `/pirates` | No | — |
| GET | `/pirates/{id}` | No | — |
| POST | `/pirates` | Yes | PirateCreate |
| PUT | `/pirates/{id}` | Yes | PirateUpdate |
| DELETE | `/pirates/{id}` | Yes | — |

### Crews
| Method | Path | Auth | Body |
|---|---|---|---|
| GET | `/crews` | No | — |
| GET | `/crews/{id}` | No | — |
| POST | `/crews` | Yes | CrewCreate |
| PUT | `/crews/{id}` | Yes | CrewUpdate |
| DELETE | `/crews/{id}` | Yes | — |
| GET | `/crews/{id}/pirates` | No | — |

---

## How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
open http://localhost:8000/docs
```

```bash
# Full flow via curl
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -d "username=marine&password=justice" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

curl http://localhost:8000/crews
curl -X POST http://localhost:8000/pirates \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name": "Shanks", "bounty": 4048900000, "role": "Captain"}'
curl http://localhost:8000/crews/1/pirates
```

---

## Author

**Carl Joshua M. Coloma** — Computer Science, Software Engineering — AI Engineering Track — Phase 2 Project
