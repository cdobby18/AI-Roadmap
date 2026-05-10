import time
from fastapi import Request

# Middleware to measure request processing time
async def timing_middleware(request: Request, call_next):

    # Start timer before request is processed
    start = time.perf_counter()

    # Process request and get response
    response = await call_next(request)

    # Calculate total processing time
    process_time = time.perf_counter() - start

    # Add custom header to response
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"

    return response