# 🏴‍☠️ Grand Line API

**Phase 2 Project** — Build a production-ready REST API for the One Piece world using FastAPI.  
The World Government needs a system to track pirates, crews, and bounties across the Grand Line.

> **Note:** This version uses in-memory dummy data instead of a database.  
> No SQLite, no SQLAlchemy, no `.env` file needed — just Python lists and dicts.  
> Perfect for a practice environment where you can't install extra software.

---

## ⚓ Concept

| Real World | One Piece World |
|------------|-----------------|
| REST API | Grand Line Registry |
| In-memory store | Pirate & Crew records |
| JWT Token | Marine Authorization Badge |
| Background Task | Bounty recalculation job |
| Middleware | Den Den Mushi logger |

---

## 🗺️ What to Build

A fully structured FastAPI application that:

- Registers and manages **Pirates** and **Crews** (full CRUD)
- Tracks and updates **Bounties** per pirate
- Protects write operations behind **JWT Authentication** (marines only)
- Logs every incoming request via **Middleware**
- Handles bounty recalculations as a **Background Task** (fire-and-forget)
- Validates all input with **Pydantic schemas**
- Stores data in **in-memory Python lists** (resets on server restart)

---

## 📁 Project Structure

```
phase-2-grandlineAPI/
├── main.py                  # App entry point — register routers, middleware
├── requirements.txt         # Project dependencies (no sqlalchemy needed)
└── app/
    ├── __init__.py
    ├── config.py            # Hardcoded constants (SECRET_KEY, credentials)
    ├── store.py             # In-memory dummy data (pirates_db, crews_db lists)
    ├── models.py            # TypedDict shapes for Pirate and Crew dicts
    ├── schemas/
    │   ├── __init__.py
    │   ├── pirate.py        # Pydantic request/response models for pirates
    │   └── crew.py          # Pydantic request/response models for crews
    ├── routes/
    │   ├── __init__.py
    │   ├── auth.py          # POST /auth/login → returns JWT token
    │   ├── pirates.py       # CRUD endpoints for pirates
    │   └── crews.py         # CRUD endpoints for crews
    ├── auth/
    │   ├── __init__.py
    │   ├── jwt_handler.py   # Create and decode JWT tokens
    │   └── jwt_bearer.py    # FastAPI dependency to protect routes
    └── middleware/
        ├── __init__.py
        └── logger.py        # Logs method, path, status code, process time
```

---

## 🔗 API Endpoints

### Auth
| Method | Path | Description | Protected |
|--------|------|-------------|-----------|
| POST | `/auth/login` | Returns JWT token | No |

### Pirates
| Method | Path | Description | Protected |
|--------|------|-------------|-----------|
| GET | `/pirates` | List all pirates | No |
| GET | `/pirates/{id}` | Get one pirate | No |
| POST | `/pirates` | Register new pirate | Yes |
| PUT | `/pirates/{id}` | Update pirate | Yes |
| DELETE | `/pirates/{id}` | Remove pirate | Yes |

### Crews
| Method | Path | Description | Protected |
|--------|------|-------------|-----------|
| GET | `/crews` | List all crews | No |
| GET | `/crews/{id}` | Get one crew | No |
| POST | `/crews` | Create new crew | Yes |
| PUT | `/crews/{id}` | Update crew | Yes |
| DELETE | `/crews/{id}` | Remove crew | Yes |

---

## ⚔️ Skills You Will Practice

| Skill | Where |
|-------|-------|
| FastAPI app setup | `main.py` |
| In-memory data store (lists of dicts) | `store.py` |
| TypedDict for type-safe dicts | `models.py` |
| Pydantic request/response schemas | `schemas/` |
| APIRouter for modular routes | `routes/` |
| JWT token creation + validation | `auth/` |
| Protected endpoints with Depends() | `routes/pirates.py`, `routes/crews.py` |
| BackgroundTasks (bounty recalc) | `routes/pirates.py` |
| Custom HTTP middleware | `middleware/logger.py` |
| Hardcoded config constants | `config.py` |
| HTTPException error handling | All route files |

---

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server (no .env file needed)
uvicorn main:app --reload

# 3. Open the docs
# http://localhost:8000/docs

# 4. Log in via the Authorize button in /docs
#    Username and password are in app/config.py
```

---

## 🧠 What You Should Learn

- How to structure a modular FastAPI project using APIRouter
- How Pydantic schemas validate both incoming requests and outgoing responses
- How JWT authentication works end-to-end (login → token → protected route)
- How middleware intercepts every request before and after a route runs
- How BackgroundTasks let you respond immediately while work runs after
- How to use in-memory Python lists as a stand-in for a database

---

## 👑 Author

**Carl Joshua M. Coloma**  
Computer Science — Software Engineering  
AI Engineering Track | Phase 2 Project
