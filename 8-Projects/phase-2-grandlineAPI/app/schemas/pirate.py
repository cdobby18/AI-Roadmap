from typing import Optional
from pydantic import BaseModel, Field


class PirateCreate(BaseModel):
    name: str = Field(..., min_length=1)
    bounty: float = Field(default=0.0, ge=0)
    devil_fruit: Optional[str] = None
    role: Optional[str] = None
    crew_id: Optional[int] = None


class PirateUpdate(BaseModel):
    name: Optional[str] = None
    bounty: Optional[float] = Field(default=None, ge=0)
    devil_fruit: Optional[str] = None
    role: Optional[str] = None
    crew_id: Optional[int] = None


class PirateResponse(BaseModel):
    id: int
    name: str
    bounty: float
    devil_fruit: Optional[str]
    role: Optional[str]
    crew_id: Optional[int]
