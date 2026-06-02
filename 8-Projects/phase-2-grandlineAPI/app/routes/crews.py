# ─── app/routes/crews.py ──────────────────────────────────────────────────────
# CRUD endpoints for Crews.
# Public:    GET /crews, GET /crews/{id}
# Protected: POST, PUT, DELETE (require valid JWT)
#
# TODO: Import APIRouter, HTTPException, status, Depends from fastapi
#       Import Session from sqlalchemy.orm
#       Import get_db from app.database
#       Import Crew from app.models
#       Import CrewCreate, CrewUpdate, CrewResponse from app.schemas.crew
#       Import get_current_marine from app.auth.jwt_bearer
#
# TODO: Create the router:  router = APIRouter()
#
# ─── GET /crews ───────────────────────────────────────────────────────────────
# TODO: Return all crews
#       Hint: db.query(Crew).all()
#       Response model: list[CrewResponse]
#
# ─── GET /crews/{crew_id} ─────────────────────────────────────────────────────
# TODO: Return a single crew by ID
#       404 if not found
#       Response model: CrewResponse
#
# ─── POST /crews ──────────────────────────────────────────────────────────────
# TODO: Create a new crew (protected)
#       Steps:
#         1. Build a Crew ORM object from crew_data.model_dump()
#         2. db.add(crew), db.commit(), db.refresh(crew)
#         3. Return the created crew
#       Response model: CrewResponse, status_code=201
#
# ─── PUT /crews/{crew_id} ─────────────────────────────────────────────────────
# TODO: Update an existing crew (protected)
#       Use exclude_unset=True so partial updates don't overwrite fields to None
#       db.commit(), db.refresh(crew), return updated crew
#
# ─── DELETE /crews/{crew_id} ──────────────────────────────────────────────────
# TODO: Delete a crew (protected)
#       404 if not found, then db.delete(crew), db.commit()
#       Return 204 No Content
#
# ─── BONUS ────────────────────────────────────────────────────────────────────
# TODO (stretch): Add GET /crews/{crew_id}/pirates
#       Returns all pirates that belong to this crew
#       Hint: db.query(Pirate).filter(Pirate.crew_id == crew_id).all()
#       This is a nested/sub-resource pattern common in real APIs
