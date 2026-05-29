from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


# Issue status options
class IssuesStatus(str, Enum):
    """Status enum for issues"""
    open = "open"
    in_progress = "in_progress"
    closed = "closed"


# Issue priority options
class IssuePriority(str, Enum):
    """Priority enum for issues"""
    low = "low"
    medium = "medium"
    high = "high"


# Schema for creating issue
class IssueCreate(BaseModel):
    """Schema for creating a new issue"""
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=1000)
    priority: IssuePriority = IssuePriority.medium
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Fix login bug",
                "description": "Users cannot login with email containing numbers",
                "priority": "high"
            }
        }


# Schema for updating issue
class IssueUpdate(BaseModel):
    """Schema for updating an issue (all fields optional)"""
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[IssuePriority] = None
    status: Optional[IssuesStatus] = None


# Schema for API response
class IssueOut(BaseModel):
    """Schema for issue API responses"""
    id: str
    title: str
    description: str
    priority: IssuePriority
    status: IssuesStatus
