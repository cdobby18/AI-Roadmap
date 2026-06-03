# ─── main.py ──────────────────────────────────────────────────────────────────
# Entry point for the Grand Line API.
# This is where you wire everything together — routers, middleware, and the
# root endpoint.
#
# No database setup needed here — store.py holds the data in memory and
# is ready as soon as Python imports it.
#
# TODO: Import FastAPI and create the app instance
#       Give it a title and description (these show up in /docs)
#       e.g. title="Grand Line API", description="Track pirates across the Grand Line"
#
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
# TODO: Add a root GET "/" endpoint that returns a welcome message
#       e.g. {"message": "Welcome to the Grand Line API ☠️"}
#       This is useful as a health check — you can hit "/" to confirm the server is up
#
# Run with: uvicorn main:app --reload
# Docs at:  http://localhost:8000/docs
