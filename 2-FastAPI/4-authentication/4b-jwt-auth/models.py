"""
User and Post models for JWT Auth demo
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegister(BaseModel):
    """User registration schema"""
    full_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    
    class Config:
        schema_extra = {
            "example": {
                "full_name": "John Doe",
                "email": "john@example.com",
                "password": "securepass123"
            }
        }


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "securepass123"
            }
        }


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class PostCreate(BaseModel):
    """Post creation schema"""
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=10)
    
    class Config:
        schema_extra = {
            "example": {
                "title": "My First Post",
                "content": "This is the content of my first post"
            }
        }


class PostOut(BaseModel):
    """Post response schema"""
    id: int
    title: str
    content: str
    author: str
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "My First Post",
                "content": "This is the content of my first post",
                "author": "john@example.com"
            }
        }
