"""
Middleware for measuring request processing time.
This demonstrates how to create custom middleware.
"""

import time
from fastapi import Request


async def timing_middleware(request: Request, call_next):
    """
    Measure and log the time taken to process each request.
    
    This middleware:
    1. Records the start time
    2. Processes the request
    3. Measures elapsed time
    4. Adds timing info to response headers
    """
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Add custom header with processing time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Print for debugging (optional)
    print(f"{request.method} {request.url.path} - {process_time:.3f}s")
    
    return response
