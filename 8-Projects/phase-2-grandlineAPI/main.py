# ─── main.py ──────────────────────────────────────────────────────────────────
# Entry point for the Grand Line API.
# This is where you wire everything together — routers, middleware, and the
# root endpoint.
#
# No database setup needed here — store.py holds the data in memory and
# is ready as soon as Python imports it.

from fastapi import FastAPI

app = FastAPI(
    title = "Grandline API",
    description = "TRACK PIRATES - ONE PIECE GRANDLINE"
)


# TODO: Register the custom logger middleware
#       app.middleware("http")(log_requests)
#       OR
#       app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)
#       Hint: import log_requests from app.middleware.logger
#             import BaseHTTPMiddleware from starlette.middleware.base (if using that form)
#
# TODO: Include routers from app/routes/
#       - auth router    → prefix="/auth",    tags=["Auth"]
#       - pirates router → prefix="/pirates", tags=["Pirates"]
#       - crews router   → prefix="/crews",   tags=["Crews"]
#       Hint: app.include_router(router, prefix=..., tags=...)
#

@app.get("/")
def root():
    return {"Message: ", "Welcome to the Grandline API"}

# Run with: uvicorn main:app --reload
# Docs at:  http://localhost:8000/docs
