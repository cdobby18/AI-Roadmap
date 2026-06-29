import logging
import time
from fastapi import Request

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("grandline")


async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(f"[{request.method}] {request.url.path} → {response.status_code} (took {duration_ms:.0f}ms)")
    return response
