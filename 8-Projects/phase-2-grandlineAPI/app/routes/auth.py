# ─── app/routes/auth.py ───────────────────────────────────────────────────────
# Authentication routes — the only public endpoint that issues JWT tokens.
# Think of this as the Marine HQ login desk.
#
# No database involved — credentials are checked against the constants
# defined in app/config.py (MARINE_USERNAME and MARINE_PASSWORD).
#
# TODO: Import APIRouter from fastapi
#       Import HTTPException, status from fastapi
#       Import OAuth2PasswordRequestForm from fastapi.security
#       Import Depends from fastapi
#       Import create_access_token from app.auth.jwt_handler
#       Import MARINE_USERNAME, MARINE_PASSWORD from app.config
#
# TODO: Create the router:  router = APIRouter()
#
# ─── POST /auth/login ─────────────────────────────────────────────────────────
# TODO: Create a POST "/login" endpoint
#       Accepts: OAuth2PasswordRequestForm (FastAPI handles parsing username/password)
#       Steps inside:
#         1. Check form.username == MARINE_USERNAME
#            AND form.password == MARINE_PASSWORD
#            (hardcoded check — no DB query needed)
#         2. If credentials don't match → raise HTTPException 401 "Invalid credentials"
#         3. Call create_access_token({"sub": form.username}) to generate a token
#         4. Return {"access_token": token, "token_type": "bearer"}
#
# Note: OAuth2PasswordRequestForm parses the request as form data (not JSON).
#       The Swagger UI "Authorize" button sends credentials in this exact format.
#       Test it by clicking "Authorize" in /docs, entering the credentials from config.py.
