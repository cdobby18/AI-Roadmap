"""
04a - AUTHENTICATION: HTTP Basic Auth

Learn:
- HTTP Basic Authentication (username + password in header)
- Secure password verification
- Bearer token pattern
- Protected endpoints

Key Concepts:
- Never hardcode passwords
- Use `secrets` module for comparisons (timing attack prevention)
- Always use HTTPS in production

Run: uvicorn main:app --reload
"""

import secrets
from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# ================================
# SETUP
# ================================

app = FastAPI(
    title="04a - Basic HTTP Authentication",
    description="Learn HTTP Basic Auth pattern",
    version="4a.0.0"
)

security = HTTPBasic()

# In-memory "database" (for learning only - use real DB in production)
users_db = {
    "alice": {"password": "secret123", "role": "admin"},
    "bob": {"password": "password456", "role": "user"},
    "charlie": {"password": "pass789", "role": "user"},
}


# ================================
# AUTHENTICATION UTILITIES
# ================================

def verify_password(plain: str, stored: str) -> bool:
    """
    Secure string comparison to prevent timing attacks.
    
    Timing attacks exploit how long it takes to compare strings.
    secrets.compare_digest() always takes the same time regardless of match.
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
    3. Return username if valid, else raise exception
    """
    user = users_db.get(credentials.username)

    # User doesn't exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Password doesn't match
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


# ================================
# PROTECTED ENDPOINTS
# ================================

@app.get("/")
def read_root():
    """Public endpoint - no auth required"""
    return {"message": "Welcome to Basic Auth Demo"}


@app.get("/protected")
def read_protected(
    current_user: Annotated[str, Depends(authenticate_user)]
):
    """
    Protected endpoint - requires authentication.
    
    The `Depends(authenticate_user)` ensures the user is authenticated
    before this function is called.
    """
    return {
        "message": f"Hello {current_user}!",
        "info": "You are authenticated!"
    }


@app.get("/profile")
def get_user_profile(
    current_user: Annotated[str, Depends(authenticate_user)]
):
    """Get current user's profile"""
    user_data = users_db.get(current_user)
    return {
        "username": current_user,
        "role": user_data["role"],
        "status": "active"
    }


# ================================
# ADMIN-ONLY ENDPOINT
# ================================

def check_admin(current_user: Annotated[str, Depends(authenticate_user)]) -> str:
    """Dependency to check if user is admin"""
    user_data = users_db.get(current_user)
    if user_data["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


@app.get("/admin/users")
def list_all_users(admin_user: Annotated[str, Depends(check_admin)]):
    """Admin-only endpoint to list all users"""
    return {
        "admin": admin_user,
        "users": list(users_db.keys()),
        "total": len(users_db)
    }


