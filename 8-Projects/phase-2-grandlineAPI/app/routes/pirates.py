from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status, Request
from app.store import pirates_db, get_pirate_by_id
import app.store as store
from app.schemas.pirate import PirateCreate, PirateUpdate, PirateResponse
from app.auth.jwt_bearer import get_current_marine
from app.middleware.rate_limiter import limiter

router = APIRouter()


def recalculate_bounty(pirate_id: int):
    pirate = get_pirate_by_id(pirate_id)
    if pirate:
        pirate["bounty"] = round(pirate["bounty"] * 1.1, 2)
        print(f"Bounty updated for pirate {pirate_id}")


@router.get("", response_model=list[PirateResponse])
@limiter.limit("60/minute")
async def list_pirates(request: Request):
    return pirates_db


@router.get("/{pirate_id}", response_model=PirateResponse)
@limiter.limit("60/minute")
async def get_pirate(request: Request, pirate_id: int):
    pirate = get_pirate_by_id(pirate_id)
    if not pirate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pirate not found")
    return pirate


@router.post("", response_model=PirateResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
async def create_pirate(request: Request, pirate_data: PirateCreate, background_tasks: BackgroundTasks, marine: str = Depends(get_current_marine)):
    new_pirate = {**pirate_data.model_dump(), "id": store.next_pirate_id}
    pirates_db.append(new_pirate)
    store.next_pirate_id += 1
    background_tasks.add_task(recalculate_bounty, new_pirate["id"])
    return new_pirate


@router.put("/{pirate_id}", response_model=PirateResponse)
@limiter.limit("30/minute")
async def update_pirate(request: Request, pirate_id: int, pirate_data: PirateUpdate, marine: str = Depends(get_current_marine)):
    pirate = get_pirate_by_id(pirate_id)
    if not pirate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pirate not found")
    pirate.update(pirate_data.model_dump(exclude_unset=True))
    return pirate


@router.delete("/{pirate_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("30/minute")
async def delete_pirate(request: Request, pirate_id: int, marine: str = Depends(get_current_marine)):
    pirate = get_pirate_by_id(pirate_id)
    if not pirate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pirate not found")
    pirates_db.remove(pirate)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
