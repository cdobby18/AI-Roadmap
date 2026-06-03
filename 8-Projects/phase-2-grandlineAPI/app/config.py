# ─── app/config.py ────────────────────────────────────────────────────────────
# Holds all app-wide configuration constants.
# No .env file needed — values are hardcoded here for this practice project.
# In a real app you would load these from environment variables or a secrets manager.
#
# Why a dedicated config file instead of scattering constants everywhere?
#   - One place to change a value and have it apply across all files
#   - Makes it obvious what the "knobs" of your app are
#   - Easy to swap to environment-based config later without touching route files
#
# TODO: Define these constants directly (no class needed, just plain variables):
#
#       SECRET_KEY   : str   — any long random string used to sign JWT tokens
#                              e.g. "grand-line-secret-change-in-production"
#
#       ALGORITHM    : str   — the JWT signing algorithm, use "HS256"
#
#       ACCESS_TOKEN_EXPIRE_MINUTES : int — how long a token is valid, e.g. 30
#
#       MARINE_USERNAME : str — the hardcoded login username, e.g. "sengoku"
#
#       MARINE_PASSWORD : str — the hardcoded login password, e.g. "marineford"
#
# Note: In a real app NEVER hardcode credentials — use os.getenv() or a secrets vault.
#       For this practice project it is fine.
#
# Usage: from app.config import SECRET_KEY, ALGORITHM, ...
