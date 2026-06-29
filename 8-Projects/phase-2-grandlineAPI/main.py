from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.middleware.logger import log_requests
from app.middleware.rate_limiter import limiter
from app.routes import auth, crews, pirates

app = FastAPI(
    title="Grand Line API",
    description="Track pirates, crews, and bounties across the Grand Line.",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(pirates.router, prefix="/pirates", tags=["Pirates"])
app.include_router(crews.router, prefix="/crews", tags=["Crews"])


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Welcome to the Grand Line API"}
