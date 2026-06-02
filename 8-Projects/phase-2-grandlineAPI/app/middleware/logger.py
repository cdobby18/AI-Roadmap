# ─── app/middleware/logger.py ─────────────────────────────────────────────────
# Den Den Mushi Logger — intercepts every HTTP request and logs it.
# Middleware runs BEFORE the route handler and AFTER the response is built,
# so it can measure the full round-trip time.
#
# What to log per request:
#   [METHOD] /path → status_code  (took Xms)
#   Example: [POST] /pirates → 201  (took 12ms)
#
# TODO: Import Request and time (or time.perf_counter for precision)
#       Import logging from the standard library (no pip install needed)
#
# TODO: Set up a logger instance at the top of the file
#       logger = logging.getLogger("grandline")
#       Optionally configure a log format and level
#
# ─── log_requests middleware ──────────────────────────────────────────────────
# TODO: Write an async function log_requests(request: Request, call_next)
#       This is the middleware function FastAPI will call for every request.
#       Steps inside:
#         1. Record start time before calling call_next
#         2. response = await call_next(request)  ← this runs the actual route
#         3. Record end time and calculate duration in milliseconds
#         4. Log: method, path, response status code, duration
#         5. Return the response (don't forget this — the client needs it)
#
# Register in main.py with:
#   app.middleware("http")(log_requests)
#   OR
#   app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)
