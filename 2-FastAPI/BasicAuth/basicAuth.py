import secrets
from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

# -----------------------------
# BASIC AUTH CONFIG
# -----------------------------
security = HTTPBasic()

# In-memory "database" (for learning only)
users_db = {
    "stanleyjobson": {"password": "swordfish", "role": "admin"},
    "alice": {"password": "wonderland", "role": "user"},
    "bob": {"password": "builder", "role": "user"},
}


# -----------------------------
# AUTH UTILITIES
# -----------------------------
def verify_password(plain: str, stored: str) -> bool:
    """
    Secure string comparison to prevent timing attacks.
    """
    return secrets.compare_digest(
        plain.encode("utf-8"),
        stored.encode("utf-8")
    )


def authenticate_user(credentials: HTTPBasicCredentials) -> str:
    """
    Core authentication logic:
    1. Check if user exists
    2. Validate password
    3. Return username if valid
    """

    user = users_db.get(credentials.username)

    # Step 1: user exists?
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Step 2: password correct?
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


# -----------------------------
# DEPENDENCY (REUSABLE AUTH LAYER)
# -----------------------------
def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    """
    FastAPI dependency:
    Automatically extracts Basic Auth credentials
    and validates them.
    """
    return authenticate_user(credentials)


# -----------------------------
# ROUTES (PROTECTED + PUBLIC)
# -----------------------------

@app.get("/")
def home():
    """
    Public endpoint (no auth required)
    """
    return {"message": "Basic Auth demo API is running"}


@app.get("/me")
def get_me(username: Annotated[str, Depends(get_current_user)]):
    """
    Protected route:
    Returns current authenticated user
    """
    return {
        "username": username,
        "message": "You are authenticated via Basic Auth"
    }


@app.get("/secure-data")
def secure_data(username: Annotated[str, Depends(get_current_user)]):
    """
    Example protected resource
    """
    role = users_db[username]["role"]

    return {
        "data": f"Secret data for {username}",
        "role": role,
        "access": "granted"
    }


@app.get("/admin-only")
def admin_route(username: Annotated[str, Depends(get_current_user)]):
    """
    Simple role-based check (still Basic Auth system)
    """
    if users_db[username]["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return {
        "message": f"Welcome admin {username}",
        "system": "Full access granted"
    }


@app.get("/debug-credentials")
def debug_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    """
    Educational endpoint:
    Shows what FastAPI receives from Basic Auth
    """
    return {
        "username": credentials.username,
        "password": "hidden for security",
        "type": "HTTP Basic Auth",
        "note": "Never expose raw passwords in production"
    }