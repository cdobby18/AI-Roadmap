# ─── app/auth/jwt_handler.py ──────────────────────────────────────────────────
# Handles the creation and decoding of JWT tokens.
# This file does not interact with FastAPI directly — it is pure token logic.
#
# How JWT works (review):
#   1. Marine logs in with username + password → server verifies credentials
#   2. Server creates a signed token containing a payload (e.g. {"sub": "sengoku"})
#   3. Client stores the token and sends it in the Authorization header on future requests
#   4. Server decodes the token on every protected request to confirm identity
#
# TODO: Import jwt from jose (python-jose)
#       Import datetime, timedelta from datetime
#       Import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES from app.config
#
# ─── create_access_token ──────────────────────────────────────────────────────
# TODO: Write a function create_access_token(data: dict) -> str
#       Steps inside:
#         1. Copy the data dict so you don't mutate the caller's dict
#         2. Calculate the expiry: datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#         3. Add "exp" key to the copy with the expiry datetime
#         4. Encode: jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
#         5. Return the encoded token string
#
# ─── decode_access_token ──────────────────────────────────────────────────────
# TODO: Write a function decode_access_token(token: str) -> dict | None
#       Steps inside:
#         1. Try to decode: jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         2. Return the decoded payload dict on success
#         3. Catch JWTError and return None (expired or tampered token)
