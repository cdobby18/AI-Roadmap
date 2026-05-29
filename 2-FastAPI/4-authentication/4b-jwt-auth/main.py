"""
04b - AUTHENTICATION: JWT Token-Based Auth

Learn:
- JSON Web Tokens (JWT) for stateless authentication
- Token generation and validation
- Bearer token pattern
- Protected routes with token verification
- User registration and login flow

Key Concepts:
- JWT = Header.Payload.Signature
- Stateless: server doesn't need to store sessions
- Use HTTPS in production
- Include token in Authorization: Bearer <token> header

Run: uvicorn main:app --reload

Test Flow:
1. POST /auth/signup with email/password
2. Receive access_token
3. Use token in "Authorization: Bearer <token>" header for protected routes
"""

import hashlib
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status, Body
from datetime import timedelta

from models import UserRegister, UserLogin, TokenResponse, PostCreate, PostOut
from auth.jwt_handler import create_access_token, decode_token
from auth.jwt_bearer import JWTBearer

# ================================
# SETUP
# ================================

app = FastAPI(
    title="04b - JWT Token Authentication",
    description="Learn stateless JWT-based authentication",
    version="4b.0.0"
)

jwt_bearer = JWTBearer()

# In-memory "database" (use real DB in production)
users_db = {}  # {email: {"password_hash": "...", "full_name": "..."}}
posts_db = []  # List of posts

# Counter for post IDs
post_id_counter = 0


# ================================
# UTILITY FUNCTIONS
# ================================

def hash_password(password: str) -> str:
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return hash_password(plain_password) == hashed_password


# ================================
# PUBLIC ENDPOINTS
# ================================

@app.get("/")
def read_root():
    """Public endpoint"""
    return {
        "message": "JWT Authentication Demo",
        "endpoints": {
            "signup": "POST /auth/signup",
            "login": "POST /auth/login",
            "protected": "GET /posts (requires token)"
        }
    }


# ================================
# AUTHENTICATION ENDPOINTS
# ================================

@app.post("/auth/signup", response_model=TokenResponse)
def signup(user_data: UserRegister = Body(...)):
    """
    Register a new user and get an access token.
    
    This demonstrates:
    - User registration
    - Password hashing
    - Automatic token generation
    """
    # Check if user already exists
    if user_data.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Store user with hashed password
    users_db[user_data.email] = {
        "full_name": user_data.full_name,
        "password_hash": hash_password(user_data.password)
    }
    
    # Generate JWT token
    access_token = create_access_token(
        data={"sub": user_data.email},
        expires_delta=timedelta(hours=24)
    )
    
    return TokenResponse(access_token=access_token)


@app.post("/auth/login", response_model=TokenResponse)
def login(credentials: UserLogin = Body(...)):
    """
    Login user with email and password.
    
    Returns JWT token if credentials are valid.
    """
    user = users_db.get(credentials.email)
    
    # User doesn't exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Password doesn't match
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate JWT token
    access_token = create_access_token(
        data={"sub": credentials.email},
        expires_delta=timedelta(hours=24)
    )
    
    return TokenResponse(access_token=access_token)


# ================================
# PROTECTED ENDPOINTS
# ================================

@app.get("/auth/me")
def get_current_user(token_data: dict = Depends(jwt_bearer)):
    """
    Get current authenticated user info.
    
    Requires valid JWT token in Authorization header.
    """
    email = token_data.get("sub")
    user = users_db.get(email)
    
    return {
        "email": email,
        "full_name": user["full_name"],
        "status": "authenticated"
    }


@app.post("/posts", response_model=PostOut)
def create_post(
    post_data: PostCreate,
    token_data: dict = Depends(jwt_bearer)
):
    """
    Create a new post (requires authentication).
    
    The Depends(jwt_bearer) ensures only authenticated users can create posts.
    """
    global post_id_counter
    
    post_id_counter += 1
    new_post = {
        "id": post_id_counter,
        "title": post_data.title,
        "content": post_data.content,
        "author": token_data.get("sub")  # Email from JWT token
    }
    
    posts_db.append(new_post)
    return new_post


@app.get("/posts", response_model=list[PostOut])
def list_posts(token_data: dict = Depends(jwt_bearer)):
    """
    List all posts (requires authentication).
    """
    return posts_db


@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(
    post_id: int,
    token_data: dict = Depends(jwt_bearer)
):
    """
    Get a specific post (requires authentication).
    """
    for post in posts_db:
        if post["id"] == post_id:
            return post
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )


# ================================
# HOW TO TEST
# ================================
# 1. POST /auth/signup
#    Body: {"full_name": "John", "email": "john@example.com", "password": "securepass123"}
#    Get: access_token
#
# 2. POST /auth/login
#    Body: {"email": "john@example.com", "password": "securepass123"}
#    Get: access_token
#
# 3. POST /posts (with Authorization: Bearer <token>)
#    Body: {"title": "My Post", "content": "Post content here"}
#
# 4. GET /posts (with Authorization: Bearer <token>)
