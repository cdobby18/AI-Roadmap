# 4 · Authentication

Two auth patterns, same underlying idea: a FastAPI dependency runs *before* your route body and either returns an identity or raises `401`/`403`. `4a` does it with credentials sent on every request; `4b` does it with a signed, stateless token — the pattern you'll actually use in production.

---

## Progress Checklist

### 4a · HTTP Basic Auth
- [x] `4a-basic-auth/main.py` — `HTTPBasic()` security scheme, `secrets.compare_digest()` for timing-attack-safe password comparison, `Depends(authenticate_user)` on protected routes, a second `check_admin` dependency chained on top for role-gated routes

### 4b · JWT Auth
- [x] `4b-jwt-auth/main.py` — `/auth/signup` and `/auth/login` issue tokens, SHA256 password hashing, `Depends(jwt_bearer)` protects `/auth/me` and the `/posts` CRUD routes
- [x] `4b-jwt-auth/models.py` — `UserRegister` / `UserLogin` (with Pydantic `EmailStr`), `TokenResponse`, `PostCreate` / `PostOut`
- [x] `4b-jwt-auth/auth/jwt_handler.py` — `create_access_token()` / `decode_token()` using PyJWT, `HS256`, expiry embedded as an `exp` claim
- [x] `4b-jwt-auth/auth/jwt_bearer.py` — `JWTBearer(HTTPBearer)` subclass: pulls the token out of the `Authorization` header, checks the scheme is `Bearer`, decodes and validates it
- [x] `4b-jwt-auth/auth/__init__.py` — empty; marks `auth/` as an importable package

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `HTTPBasic()` | Client resends username+password (base64, not encrypted) on *every* request |
| `secrets.compare_digest()` | Constant-time string comparison — plain `==` leaks timing info an attacker can exploit |
| JWT (`header.payload.signature`) | Stateless — the server verifies a signature instead of looking up a session |
| `Depends(JWTBearer())` | Dependency injection — token validation happens once, before the route function runs |
| `exp` claim | Token self-expires; `decode_token()` returns `None` on `ExpiredSignatureError` |

---

## Gotcha: Basic Auth vs JWT

Basic Auth sends the raw password on *every single request* — fine over HTTPS for a quick internal tool, risky anywhere else, and it has no built-in expiry. JWT trades that for a signed token that expires and never re-transmits the password after login — but it's only as secure as `JWT_SECRET` (hardcoded here for the demo — load it from an environment variable in anything real).

Also worth flagging: `4b-jwt-auth/main.py` hashes passwords with plain `hashlib.sha256()` — no salt, no work factor. That's fine for learning the auth *flow*, but it's not how you'd hash passwords in production (use `bcrypt` or `argon2`, which are deliberately slow and salted).
