# ─── main.py ──────────────────────────────────────────────────────────────────
# Entry point for the Grand Line API.
# This is where you wire everything together.
#
# TODO: Import FastAPI and create the app instance
#
# TODO: Set up the lifespan context manager
#       - On startup: call create_tables() so the DB and tables exist before
#         the first request comes in (no migrations needed for SQLite)
#       - On shutdown: clean up any open resources if needed
#       Hint: use @asynccontextmanager from contextlib
#
# TODO: Register the custom logger middleware
#       Hint: app.add_middleware(...) or app.middleware("http")
#
# TODO: Include routers from app/routes/
#       - auth router    → prefix="/auth",    tag="Auth"
#       - pirates router → prefix="/pirates", tag="Pirates"
#       - crews router   → prefix="/crews",   tag="Crews"
#
# TODO: Add a root GET "/" endpoint that returns a welcome message
#       Something like: {"message": "Welcome to the Grand Line API ☠️"}
#
# Run with: uvicorn main:app --reload
