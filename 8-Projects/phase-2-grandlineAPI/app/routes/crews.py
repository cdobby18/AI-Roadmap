# ─── app/routes/crews.py ──────────────────────────────────────────────────────
# CRUD endpoints for Crews.
# Public:    GET /crews, GET /crews/{id}
# Protected: POST, PUT, DELETE (require valid JWT)
#
# Data source: app/store.py  (in-memory lists — no database or ORM)
# All operations read from or mutate crews_db directly.
#
# TODO: Import APIRouter, HTTPException, status, Depends, Response from fastapi
#       Import crews_db, next_crew_id, pirates_db from app.store
#       Import CrewCreate, CrewUpdate, CrewResponse from app.schemas.crew
#       Import PirateResponse from app.schemas.pirate  (needed for the bonus endpoint)
#       Import get_current_marine from app.auth.jwt_bearer
#
# TODO: Create the router:  router = APIRouter()
#
# ─── GET /crews ───────────────────────────────────────────────────────────────
# TODO: Return the full crews_db list
#       Response model: list[CrewResponse]
#
# ─── GET /crews/{crew_id} ─────────────────────────────────────────────────────
# TODO: Find and return a single crew by ID
#       404 if not found
#       Response model: CrewResponse
#
# ─── POST /crews ──────────────────────────────────────────────────────────────
# TODO: Create a new crew (protected)
#       Steps:
#         1. Declare global next_crew_id
#         2. Build a new crew dict from crew_data.model_dump()
#            Add "id": next_crew_id and "is_active": True
#         3. Append to crews_db
#         4. Increment next_crew_id
#         5. Return the new crew dict
#       Response model: CrewResponse, status_code=201
#
# ─── PUT /crews/{crew_id} ─────────────────────────────────────────────────────
# TODO: Update an existing crew (protected)
#       Use model_dump(exclude_unset=True) so partial updates don't wipe other fields
#       Update the dict in-place with crew.update(changes)
#       Return the updated crew dict
#       Response model: CrewResponse
#
# ─── DELETE /crews/{crew_id} ──────────────────────────────────────────────────
# TODO: Delete a crew (protected)
#       404 if not found, then crews_db.remove(crew)
#       Return Response(status_code=status.HTTP_204_NO_CONTENT)
#
# ─── BONUS: GET /crews/{crew_id}/pirates ─────────────────────────────────────
# TODO (stretch): Return all pirates that belong to a given crew
#       Steps:
#         1. Confirm the crew exists (404 if not)
#         2. Filter pirates_db: [p for p in pirates_db if p["crew_id"] == crew_id]
#         3. Return the filtered list
#       Response model: list[PirateResponse]
#       This is a nested/sub-resource pattern common in real REST APIs
