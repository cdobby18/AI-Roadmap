# 🏴‍☠️ Grand Line API

**Phase 2 Project** — Build a production-ready REST API for the One Piece world using FastAPI.  
The World Government needs a system to track pirates, crews, and bounties across the Grand Line.

---

## ⚓ Concept

| Real World | One Piece World |
|------------|-----------------|
| REST API | Grand Line Registry |
| Pirates (data) | Pirate records |
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
- Stores data in **SQLite** via SQLAlchemy

---

## 📁 Project Structure

```
phase-2-grandlineAPI/
├── main.py                  # App entry point — register routers, lifespan, middleware
├── requirements.txt         # Project dependencies
├── .env.example             # Environment variable template (never commit real .env)
└── app/
    ├── __init__.py
    ├── database.py          # SQLite engine + session factory + Base
    ├── config.py            # Settings loaded from .env via pydantic-settings
    ├── models.py            # SQLAlchemy ORM models (Pirate, Crew)
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
        └── logger.py        # Logs method, path, status code, process time per request
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
| FastAPI app setup + lifespan | `main.py` |
| SQLAlchemy ORM + SQLite | `database.py`, `models.py` |
| Pydantic request/response schemas | `schemas/` |
| APIRouter for modular routes | `routes/` |
| JWT token creation + validation | `auth/` |
| Protected endpoints with Depends() | `routes/pirates.py`, `routes/crews.py` |
| BackgroundTasks (bounty recalc) | `routes/pirates.py` |
| Custom HTTP middleware | `middleware/logger.py` |
| Environment variable config | `config.py`, `.env.example` |
| Proper HTTPException error handling | All route files |

---

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy environment variables
cp .env.example .env

# 3. Start the server
uvicorn main:app --reload

# 4. Open the docs
# http://localhost:8000/docs
```

---

## 🧠 What You Should Learn

- How to structure a production FastAPI project using APIRouter
- How SQLAlchemy connects to SQLite and creates tables
- How Pydantic schemas differ from ORM models (and why both exist)
- How JWT authentication works end-to-end (login → token → protected route)
- How middleware intercepts every request before it hits a route
- How BackgroundTasks let you respond immediately while work runs after

---

## 👑 Author

**Carl Joshua M. Coloma**  
Computer Science — Software Engineering  
AI Engineering Track | Phase 2 Project
