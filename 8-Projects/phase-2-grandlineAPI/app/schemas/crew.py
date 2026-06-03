# ─── app/schemas/crew.py ──────────────────────────────────────────────────────
# Pydantic schemas for the Crew resource.
#
# How Pydantic works with plain dicts (no ORM):
#   Routes return plain dicts from crews_db — Pydantic validates them
#   against the response_model automatically. No special config needed.
#
# TODO: Import BaseModel, Field from pydantic
#       Import Optional from typing
#
# ─── CrewCreate ───────────────────────────────────────────────────────────────
# TODO: Schema for POST /crews (client sends this when creating a crew)
#       Fields:
#         - name       : str, required, min_length=1   (e.g. "Straw Hat Pirates")
#         - ship       : Optional[str], default=None   (e.g. "Thousand Sunny")
#         - sea_region : Optional[str], default=None   (e.g. "New World")
#
# ─── CrewUpdate ───────────────────────────────────────────────────────────────
# TODO: Schema for PUT /crews/{id} (partial update — all fields optional)
#       Same fields as CrewCreate but every field is Optional with default=None
#
# ─── CrewResponse ─────────────────────────────────────────────────────────────
# TODO: Schema for what the API returns (includes id and is_active)
#       Fields: id, name, ship, sea_region, is_active
#       No special config needed — Pydantic reads plain dicts out of the box
