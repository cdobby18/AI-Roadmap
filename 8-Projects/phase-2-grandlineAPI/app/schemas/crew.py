from typing import Optional
from pydantic import BaseModel, Field


class CrewCreate(BaseModel):
    name: str = Field(..., min_length=1)
    ship: Optional[str] = None
    sea_region: Optional[str] = None


class CrewUpdate(BaseModel):
    name: Optional[str] = None
    ship: Optional[str] = None
    sea_region: Optional[str] = None


class CrewResponse(BaseModel):
    id: int
    name: str
    ship: Optional[str]
    sea_region: Optional[str]
    is_active: bool
