from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from app.store import crews_db, pirates_db, get_crew_by_id
import app.store as store
from app.schemas.crew import CrewCreate, CrewUpdate, CrewResponse
from app.schemas.pirate import PirateResponse
from app.auth.jwt_bearer import get_current_marine
from app.middleware.rate_limiter import limiter

router = APIRouter()


@router.get("", response_model=list[CrewResponse])
@limiter.limit("60/minute")
async def list_crews(request: Request):
    return crews_db


@router.get("/{crew_id}", response_model=CrewResponse)
@limiter.limit("60/minute")
async def get_crew(request: Request, crew_id: int):
    crew = get_crew_by_id(crew_id)
    if not crew:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crew not found")
    return crew


@router.post("", response_model=CrewResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
async def create_crew(request: Request, crew_data: CrewCreate, marine: str = Depends(get_current_marine)):
    new_crew = {**crew_data.model_dump(), "id": store.next_crew_id, "is_active": True}
    crews_db.append(new_crew)
    store.next_crew_id += 1
    return new_crew


@router.put("/{crew_id}", response_model=CrewResponse)
@limiter.limit("30/minute")
async def update_crew(request: Request, crew_id: int, crew_data: CrewUpdate, marine: str = Depends(get_current_marine)):
    crew = get_crew_by_id(crew_id)
    if not crew:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crew not found")
    crew.update(crew_data.model_dump(exclude_unset=True))
    return crew


@router.delete("/{crew_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("30/minute")
async def delete_crew(request: Request, crew_id: int, marine: str = Depends(get_current_marine)):
    crew = get_crew_by_id(crew_id)
    if not crew:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crew not found")
    crews_db.remove(crew)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{crew_id}/pirates", response_model=list[PirateResponse])
@limiter.limit("60/minute")
async def get_crew_pirates(request: Request, crew_id: int):
    if not get_crew_by_id(crew_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crew not found")
    return [p for p in pirates_db if p["crew_id"] == crew_id]
