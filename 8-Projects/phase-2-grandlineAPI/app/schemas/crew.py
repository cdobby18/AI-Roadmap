# ─── app/schemas/crew.py ──────────────────────────────────────────────────────
# Pydantic schemas for the Crew resource.
#
# TODO: Import BaseModel, Field, ConfigDict from pydantic; Optional from typing
#
# ─── CrewCreate ───────────────────────────────────────────────────────────────
# TODO: Schema for POST /crews (client sends this when creating a crew)
#       Fields:
#         - name       : str, required, min_length=1   (e.g. "Straw Hat Pirates")
#         - ship       : Optional[str], default=None   (e.g. "Thousand Sunny")
#         - sea_region : Optional[str], default=None   (e.g. "New World")
#
# ─── CrewUpdate ───────────────────────────────────────────────────────────────
# TODO: Schema for PUT /crews/{id} (all fields optional — partial update)
#       Same fields as CrewCreate but every field is Optional
#
# ─── CrewResponse ─────────────────────────────────────────────────────────────
# TODO: Schema for what the API returns (includes id and is_active from DB)
#       Fields: id, name, ship, sea_region, is_active
#       Add model_config = ConfigDict(from_attributes=True)
