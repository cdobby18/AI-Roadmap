# ─── app/schemas/pirate.py ────────────────────────────────────────────────────
# Pydantic schemas for the Pirate resource.
# These control what the API accepts (request) and what it returns (response).
#
# Why separate schemas from models?
#   - You may not want to expose every DB column to the client (e.g. internal IDs)
#   - Input validation rules belong here, not in the ORM model
#   - Response shapes can differ from DB shapes (e.g. nest crew name instead of crew_id)
#
# TODO: Import BaseModel and Field from pydantic; Optional from typing
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
# TODO: Schema for PUT /pirates/{id} (all fields optional — partial update)
#       Same fields as PirateCreate but every field is Optional
#       Hint: Optional[str] = None means the client doesn't have to send it
#
# ─── PirateResponse ───────────────────────────────────────────────────────────
# TODO: Schema for what the API returns (includes id from DB)
#       Fields: id, name, bounty, devil_fruit, role, crew_id
#       Add model_config = ConfigDict(from_attributes=True)
#       This lets Pydantic read values directly from a SQLAlchemy model object
