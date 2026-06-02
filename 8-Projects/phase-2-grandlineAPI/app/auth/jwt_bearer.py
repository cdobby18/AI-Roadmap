# ─── app/auth/jwt_bearer.py ───────────────────────────────────────────────────
# A FastAPI dependency class that extracts and validates the JWT token
# from the Authorization header on every protected request.
#
# How FastAPI dependencies work:
#   When you put   token: str = Depends(get_current_marine)   in a route,
#   FastAPI calls get_current_marine() automatically before the route runs.
#   If it raises an HTTPException, the route never executes.
#
# TODO: Import HTTPException, status from fastapi
#       Import OAuth2PasswordBearer from fastapi.security
#       Import decode_access_token from app.auth.jwt_handler
#
# TODO: Create an OAuth2PasswordBearer instance
#       oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
#       This tells FastAPI's Swagger UI where the login endpoint is
#
# ─── get_current_marine ───────────────────────────────────────────────────────
# TODO: Write an async function get_current_marine(token: str = Depends(oauth2_scheme))
#       Steps inside:
#         1. Call decode_access_token(token) to get the payload
#         2. If payload is None → raise HTTPException 401 "Invalid or expired token"
#         3. Extract "sub" from the payload (this is the username)
#         4. If "sub" is missing → raise HTTPException 401 "Token missing subject"
#         5. Return the username string
#
# Usage in a route:
#   @router.post("/pirates")
#   def create_pirate(..., marine: str = Depends(get_current_marine)):
#       ...   ← only runs if the token is valid
