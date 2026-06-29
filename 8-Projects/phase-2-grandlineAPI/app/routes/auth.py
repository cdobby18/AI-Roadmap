from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.jwt_handler import create_access_token
from app.config import MARINE_USERNAME, MARINE_PASSWORD
from app.middleware.rate_limiter import limiter
from fastapi import Request

router = APIRouter()


@router.post("/login")
@limiter.limit("10/minute")
async def login(request: Request, form: OAuth2PasswordRequestForm = Depends()):
    if form.username != MARINE_USERNAME or form.password != MARINE_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": form.username})
    return {"access_token": token, "token_type": "bearer"}
