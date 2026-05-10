from fastapi import FastAPI
from app.routes.issues import router as issues_router
from app.middleware.timer import timing_middleware
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI application instance
app = FastAPI()

# Add custom middleware to measure request processing time
app.middleware("http")(timing_middleware)

# Enable CORS (Cross-Origin Resource Sharing)
# Allows frontend apps (React, etc.) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins
    allow_credentials=True,    # Allow cookies/auth headers
    allow_methods=["*"],      # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],      # Allow all headers
)

# Register issues router (all issue endpoints)
app.include_router(issues_router)