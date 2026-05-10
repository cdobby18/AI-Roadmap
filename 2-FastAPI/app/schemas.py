from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

# Issue status options
class IssuesStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"

# Issue priority options
class IssuePriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

# Schema for creating issue
class IssueCreate(BaseModel):
    # Issue title validation
    title: str = Field(min_length=3, max_length=100)
    # Issue description validation
    description: str = Field(min_length=5, max_length=1000)
    # Default issue priority
    priority: IssuePriority = IssuePriority.medium

# Schema for updating issue [OPTIONAL]
class IssueUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[IssuePriority] = None
    status: Optional[IssuesStatus] = None

# Schema for API response
class IssueOut(BaseModel):
    id: str
    title: str
    description: str
    priority: IssuePriority
    status: IssuesStatus