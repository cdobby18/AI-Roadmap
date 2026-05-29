"""
03 - ADVANCED ROUTING: Production Patterns

Learn:
- APIRouter for modular routing
- Middleware for cross-cutting concerns
- Persistent storage (JSON file)
- Error handling and validation
- Project structure best practices

Run: uvicorn main:app --reload
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.timer import timing_middleware
from routes.issues import router as issues_router

# ================================
# FASTAPI APP SETUP
# ================================

app = FastAPI(
    title="03 - Advanced Routing",
    description="Production-ready FastAPI patterns with middleware and modular routes",
    version="3.0.0"
)

# Add custom middleware to measure request processing time
app.middleware("http")(timing_middleware)

# Enable CORS (Cross-Origin Resource Sharing)
# Allows frontend apps (React, Vue, etc.) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allow all origins (restrict in production)
    allow_credentials=True,         # Allow cookies/auth headers
    allow_methods=["*"],            # Allow all HTTP methods
    allow_headers=["*"],            # Allow all headers
)

# Include routers from different modules
app.include_router(issues_router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Advanced FastAPI with modular routing",
        "docs": "/docs",
        "api_version": "3.0.0"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
