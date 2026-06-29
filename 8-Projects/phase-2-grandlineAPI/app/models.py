from typing import Optional, TypedDict


class Crew(TypedDict):
    id: int
    name: str
    ship: Optional[str]
    sea_region: Optional[str]
    is_active: bool


class Pirate(TypedDict):
    id: int
    name: str
    bounty: float
    devil_fruit: Optional[str]
    role: Optional[str]
    crew_id: Optional[int]
