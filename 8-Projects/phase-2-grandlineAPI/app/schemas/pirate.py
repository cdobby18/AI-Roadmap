# ─── app/schemas/pirate.py ────────────────────────────────────────────────────
# Pydantic schemas for the Pirate resource.
# These control what the API accepts (request body) and what it returns (response).
#
# Why separate schemas from models?
#   - You may not want to expose every field to the client
#   - Input validation rules (min_length, ge=0) belong here, not in the data store
#   - Request shape and response shape can differ
#
# How Pydantic works with plain dicts (no ORM):
#   When your route returns a dict, FastAPI passes it to the response_model schema.
#   Pydantic reads the dict keys directly — no special config needed.
#   Just return a dict and Pydantic handles validation automatically.
#
# TODO: Import BaseModel and Field from pydantic
#       Import Optional from typing
#
# ─── PirateCreate ─────────────────────────────────────────────────────────────
# TODO: Schema for POST /pirates (creating a pirate — client sends this)
#       Fields:
#         - name        : str, required, min_length=1
#         - bounty      : float, default=0.0, ge=0   (cannot be negative)
#         - devil_fruit : Optional[str], default=None
#         - role        : Optional[str], default=None
#         - crew_id     : Optional[int], default=None
#
# ─── PirateUpdate ─────────────────────────────────────────────────────────────
# TODO: Schema for PUT /pirates/{id} (partial update — all fields optional)
#       Same fields as PirateCreate but every field wrapped in Optional
#       Hint: Optional[str] = None means the client doesn't have to send it
#             model_dump(exclude_unset=True) in the route will skip unset fields
#
# ─── PirateResponse ───────────────────────────────────────────────────────────
# TODO: Schema for what the API returns (includes id from the store)
#       Fields: id, name, bounty, devil_fruit, role, crew_id
#       No special config needed — Pydantic reads plain dicts out of the box
